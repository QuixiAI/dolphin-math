import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.round_solids_generator import RoundSolidsGenerator
from helpers import DELIM


def oracle_answer(example):
    """Recomputes the answer from the problem text alone (exact, π symbolic)."""
    p = example["problem"]
    op = example["operation"]
    nums = [int(n) for n in re.findall(r"(\d+) units", p)]
    if op == "volume_pyramid":
        l, w, h = nums
        v = Fraction(l * w * h, 3)
        assert v.denominator == 1
        return f"{v.numerator} cubic units"
    if op == "volume_cone":
        r, h = nums
        c = Fraction(r * r * h, 3)
        assert c.denominator == 1
        return f"{c.numerator}π cubic units"
    if op == "volume_sphere":
        (n,) = nums
        r = n // 2 if "diameter" in p else n
        c = Fraction(4 * r ** 3, 3)
        coef = f"{c.numerator}π" if c.denominator == 1 else f"{4 * r ** 3}π/3"
        return f"{coef} cubic units"
    if op == "surface_area_pyramid":
        b, slant = nums
        return f"{b * b + 2 * b * slant} square units"
    if op == "surface_area_cone":
        r, h = nums
        slant_sq = r * r + h * h
        slant = int(slant_sq ** 0.5)
        assert slant * slant == slant_sq, "not a perfect square slant"
        return f"{r * r + r * slant}π square units"
    if op == "surface_area_sphere":
        (n,) = nums
        r = n // 2 if "diameter" in p else n
        return f"{4 * r * r}π square units"
    raise AssertionError(op)


class TestRoundSolidsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RoundSolidsGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_all_variants_reachable(self):
        seen = {self.gen.generate()["operation"] for _ in range(150)}
        self.assertEqual(seen, set(RoundSolidsGenerator.VARIANTS))

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute every answer from the problem text alone."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_step_arithmetic(self):
        """E, A, M, and ROOT steps must be independently true."""
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "ROOT":
                    self.assertEqual(int(f[2]) ** 2, int(f[1]), s)

    def test_pi_answers_only_where_expected(self):
        for _ in range(200):
            result = self.gen.generate()
            has_pi = "π" in result["final_answer"]
            expects_pi = result["operation"] in (
                "volume_cone", "volume_sphere",
                "surface_area_cone", "surface_area_sphere")
            self.assertEqual(has_pi, expects_pi, result["operation"])

    def test_fixed_variant_constructor(self):
        for variant in RoundSolidsGenerator.VARIANTS:
            gen = RoundSolidsGenerator(variant)
            for _ in range(5):
                self.assertEqual(gen.generate()["operation"], variant)
        with self.assertRaises(ValueError):
            RoundSolidsGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
