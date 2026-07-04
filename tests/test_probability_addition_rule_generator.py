import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.probability_addition_rule_generator import (
    ProbabilityAdditionRuleGenerator, exact,
)
from helpers import DELIM


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    if "fair die is rolled" in p:
        sets = re.findall(r"\[([\d, ]+)\]", p)
        sa = {int(v) for v in sets[0].split(", ")}
        sb = {int(v) for v in sets[1].split(", ")}
        return ans == exact(Fraction(len(sa | sb), 6))
    pa = re.search(r"P\(A\) = (\d+)/(\d+)", p)
    a, D = int(pa.group(1)), int(pa.group(2))
    b = int(re.search(r"P\(B\) = (\d+)/\d+", p).group(1))
    if "mutually exclusive" in p:
        return ans == exact(Fraction(a + b, D))
    m = re.search(r"P\(A and B\) = (\d+)/\d+", p)
    if m and "Find P(A or B)" in p:
        c = int(m.group(1))
        return ans == exact(Fraction(a + b - c, D))
    u = int(re.search(r"P\(A or B\) = (\d+)/\d+", p).group(1))
    return ans == exact(Fraction(a + b - u, D))


class TestProbabilityAdditionRuleGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ProbabilityAdditionRuleGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: recompute the probability from the givens."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_probabilities_valid(self):
        for _ in range(400):
            result = self.gen.generate()
            val = float(Fraction(result["final_answer"]))
            self.assertGreaterEqual(val, 0)
            self.assertLessEqual(val, 1)

    def test_formula_present(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"ADD_FORMULA{DELIM}")
                                for s in result["steps"]))

    def test_mutually_exclusive_notes_zero(self):
        gen = ProbabilityAdditionRuleGenerator("mutually_exclusive")
        for _ in range(100):
            result = gen.generate()
            self.assertTrue(any("P(A ∩ B) = 0" in s
                                for s in result["steps"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ProbabilityAdditionRuleGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
