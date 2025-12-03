import unittest
import sys
import os

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.one_step_inequality_generator import OneStepInequalityGenerator
from helpers import DELIM


class TestOneStepInequalityGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = OneStepInequalityGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "one_step_inequality")
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

            # Problem should contain 'Solve the inequality'
            self.assertIn("Solve the inequality", result["problem"])

            # Check for inequality steps
            has_setup_step = any(s.startswith(f"INEQ_SETUP{DELIM}") for s in result["steps"])
            has_op_step = any(s.startswith(f"INEQ_OP_BOTH{DELIM}") for s in result["steps"])
            has_result_step = any(s.startswith(f"INEQ_RESULT{DELIM}") for s in result["steps"])

            self.assertTrue(has_setup_step, "Missing INEQ_SETUP step")
            self.assertTrue(has_op_step, "Missing INEQ_OP_BOTH step")
            self.assertTrue(has_result_step, "Missing INEQ_RESULT step")

            # Final answer should contain a relation symbol
            has_relation = any(rel in result["final_answer"] for rel in ['<', '>', '≤', '≥'])
            self.assertTrue(has_relation, f"Final answer '{result['final_answer']}' should contain a relation symbol")

    def test_inequality_flip_with_negative(self):
        """Test that inequalities flip when dividing/multiplying by negative."""
        gen = OneStepInequalityGenerator(include_negative_coefficient=True)
        flips_found = 0
        for _ in range(50):
            result = gen.generate()
            if any(s.startswith(f"INEQ_FLIP{DELIM}") for s in result["steps"]):
                flips_found += 1

        # Should find at least some flips
        self.assertGreater(flips_found, 0, "Should have some problems that require flipping the inequality")

    def test_no_flip_without_negative(self):
        """Test that no flips occur without negative coefficients."""
        gen = OneStepInequalityGenerator(include_negative_coefficient=False)
        for _ in range(20):
            result = gen.generate()
            has_flip = any(s.startswith(f"INEQ_FLIP{DELIM}") for s in result["steps"])
            self.assertFalse(has_flip, "Should not have flip step when negative coefficients are disabled")

    def test_addition_operation(self):
        """Test addition inequality generation."""
        gen = OneStepInequalityGenerator(operation='+')
        for _ in range(5):
            result = gen.generate()
            self.assertIn("+", result["problem"])

    def test_subtraction_operation(self):
        """Test subtraction inequality generation."""
        gen = OneStepInequalityGenerator(operation='-')
        for _ in range(5):
            result = gen.generate()
            self.assertIn("-", result["problem"])


if __name__ == '__main__':
    unittest.main()
