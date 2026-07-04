import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.composite_arithmetic_generator import (
    CompositeArithmeticGenerator,
)
from helpers import DELIM


def oracle_check(example):
    """A9 oracle: recompute each answer from the problem text alone."""
    p = example["problem"]
    ans = example["final_answer"]
    m = re.fullmatch(r"Find the mean of these test scores: (.+)\.", p)
    if m:
        vals = [int(v) for v in m.group(1).split(", ")]
        mean = Fraction(sum(vals), len(vals))
        return mean.denominator == 1 and ans == str(mean.numerator)
    m = re.fullmatch(r"A rectangle measures (\d+) (\d+)/(\d+) feet by "
                     r"(\d+) (\d+)/(\d+) feet\. Find its area\.", p)
    if m:
        w1, n1, d1, w2, n2, d2 = (int(x) for x in m.groups())
        area = Fraction(w1 * d1 + n1, d1) * Fraction(w2 * d2 + n2, d2)
        val = ans.replace(" square feet", "")
        mm = re.fullmatch(r"(\d+) (\d+)/(\d+)", val)
        if mm:
            w, nn, dd = (int(x) for x in mm.groups())
            got = w + Fraction(nn, dd)
        elif "/" in val:
            got = Fraction(val)
        else:
            got = Fraction(int(val))
        return got == area and val.endswith("feet") is False
    m = re.fullmatch(r"A bill has items costing (.+)\. Leave a "
                     r"(\d+)% tip on the total\. How much is the "
                     r"tip\?", p)
    assert m, p
    items = [int(v.lstrip("$")) for v in m.group(1).split(", ")]
    pct = int(m.group(2))
    tip = Fraction(sum(items) * pct, 100)
    dollars = int(tip)
    cents = int((tip - dollars) * 100)
    return ans == f"${dollars}.{cents:02d}"


class TestCompositeArithmeticGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CompositeArithmeticGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_recompute_from_problem(self):
        """A9 oracle: every composite answer recomputed independently."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_metadata_emitted(self):
        for _ in range(50):
            result = self.gen.generate()
            self.assertEqual(result["grade_level"], "elementary")
            self.assertEqual(result["difficulty"], 4)

    def test_chains_multiple_skills(self):
        """Each scratchpad opens with the plan and uses >=2 skills."""
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(result["steps"][0]
                            .startswith(f"COMPOSITE_SETUP{DELIM}"))
            codes = {s.split(DELIM)[0] for s in result["steps"]}
            # setup + at least two distinct working codes + Z
            self.assertGreaterEqual(len(codes), 4, result["steps"])

    def test_mean_uses_long_division(self):
        gen = CompositeArithmeticGenerator("mean_long_division")
        for _ in range(100):
            result = gen.generate()
            self.assertTrue(any(s.startswith(f"D{DELIM}")
                                for s in result["steps"]))
            self.assertTrue(any(s.startswith(f"BRING_DOWN{DELIM}")
                                for s in result["steps"]))

    def test_pipe_safety(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 5, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            CompositeArithmeticGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
