import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.five_number_summary_generator import (
    FiveNumberSummaryGenerator,
)
from generators.exponential_model_generator import dec
from helpers import DELIM


def five(data):
    """Independent five-number summary (median-exclusive halves)."""
    s = sorted(data)
    n = len(s)
    med = (Fraction(s[n // 2]) if n % 2
           else Fraction(s[n // 2 - 1] + s[n // 2], 2))
    lo = s[:n // 2]
    hi = s[(n + 1) // 2:]
    q1 = lo[len(lo) // 2]
    q3 = hi[len(hi) // 2]
    return s[0], q1, med, q3, s[-1]


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    data = [int(v) for v in
            re.search(r"data set: (.+)\.$", p).group(1).split(", ")]
    mn, q1, med, q3, mx = five(data)
    if p.startswith("Find the five-number summary"):
        return ans == (f"min = {mn}, Q1 = {q1}, median = {dec(med)}, "
                       f"Q3 = {q3}, max = {mx}")
    if p.startswith("Find the interquartile range"):
        return ans == str(q3 - q1)
    iqr = q3 - q1
    lo_f = q1 - Fraction(3, 2) * iqr
    hi_f = q3 + Fraction(3, 2) * iqr
    outs = [v for v in sorted(data) if v < lo_f or v > hi_f]
    want = ", ".join(map(str, outs)) if outs else "none"
    return ans == want


class TestFiveNumberSummaryGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FiveNumberSummaryGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_recompute_from_problem(self):
        """A9 oracle: recompute the summary from the problem text."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_quartiles_are_data_points(self):
        for _ in range(200):
            result = self.gen.generate()
            data = [int(v) for v in
                    re.search(r"data set: (.+)\.$",
                              result["problem"]).group(1).split(", ")]
            for s in result["steps"]:
                if s.startswith(f"QUARTILE{DELIM}"):
                    self.assertIn(int(s.split(DELIM)[3]), data)

    def test_outliers_both_outcomes_occur(self):
        gen = FiveNumberSummaryGenerator("outliers")
        answers = [gen.generate()["final_answer"] for _ in range(100)]
        self.assertIn("none", answers)
        self.assertTrue(any(a != "none" for a in answers))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            FiveNumberSummaryGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
