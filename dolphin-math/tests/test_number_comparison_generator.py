import unittest
import sys
import os

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.number_comparison_generator import NumberComparisonGenerator
from helpers import DELIM


class TestNumberComparisonGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = NumberComparisonGenerator()

    def test_compare_correctness(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        parts = res["final_answer"].split()
        a, rel, b = float(parts[0]), parts[1], float(parts[2])
        if rel == ">":
            self.assertGreater(a, b)
        elif rel == "<":
            self.assertLess(a, b)
        else:
            self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
