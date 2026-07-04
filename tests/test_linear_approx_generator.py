import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.linear_approx_generator import LinearApproxGenerator
from generators.exponential_model_generator import dec
from helpers import DELIM


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"Use a linear approximation to estimate √(\d+)\. "
                     r"Give the answer as a fraction\.", p)
    if m:
        N = int(m.group(1))
        a = round(N ** 0.5)
        approx = a + Fraction(N - a * a, 2 * a)
        return f"√{N} ≈ {approx}"
    m = re.fullmatch(r"Use a linear approximation to estimate ∛(-?\d+)\. "
                     r"Give the answer as a fraction\.", p)
    if m:
        N = int(m.group(1))
        a = round(N ** (1 / 3))
        approx = a + Fraction(N - a ** 3, 3 * a * a)
        return f"∛{N} ≈ {approx}"
    m = re.fullmatch(r"Use a linear approximation to estimate "
                     r"\(([\d.]+)\)\^3\.", p)
    assert m, p
    x = Fraction(m.group(1))
    a = round(float(x))
    approx = a ** 3 + 3 * a * a * (x - a)
    return f"({dec(x)})^3 ≈ {dec(approx)}"


class TestLinearApproxGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LinearApproxGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_approximation_is_close_to_truth(self):
        """The linearization is within 5% of the true value."""
        for _ in range(300):
            result = self.gen.generate()
            m = re.search(r"≈ (.+)$", result["final_answer"])
            approx = float(Fraction(m.group(1)))
            p = result["problem"]
            mm = re.search(r"√(\d+)", p)
            if mm and "∛" not in p:
                true = int(mm.group(1)) ** 0.5
            elif "∛" in p:
                true = int(re.search(r"∛(-?\d+)", p).group(1)) ** (1 / 3)
            else:
                true = float(re.search(r"\(([\d.]+)\)",
                                       p).group(1)) ** 3
            self.assertLess(abs(approx - true) / abs(true), 0.05,
                            result["final_answer"])

    def test_step_arithmetic_exact(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] in ("M", "A") and len(f) == 4:
                    x, y, z = (Fraction(v) for v in f[1:])
                    got = x * y if f[0] == "M" else x + y
                    self.assertEqual(got, z, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            LinearApproxGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
