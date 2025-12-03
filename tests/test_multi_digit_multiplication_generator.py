import unittest
import random
import sys
import os
from unittest.mock import patch

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.multi_digit_multiplication_generator import MultiDigitMultiplicationGenerator
from helpers import DELIM


class TestMultiDigitMultiplicationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = MultiDigitMultiplicationGenerator()

    def test_generate_output_format(self):
        res = self.generator.generate()
        for key in ["problem_id", "operation", "problem", "steps", "final_answer"]:
            self.assertIn(key, res)
        self.assertEqual(res["operation"], "multi_digit_multiplication")
        self.assertTrue(res["steps"] and res["steps"][-1].startswith(f"Z{DELIM}"))

    def test_multiplication_correctness_and_partials(self):
        res = self.generator.generate()
        left, right = res["problem"].split("*")
        top = int(left.strip())
        bottom = int(right.strip())
        self.assertEqual(int(res["final_answer"]), top * bottom)

        partial_steps = [s for s in res["steps"] if s.startswith(f"MUL_PARTIAL{DELIM}")]
        self.assertGreater(len(partial_steps), 0)
        add_partials_steps = [s for s in res["steps"] if s.startswith(f"ADD_PARTIALS{DELIM}")]
        self.assertEqual(len(add_partials_steps), 1)

    def test_layout_places_larger_on_top(self):
        with patch(
            "generators.multi_digit_multiplication_generator.random.randint",
            side_effect=[123, 9999],
        ):
            res = self.generator.generate()
        top, bottom = [int(x.strip()) for x in res["problem"].split("*")]
        self.assertGreaterEqual(top, bottom)


if __name__ == "__main__":
    unittest.main()
