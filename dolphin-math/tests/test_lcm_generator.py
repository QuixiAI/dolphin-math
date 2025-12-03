import unittest
import sys
import os
from math import gcd

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.lcm_generator import LCMGenerator
from helpers import DELIM


class TestLCMGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = LCMGenerator()

    def test_lcm_correctness(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        # Problem string: "Find LCM of {a} and {b}"
        parts = res["problem"].split()
        a_str, b_str = parts[-3], parts[-1]
        a = int(a_str)
        b = int(b_str)
        g = gcd(a, b)
        expected = abs(a * b) // g if g else 0
        self.assertEqual(int(res["final_answer"]), expected)


if __name__ == "__main__":
    unittest.main()
