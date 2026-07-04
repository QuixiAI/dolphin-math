import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.geometric_distribution_generator import (
    GeometricDistributionGenerator, exact,
)
from helpers import DELIM


def oracle_answer(example):
    """A9 oracle: recompute the geometric quantity from the prompt."""
    problem = example["problem"]
    p = Fraction(re.search(r"p = (\d+/\d+)", problem).group(1))
    q = 1 - p
    m = re.search(r"Find P\(X = (\d+)\)", problem)
    if m:
        k = int(m.group(1))
        return exact((q ** (k - 1)) * p)
    m = re.search(r"Find P\(X <= (\d+)\)", problem)
    if m:
        k = int(m.group(1))
        return exact(1 - q ** k)
    m = re.search(r"Find P\(X > (\d+)\)", problem)
    if m:
        k = int(m.group(1))
        return exact(q ** k)
    return exact(1 / p)


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        code = parts[0]
        if code == "POW":
            base_txt, exponent_txt = re.fullmatch(
                r"\((\d+/\d+|\d+(?:\.\d+)?)\)\^(\d+)", parts[1]
            ).groups()
            if exact(Fraction(base_txt) ** int(exponent_txt)) != parts[2]:
                return False
        elif code == "M":
            if exact(Fraction(parts[1]) * Fraction(parts[2])) != parts[3]:
                return False
        elif code == "S":
            if exact(Fraction(parts[1]) - Fraction(parts[2])) != parts[3]:
                return False
        elif code == "D":
            if exact(Fraction(parts[1]) / Fraction(parts[2])) != parts[3]:
                return False
    return True


class TestGeometricDistributionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GeometricDistributionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
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

    def test_probabilities_valid(self):
        for variant in ("exact_k", "at_most", "after_k"):
            gen = GeometricDistributionGenerator(variant)
            for _ in range(100):
                result = gen.generate()
                val = float(Fraction(result["final_answer"]))
                self.assertGreaterEqual(val, 0)
                self.assertLessEqual(val, 1)

    def test_formula_present(self):
        for variant in GeometricDistributionGenerator.VARIANTS:
            result = GeometricDistributionGenerator(variant).generate()
            self.assertTrue(any(s.startswith(f"GEOM_FORMULA{DELIM}")
                                for s in result["steps"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            GeometricDistributionGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
