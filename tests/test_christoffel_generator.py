import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.christoffel_generator import ChristoffelGenerator
from helpers import DELIM


POLAR_RE = re.compile(
    r"For the polar metric ds\^2 = dr\^2 \+ r\^2 dtheta\^2, compute "
    r"the nonzero Christoffel symbols at r=(\d+)\."
)
SPHERE_RE = re.compile(
    r"For the sphere metric ds\^2 = R\^2 dphi\^2 \+ R\^2 sin\^2\(phi\) "
    r"dtheta\^2 with R=(\d+), compute the nonzero Christoffel symbols "
    r"at phi=(\d+) deg\. Given sin\(phi\)=([^ ]+) and cos\(phi\)=([^\.]+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_exact(text):
    if text == "0":
        return Fraction(0), Fraction(0)
    if text == "sqrt(2)/2":
        return Fraction(0), Fraction(1, 2)
    if text == "-sqrt(2)/2":
        return Fraction(0), Fraction(-1, 2)
    return Fraction(text), Fraction(0)


def exact_text(value):
    rational, sqrt2 = value
    if sqrt2 == 0:
        return str(rational)
    if rational == 0 and sqrt2 == Fraction(1, 2):
        return "sqrt(2)/2"
    if rational == 0 and sqrt2 == Fraction(-1, 2):
        return "-sqrt(2)/2"
    raise AssertionError(value)


def exact_mul(left, right):
    a, b = parse_exact(left)
    c, d = parse_exact(right)
    return exact_text((a * c + 2 * b * d, a * d + b * c))


def exact_div(left, right):
    a, b = parse_exact(left)
    c, d = parse_exact(right)
    # Generated sphere cases divide monomials only.
    if d == 0:
        return exact_text((a / c, b / c))
    if b == 0 and a == 0:
        return "0"
    denom = c * c - 2 * d * d
    return exact_text(((a * c - 2 * b * d) / denom,
                       (b * c - a * d) / denom))


def parse_problem(problem):
    match = POLAR_RE.fullmatch(problem)
    if match:
        return {"variant": "polar", "radius": int(match.group(1))}
    match = SPHERE_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "sphere",
        "radius": int(match.group(1)),
        "phi": int(match.group(2)),
        "sin": match.group(3),
        "cos": match.group(4),
    }


def expected_polar(parts):
    radius = parts["radius"]
    radius_sq = radius ** 2
    two_r = 2 * radius
    gamma_r = -radius
    inv_rr = Fraction(1, radius_sq)
    temp = inv_rr * two_r
    gamma_theta = temp / 2
    answer = (
        f"Gamma^r_thetatheta = {gamma_r}, "
        f"Gamma^theta_rtheta = Gamma^theta_thetar = "
        f"{fraction_text(gamma_theta)}"
    )
    steps = [
        make_step("CHRISTOFFEL_SETUP", "polar",
                  "g_rr=1, g_thetatheta=r^2", f"r={radius}"),
        make_step("INVERSE_METRIC", "g^rr=1",
                  "g^thetatheta=1/r^2"),
        make_step("CHRISTOFFEL_FORMULA",
                  "Gamma^i_jk = 1/2 g^im(d_j g_mk + d_k g_mj - d_m g_jk)"),
        make_step("DERIV", "d_r g_thetatheta = 2r",
                  f"at r={radius}", two_r),
        make_step("M", "-1/2", two_r, gamma_r),
        make_step("E", radius, 2, radius_sq),
        make_step("D", 1, radius_sq, fraction_text(inv_rr)),
        make_step("M", fraction_text(inv_rr), two_r, fraction_text(temp)),
        make_step("D", fraction_text(temp), 2, fraction_text(gamma_theta)),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_sphere(parts):
    radius_sq = parts["radius"] ** 2
    sin_cos = exact_mul(parts["sin"], parts["cos"])
    gamma_phi = exact_mul("-1", sin_cos)
    cot = exact_div(parts["cos"], parts["sin"])
    answer = (
        f"Gamma^phi_thetatheta = {gamma_phi}, "
        f"Gamma^theta_phitheta = Gamma^theta_thetaphi = {cot}"
    )
    steps = [
        make_step("CHRISTOFFEL_SETUP", "sphere",
                  "g_phiphi=R^2, g_thetatheta=R^2 sin^2(phi)",
                  f"R={parts['radius']}, phi={parts['phi']} deg"),
        make_step("INVERSE_METRIC", "g^phiphi=1/R^2",
                  "g^thetatheta=1/(R^2 sin^2(phi))"),
        make_step("CHRISTOFFEL_FORMULA",
                  "Gamma^i_jk = 1/2 g^im(d_j g_mk + d_k g_mj - d_m g_jk)"),
        make_step("E", parts["radius"], 2, radius_sq),
        make_step("TRIG_VALUE", f"sin(phi)={parts['sin']}",
                  f"cos(phi)={parts['cos']}"),
        make_step("DERIV", "d_phi g_thetatheta",
                  "2R^2 sin(phi)cos(phi)"),
        make_step("M", parts["sin"], parts["cos"], sin_cos),
        make_step("M", -1, sin_cos, gamma_phi),
        make_step("D", parts["cos"], parts["sin"], cot),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "polar":
        return expected_polar(parts)
    return expected_sphere(parts)


class TestChristoffelGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ChristoffelGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    if "sqrt" in fields[1] or "sqrt" in fields[2]:
                        self.assertEqual(exact_mul(fields[1], fields[2]),
                                         fields[3], raw_step)
                    else:
                        self.assertEqual(Fraction(fields[1]) *
                                         Fraction(fields[2]),
                                         Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    if "sqrt" in fields[1] or "sqrt" in fields[2]:
                        self.assertEqual(exact_div(fields[1], fields[2]),
                                         fields[3], raw_step)
                    else:
                        self.assertEqual(Fraction(fields[1]) /
                                         Fraction(fields[2]),
                                         Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("polar", "sphere"):
            gen = ChristoffelGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"christoffel_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ChristoffelGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
