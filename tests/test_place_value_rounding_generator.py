import unittest
import random
import sys
import os

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.place_value_rounding_generator import PlaceValueRoundingGenerator
from helpers import DELIM


class TestPlaceValueRoundingGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = PlaceValueRoundingGenerator()

    def test_rounding_format(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        # Ensure final answer parses as float or int
        try:
            float(res["final_answer"])
        except ValueError:
            self.fail("Final answer not numeric")


if __name__ == "__main__":
    unittest.main()
