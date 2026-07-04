import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.fundamental_form_generator import FundamentalFormGenerator
from helpers import DELIM


CYLINDER_RE = re.compile(
    r"For the cylinder r\(u,v\)=\((\d+) cos u,\1 sin u,v\), "
    r"0<=u<=(.+) and 0<=v<=(\d+), find E, F, G and the patch area\."
)
SPHERE_RE = re.compile(
    r"For the sphere r\(theta,phi\)=\((\d+) sin phi cos theta,\1 sin "
    r"phi sin theta,\1 cos phi\), 0<=theta<=(.+) and (\d+)<=phi<=(\d+)\. "
    r"Given cos\(\3\)=([^ ]+) and cos\(\4\)=([^,]+), find E, F, G "
    r"and the patch area\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def pi_text(multiplier):
    multiplier = Fraction(multiplier)
    if multiplier == 0:
        return "0"
    if multiplier == 1:
        return "pi"
    if multiplier == -1:
        return "-pi"
    if multiplier.denominator == 1:
        return f"{multiplier.numerator}pi"
    if multiplier.numerator == 1:
        return f"pi/{multiplier.denominator}"
    if multiplier.numerator == -1:
        return f"-pi/{multiplier.denominator}"
    return f"{multiplier.numerator}pi/{multiplier.denominator}"


def parse_pi(text):
    if text == "pi":
        return Fraction(1)
    match = re.fullmatch(r"(\d+)pi", text)
    if match:
        return Fraction(int(match.group(1)))
    match = re.fullmatch(r"pi/(\d+)", text)
    if match:
        return Fraction(1, int(match.group(1)))
    match = re.fullmatch(r"(\d+)pi/(\d+)", text)
    if match:
        return Fraction(int(match.group(1)), int(match.group(2)))
    raise AssertionError(text)


def parse_problem(problem):
    match = CYLINDER_RE.fullmatch(problem)
    if match:
        return {"variant": "cylinder_patch", "radius": int(match.group(1)),
                "theta": parse_pi(match.group(2)),
                "height": int(match.group(3))}
    match = SPHERE_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "sphere_patch",
        "radius": int(match.group(1)),
        "theta": parse_pi(match.group(2)),
        "phi1": int(match.group(3)),
        "phi2": int(match.group(4)),
        "cos1": Fraction(match.group(5)),
        "cos2": Fraction(match.group(6)),
    }


def expected_cylinder(parts):
    radius = parts["radius"]
    theta = parts["theta"]
    height = parts["height"]
    radius_sq = radius ** 2
    radius_theta = radius * theta
    area_coeff = radius_theta * height
    theta_text = pi_text(theta)
    answer = f"E = {radius_sq}, F = 0, G = 1, area = {pi_text(area_coeff)}"
    steps = [
        make_step("FUNDAMENTAL_FORM_SETUP", "cylinder",
                  f"R={radius}",
                  f"u in [0,{theta_text}], v in [0,{height}]"),
        make_step("PARTIAL", "r_u=(-R sin u,R cos u,0)",
                  "r_v=(0,0,1)"),
        make_step("E", radius, 2, radius_sq),
        make_step("DOT", "r_u dot r_u", radius_sq),
        make_step("DOT", "r_u dot r_v", 0),
        make_step("DOT", "r_v dot r_v", 1),
        make_step("M", radius_sq, 1, radius_sq),
        make_step("S", radius_sq, 0, radius_sq),
        make_step("ROOT", radius_sq, radius),
        make_step("AREA_INTEGRAL", "sqrt(EG-F^2)=R",
                  "area = R*theta*h"),
        make_step("M", radius, theta, radius_theta),
        make_step("M", radius_theta, height, area_coeff),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_sphere(parts):
    radius = parts["radius"]
    theta = parts["theta"]
    radius_sq = radius ** 2
    cos_diff = parts["cos1"] - parts["cos2"]
    theta_factor = radius_sq * theta
    area_coeff = theta_factor * cos_diff
    theta_text = pi_text(theta)
    e_text = f"{radius_sq}sin^2(phi)"
    answer = f"E = {e_text}, F = 0, G = {radius_sq}, area = {pi_text(area_coeff)}"
    steps = [
        make_step("FUNDAMENTAL_FORM_SETUP", "sphere", f"R={radius}",
                  f"theta in [0,{theta_text}], phi in "
                  f"[{parts['phi1']},{parts['phi2']}]"),
        make_step("PARTIAL",
                  "r_theta=(-R sin phi sin theta,R sin phi cos theta,0)",
                  "r_phi=(R cos phi cos theta,R cos phi sin theta,-R sin phi)"),
        make_step("DOT", "r_theta dot r_theta", e_text),
        make_step("DOT", "r_theta dot r_phi", 0),
        make_step("E", radius, 2, radius_sq),
        make_step("DOT", "r_phi dot r_phi", radius_sq),
        make_step("AREA_INTEGRAL", "sqrt(EG-F^2)=R^2 sin(phi)",
                  "area = R^2*theta*(cos phi1 - cos phi2)"),
        make_step("S", fraction_text(parts["cos1"]),
                  fraction_text(parts["cos2"]), fraction_text(cos_diff)),
        make_step("M", radius_sq, theta, theta_factor),
        make_step("M", theta_factor, fraction_text(cos_diff), area_coeff),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "cylinder_patch":
        return expected_cylinder(parts)
    return expected_sphere(parts)


class TestFundamentalFormGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FundamentalFormGenerator()

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
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    self.assertEqual(int(fields[2]) ** 2, int(fields[1]),
                                     raw_step)

    def test_variants_are_available(self):
        for variant in ("cylinder_patch", "sphere_patch"):
            gen = FundamentalFormGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"fundamental_form_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FundamentalFormGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
