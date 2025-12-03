import unittest
import sys
import os
import random

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.multi_digit_addition_generator import MultiDigitAdditionGenerator
from helpers import DELIM


class TestMultiDigitAdditionGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = MultiDigitAdditionGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        for key in ["problem_id", "operation", "problem", "steps", "final_answer"]:
            self.assertIn(key, result)

        self.assertEqual(result["operation"], "multi_digit_addition")
        self.assertIsInstance(result["problem"], str)
        self.assertIsInstance(result["steps"], list)
        self.assertGreater(len(result["steps"]), 0)

        final_step = result["steps"][-1]
        self.assertTrue(final_step.startswith(f"Z{DELIM}"))
        self.assertEqual(final_step.split(DELIM)[1], result["final_answer"])

    def test_addition_correctness_and_columns(self):
        random.seed(123)
        for _ in range(10):
            res = self.generator.generate()
            # Validate numeric sum
            problem_str = res["problem"]
            left, right = problem_str.split("+")
            num1 = int(left.strip())
            num2 = int(right.strip())
            self.assertEqual(int(res["final_answer"]), num1 + num2)

            # Check column steps and final carry consistency
            add_steps = [s for s in res["steps"] if s.startswith(f"ADD_COL{DELIM}")]
            self.assertGreater(len(add_steps), 0)
            # Optional: ensure carry final matches overflow
            carry_steps = [s for s in res["steps"] if s.startswith(f"CARRY_FINAL{DELIM}")]
            if num1 + num2 >= 10 ** len(str(max(num1, num2))):
                self.assertTrue(carry_steps, "Expect final carry when result has extra digit")


if __name__ == "__main__":
    unittest.main()
