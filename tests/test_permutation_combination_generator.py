import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.permutation_combination_generator import (
    PermutationCombinationGenerator,
)
from helpers import DELIM


def oracle_check(example):
    """A9 oracle: recompute the count from the problem text."""
    p = example["problem"]
    ans = int(example["final_answer"])
    m = re.fullmatch(r"Evaluate (\d+)!\.", p)
    if m:
        return ans == math.factorial(int(m.group(1)))
    m = re.search(r"Compute P\((\d+), (\d+)\)", p)
    if m:
        return ans == math.perm(int(m.group(1)), int(m.group(2)))
    m = re.search(r"Compute C\((\d+), (\d+)\)", p)
    if m:
        return ans == math.comb(int(m.group(1)), int(m.group(2)))
    m = re.search(r"(\d+) people be seated .* group of (\d+)", p)
    if m:
        return ans == math.perm(int(m.group(2)), int(m.group(1)))
    m = re.search(r"committee of (\d+) be chosen from a group of (\d+)",
                  p)
    return ans == math.comb(int(m.group(2)), int(m.group(1)))


class TestPermutationCombinationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PermutationCombinationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: math.factorial / perm / comb agree with each answer."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_running_products_are_correct(self):
        """Every M step's product equals its two factors multiplied."""
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                if s.startswith(f"M{DELIM}"):
                    _, a, b, c = s.split(DELIM)
                    self.assertEqual(int(a) * int(b), int(c), s)

    def test_word_identifies_order(self):
        gen = PermutationCombinationGenerator("word")
        kinds = set()
        for _ in range(200):
            result = gen.generate()
            ident = next(s for s in result["steps"]
                         if s.startswith(f"IDENTIFY{DELIM}"))
            kinds.add(ident.split(DELIM)[2])
        self.assertEqual(kinds, {"use P(n, r)", "use C(n, r)"})

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
            PermutationCombinationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
