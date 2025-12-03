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

from generators.multi_digit_subtraction_generator import MultiDigitSubtractionGenerator
from helpers import DELIM


class TestMultiDigitSubtractionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = MultiDigitSubtractionGenerator()

    def test_generate_output_format(self):
        res = self.generator.generate()
        for key in ["problem_id", "operation", "problem", "steps", "final_answer"]:
            self.assertIn(key, res)
        self.assertEqual(res["operation"], "multi_digit_subtraction")
        self.assertTrue(res["steps"] and res["steps"][-1].startswith(f"Z{DELIM}"))

    def test_subtraction_correctness(self):
        res = self.generator.generate()
        left, right = res["problem"].split("-")
        minuend = int(left.strip())
        subtrahend = int(right.strip())
        self.assertGreaterEqual(minuend, subtrahend)
        self.assertEqual(int(res["final_answer"]), minuend - subtrahend)

    def test_borrow_step_present_when_needed(self):
        # Force a borrow scenario with known numbers
        with patch(
            "generators.multi_digit_subtraction_generator.random.randint",
            side_effect=[1000, 999],
        ):
            res = self.generator.generate()
        borrow_steps = [s for s in res["steps"] if s.startswith(f"BORROW{DELIM}")]
        self.assertTrue(borrow_steps, "Expected borrow step for 1000 - 999")
        self.assertEqual(int(res["final_answer"]), 1)
        sub_steps = [s for s in res["steps"] if s.startswith(f"SUB_COL{DELIM}")]
        self.assertTrue(any("borrow1" in s for s in sub_steps), "Expected borrow-in reflected in SUB_COL details")


if __name__ == "__main__":
    unittest.main()
