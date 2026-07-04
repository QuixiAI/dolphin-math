import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.curve_geometry_generator import CurveGeometryGenerator
from helpers import DELIM


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def split_terms(expr):
    if expr == "0":
        return []
    return [raw for raw in expr.replace(" - ", " + -").split(" + ")
            if raw]


def t_coeff(expr):
    total = 0
    for raw in split_terms(expr):
        sign = -1 if raw.startswith("-") else 1
        raw = raw[1:] if raw.startswith("-") else raw
        coeff = sign
        has_t = False
        for factor in raw.split("*"):
            if factor.isdigit():
                coeff *= int(factor)
            elif factor == "t":
                has_t = True
            else:
                pass
        if has_t:
            total += coeff
    return total


def oracle_answer(example):
    problem = example["problem"]
    if problem.startswith("Find the arc length"):
        x_t, y_t, t_end = re.fullmatch(
            r"Find the arc length of r\(t\) = <(.+), (.+)> for "
            r"0 <= t <= (\d+)\.",
            problem,
        ).groups()
        a = t_coeff(x_t)
        c = t_coeff(y_t)
        speed = math.isqrt(a * a + c * c)
        return f"arc length {speed * int(t_end)}"
    radius = int(re.fullmatch(
        r"For r\(t\) = <(\d+)\*cos\(t\), \d+\*sin\(t\)>, find "
        r"curvature, unit tangent, and unit normal at t = 0\.",
        problem,
    ).group(1))
    return (f"curvature {fmt_frac(Fraction(1, radius))}; "
            f"T(0)=<0, 1>; N(0)=<-1, 0>")


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "SPEED" and parts[1] == "sqrt(a^2 + b^2)":
            nums = [int(x) for x in re.findall(r"\(?(-?\d+)\)?\^2", parts[2])]
            if math.isqrt(nums[0] * nums[0] + nums[1] * nums[1]) != int(parts[3]):
                return False
        elif parts[0] == "ARC_LENGTH":
            left, right = parts[2].split("*")
            if int(left) * int(right) != int(parts[3]):
                return False
    return True


class TestCurveGeometryGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CurveGeometryGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_variant_outputs(self):
        cases = {
            "arc_line": "arc length",
            "circle_tn": "curvature",
        }
        for variant, phrase in cases.items():
            gen = CurveGeometryGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertIn(phrase, result["final_answer"])

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1\*|\+ 0|--")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)
                self.assertNotIn(f"{DELIM}{DELIM}", s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 2)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            CurveGeometryGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
