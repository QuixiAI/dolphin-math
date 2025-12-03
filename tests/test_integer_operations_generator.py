import unittest
import random
import sys
import os

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.integer_operations_generator import IntegerOperationsGenerator
from helpers import DELIM


class TestIntegerOperationsGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = IntegerOperationsGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertTrue(result["operation"].startswith("integer_"))
        self.assertIn("problem", result)
        self.assertIsInstance(result["problem"], str)
        self.assertIn("steps", result)
        self.assertIsInstance(result["steps"], list)
        self.assertGreater(len(result["steps"]), 0)
        self.assertIn("final_answer", result)
        self.assertIsInstance(result["final_answer"], str)

        # Check final step
        final_step = result["steps"][-1]
        self.assertTrue(final_step.startswith(f"Z{DELIM}"))

    def test_generate_consistency(self):
        """Generate multiple examples and check basic consistency."""
        for _ in range(20):
            result = self.generator.generate()

            self.assertIsInstance(result, dict)
            self.assertIn("problem_id", result)
            self.assertIn("operation", result)
            self.assertIn("problem", result)
            self.assertIn("steps", result)
            self.assertIn("final_answer", result)
            self.assertGreater(len(result["steps"]), 0)
            self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))

            # Check if problem starts with 'Calculate:'
            self.assertTrue(result["problem"].startswith("Calculate:"))

            # Check for integer operation steps
            has_sign_rule = any(s.startswith(f"INT_SIGN_RULE{DELIM}") for s in result["steps"])
            self.assertTrue(has_sign_rule, "Missing INT_SIGN_RULE step")

            # Final answer should be a valid integer
            try:
                int(result["final_answer"])
            except ValueError:
                self.fail(f"Final answer '{result['final_answer']}' is not a valid integer")

    def test_addition_operation(self):
        """Test integer addition generation."""
        gen = IntegerOperationsGenerator(operation='+')
        for _ in range(10):
            result = gen.generate()
            self.assertEqual(result["operation"], "integer_addition")
            self.assertIn("+", result["problem"])

    def test_subtraction_operation(self):
        """Test integer subtraction generation."""
        gen = IntegerOperationsGenerator(operation='-')
        for _ in range(10):
            result = gen.generate()
            self.assertEqual(result["operation"], "integer_subtraction")
            self.assertIn("-", result["problem"])

    def test_multiplication_operation(self):
        """Test integer multiplication generation."""
        gen = IntegerOperationsGenerator(operation='*')
        for _ in range(10):
            result = gen.generate()
            self.assertEqual(result["operation"], "integer_multiplication")
            self.assertIn("×", result["problem"])

    def test_division_operation(self):
        """Test integer division generation."""
        gen = IntegerOperationsGenerator(operation='/')
        for _ in range(10):
            result = gen.generate()
            self.assertEqual(result["operation"], "integer_division")
            self.assertIn("÷", result["problem"])

    def test_invalid_operation(self):
        """Test that invalid operation raises error."""
        with self.assertRaises(ValueError):
            IntegerOperationsGenerator(operation='%')

    def test_negative_numbers_present(self):
        """Test that negative numbers are generated."""
        gen = IntegerOperationsGenerator()
        negative_found = False
        for _ in range(20):
            result = gen.generate()
            if "(-" in result["problem"] or "(-" in result["final_answer"]:
                negative_found = True
                break
        self.assertTrue(negative_found, "Should generate some problems with negative numbers")

    def test_sign_rules_for_multiplication(self):
        """Test that sign rules are correctly applied in multiplication."""
        gen = IntegerOperationsGenerator(operation='*')
        for _ in range(10):
            result = gen.generate()

            # Find the sign rule step
            sign_rule_step = None
            for s in result["steps"]:
                if s.startswith(f"INT_SIGN_RULE{DELIM}"):
                    sign_rule_step = s
                    break

            self.assertIsNotNone(sign_rule_step, "Should have sign rule step")
            # Should mention either same_signs or different_signs
            self.assertTrue(
                "same_signs" in sign_rule_step or "different_signs" in sign_rule_step,
                "Sign rule should mention same or different signs"
            )

    def test_sign_rules_for_division(self):
        """Test that sign rules are correctly applied in division."""
        gen = IntegerOperationsGenerator(operation='/')
        for _ in range(10):
            result = gen.generate()

            # Find the sign rule step
            sign_rule_step = None
            for s in result["steps"]:
                if s.startswith(f"INT_SIGN_RULE{DELIM}"):
                    sign_rule_step = s
                    break

            self.assertIsNotNone(sign_rule_step, "Should have sign rule step")

    def test_division_is_exact(self):
        """Test that division problems have exact integer results."""
        gen = IntegerOperationsGenerator(operation='/')
        for _ in range(20):
            result = gen.generate()
            # Final answer should be an exact integer
            answer = int(result["final_answer"])
            self.assertIsInstance(answer, int)


if __name__ == '__main__':
    unittest.main()
