import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.gauss_bonnet_generator import GaussBonnetGenerator
from helpers import DELIM


SPHERE_RE = re.compile(
    r"Verify Gauss-Bonnet for a sphere of radius (\d+) with Euler "
    r"characteristic 2\."
)
TORUS_RE = re.compile(
    r"Verify Gauss-Bonnet for a flat rectangular torus of width (\d+) "
    r"and height (\d+), with Euler characteristic 0\."
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


def parse_problem(problem):
    match = SPHERE_RE.fullmatch(problem)
    if match:
        return {"variant": "sphere", "radius": int(match.group(1))}
    match = TORUS_RE.fullmatch(problem)
    assert match is not None, problem
    return {"variant": "flat_torus", "width": int(match.group(1)),
            "height": int(match.group(2))}


def expected_sphere(parts):
    radius_sq = parts["radius"] ** 2
    curvature = Fraction(1, radius_sq)
    area_coeff = 4 * radius_sq
    total_coeff = curvature * area_coeff
    rhs_coeff = 4
    answer = f"verified: integral K dA = {pi_text(total_coeff)} = 2pi chi"
    steps = [
        make_step("GAUSS_BONNET_SETUP", "sphere",
                  f"R={parts['radius']}", "chi=2"),
        make_step("THEOREM", "integral K dA = 2*pi*chi"),
        make_step("E", parts["radius"], 2, radius_sq),
        make_step("D", 1, radius_sq, fraction_text(curvature)),
        make_step("M", 4, radius_sq, area_coeff),
        make_step("M", fraction_text(curvature), area_coeff,
                  fraction_text(total_coeff)),
        make_step("M", 2, 2, rhs_coeff),
        make_step("CHECK", "integral K dA", pi_text(total_coeff),
                  f"2pi chi = {pi_text(rhs_coeff)}"),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_torus(parts):
    area = parts["width"] * parts["height"]
    answer = "verified: integral K dA = 0 = 2pi chi"
    steps = [
        make_step("GAUSS_BONNET_SETUP", "flat_torus",
                  f"width={parts['width']}, height={parts['height']}",
                  "chi=0"),
        make_step("THEOREM", "integral K dA = 2*pi*chi"),
        make_step("M", parts["width"], parts["height"], area),
        make_step("M", 0, area, 0),
        make_step("M", 2, 0, 0),
        make_step("CHECK", "integral K dA", "0", "2pi chi = 0"),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "sphere":
        return expected_sphere(parts)
    return expected_torus(parts)


class TestGaussBonnetGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GaussBonnetGenerator()

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

    def test_check_step_matches_gauss_bonnet(self):
        for _ in range(300):
            result = self.gen.generate()
            check = [s for s in result["steps"]
                     if s.startswith(f"CHECK{DELIM}")][-1]
            fields = check.split(DELIM)
            self.assertEqual(fields[2], fields[3].split(" = ")[1])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("sphere", "flat_torus"):
            gen = GaussBonnetGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"gauss_bonnet_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GaussBonnetGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
