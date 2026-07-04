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

from generators.triangle_solve_generator import TriangleSolveGenerator
from helpers import DELIM


def oracle_check(example):
    """Recomputes with the given values; also cross-checks the given
    trig value against the real angle within rounding tolerance."""
    p = example["problem"]
    m = re.fullmatch(r"In triangle ABC, angle A = (\d+)°, angle "
                     r"B = (\d+)°, and side a = (\d+) \(opposite A\)\. "
                     r"Given sin \1° = ([\d.]+), sin \2° = ([\d.]+), "
                     r"find side b\.", p)
    if m:
        A, B, a = int(m.group(1)), int(m.group(2)), int(m.group(3))
        sA, sB = Fraction(m.group(4)), Fraction(m.group(5))
        assert abs(float(sA) - math.sin(math.radians(A))) < 0.02
        assert abs(float(sB) - math.sin(math.radians(B))) < 0.02
        b = a * sB / sA
        assert b.denominator == 1
        return example["final_answer"] == f"b = {b.numerator}"
    m = re.fullmatch(r"In triangle ABC, a = (\d+), b = (\d+), and the "
                     r"included angle C = (\d+)°\. Given cos \3° = "
                     r"(-?[\d.]+), find side c\.", p)
    if m:
        a, b, C = int(m.group(1)), int(m.group(2)), int(m.group(3))
        cv = Fraction(m.group(4))
        assert abs(float(cv) - math.cos(math.radians(C))) < 0.02
        c2 = a * a + b * b - 2 * a * b * cv
        c = math.isqrt(c2.numerator)
        assert c * c == c2.numerator
        return example["final_answer"] == f"c = {c}"
    m = re.fullmatch(r"In triangle ABC, a = (\d+), b = (\d+), and "
                     r"c = (\d+)\. Given cos (\d+)° = (-?[\d.]+), find "
                     r"angle C\.", p)
    assert m, p
    a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
    label, cv = int(m.group(4)), Fraction(m.group(5))
    computed = Fraction(a * a + b * b - c * c, 2 * a * b)
    assert computed == cv
    assert abs(float(cv) - math.cos(math.radians(label))) < 0.02
    return example["final_answer"] == f"C = {label}°"


class TestTriangleSolveGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TriangleSolveGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute, and sanity-check the given values
        against the true trig functions."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_theorem_always_cited(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"THEOREM{DELIM}")
                                for s in result["steps"]))

    def test_step_arithmetic_exact(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] in ("M", "A", "S", "D") and len(f) == 4:
                    x, y, z = (Fraction(v) for v in f[1:])
                    got = {"M": lambda: x * y, "A": lambda: x + y,
                           "S": lambda: x - y, "D": lambda: x / y}[f[0]]()
                    self.assertEqual(got, z, s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            TriangleSolveGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
