import unittest
import random
import sys
import os
from math import prod

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.factors_generator import FactorsGenerator
from helpers import DELIM


class TestFactorsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = FactorsGenerator()

    def test_format_and_correctness(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        n = int(res["problem"].split()[-1])
        factors = [int(f.strip()) for f in res["final_answer"].split(",")]
        for f in factors:
            self.assertEqual(n % f, 0)


if __name__ == "__main__":
    unittest.main()
