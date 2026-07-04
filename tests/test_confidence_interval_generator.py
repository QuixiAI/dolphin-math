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

from generators.confidence_interval_generator import (
    ConfidenceIntervalGenerator,
)
from generators.exponential_model_generator import dec
from helpers import DELIM


def num(pattern, text):
    return Fraction(re.search(pattern, text).group(1).rstrip("."))


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    z = num(r"z\* = ([\d.]+)", p)
    if "minimum sample size" in p:
        E = num(r"margin of error of ([\d.]+)", p)
        if "proportion" in p:
            phat = num(r"p̂ = ([\d.]+)", p)
            n = math.ceil((z / E) ** 2 * phat * (1 - phat))
        else:
            sigma = num(r"σ = (\d+)", p)
            n = math.ceil((z * sigma / E) ** 2)
        return ans == str(n)
    if "margin of error for a confidence interval for the proportion" in p:
        n = int(num(r"sample of size (\d+)", p))
        E = z * (Fraction(1, 2) / math.isqrt(n))
        return ans == dec(E)
    if "margin of error for a confidence interval for the mean" in p:
        n = int(num(r"sample of size (\d+)", p))
        sigma = num(r"σ = (\d+)", p)
        return ans == dec(z * sigma / math.isqrt(n))
    # confidence interval for the mean
    n = int(num(r"sample of size (\d+)", p))
    xbar = num(r"x̄ = (\d+)", p)
    sigma = num(r"σ = (\d+)", p)
    E = z * sigma / math.isqrt(n)
    return ans == f"({dec(xbar - E)}, {dec(xbar + E)})"


class TestConfidenceIntervalGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ConfidenceIntervalGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: recompute each answer from the givens."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_critical_value_in_problem(self):
        """Principle 5: z* is always supplied in the text."""
        for _ in range(300):
            result = self.gen.generate()
            self.assertRegex(result["problem"], r"z\* = [\d.]+")

    def test_sample_sizes_are_integers(self):
        for v in ("sample_size_mean", "sample_size_prop"):
            gen = ConfidenceIntervalGenerator(v)
            for _ in range(100):
                result = gen.generate()
                self.assertRegex(result["final_answer"], r"^\d+$")
                self.assertTrue(any(s.startswith(f"CEIL{DELIM}")
                                    for s in result["steps"]))

    def test_pipe_safe_and_exact(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)
                self.assertNotIn("...", s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 5)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ConfidenceIntervalGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
