import unittest
import random
import sys
import os
from math import gcd

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.gcf_generator import GCFGenerator
from helpers import DELIM


class TestGCFGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = GCFGenerator()

    def test_gcf_correctness(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        parts = res["problem"].split()
        a = int(parts[-3])
        b = int(parts[-1])
        self.assertEqual(int(res["final_answer"]), gcd(a, b))


if __name__ == "__main__":
    unittest.main()
