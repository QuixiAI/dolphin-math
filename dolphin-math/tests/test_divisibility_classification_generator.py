import unittest
import sys
import os
import random
from math import isqrt

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.divisibility_classification_generator import DivisibilityClassificationGenerator
from helpers import DELIM


class TestDivisibilityClassificationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Use seed for deterministic tests
        self.gen = DivisibilityClassificationGenerator()

    def test_classification_correctness(self):
        # Run multiple tests to verify correctness across different numbers
        for _ in range(10):
            res = self.gen.generate()
            self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
            n = int(res["problem"].split()[1])
            answer = res["final_answer"]
            # Simple primality check
            prime = True
            for d in range(2, isqrt(n) + 1):
                if n % d == 0:
                    prime = False
                    break
            if prime:
                self.assertEqual(answer, "prime", f"Number {n} should be prime")
            else:
                self.assertEqual(answer, "composite", f"Number {n} should be composite")


if __name__ == "__main__":
    unittest.main()
