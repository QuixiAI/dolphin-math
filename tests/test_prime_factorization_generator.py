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

from generators.prime_factorization_generator import PrimeFactorizationGenerator
from helpers import DELIM


class TestPrimeFactorizationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = PrimeFactorizationGenerator()

    def test_factorization_correctness(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        n = int(res["problem"].split()[-1])
        factors = [int(p) for p in res["final_answer"].split(" × ")]
        product = prod(factors)
        self.assertEqual(product, n)
        for p in factors:
            for d in range(2, int(p ** 0.5) + 1):
                self.assertNotEqual(p % d, 0)


if __name__ == "__main__":
    unittest.main()
