import unittest
import sys
import os

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.one_step_equation_generator import OneStepEquationGenerator
from helpers import DELIM


class TestOneStepEquationGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = OneStepEquationGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertTrue(result["operation"].startswith("one_step_equation"))
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

            # Problem should contain 'Solve for x'
            self.assertIn("Solve for x", result["problem"])

            # Check for equation steps
            has_setup_step = any(s.startswith(f"EQ_SETUP{DELIM}") for s in result["steps"])
            has_op_step = any(s.startswith(f"EQ_OP_BOTH{DELIM}") for s in result["steps"])
            has_result_step = any(s.startswith(f"EQ_RESULT{DELIM}") for s in result["steps"])

            self.assertTrue(has_setup_step, "Missing EQ_SETUP step")
            self.assertTrue(has_op_step, "Missing EQ_OP_BOTH step")
            self.assertTrue(has_result_step, "Missing EQ_RESULT step")

            # Final answer should be a valid integer
            try:
                int(result["final_answer"])
            except ValueError:
                self.fail(f"Final answer '{result['final_answer']}' is not a valid integer")

    def test_addition_operation(self):
        """Test addition equation generation."""
        gen = OneStepEquationGenerator(operation='+')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "one_step_equation_add")
            self.assertIn("+", result["problem"])

    def test_subtraction_operation(self):
        """Test subtraction equation generation."""
        gen = OneStepEquationGenerator(operation='-')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "one_step_equation_sub")
            self.assertIn("-", result["problem"])

    def test_multiplication_operation(self):
        """Test multiplication equation generation."""
        gen = OneStepEquationGenerator(operation='*')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "one_step_equation_mult")
            self.assertIn("x =", result["problem"])

    def test_division_operation(self):
        """Test division equation generation."""
        gen = OneStepEquationGenerator(operation='/')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "one_step_equation_div")
            self.assertIn("/", result["problem"])

    def test_no_negative_solutions(self):
        """Test with negative solutions disabled."""
        gen = OneStepEquationGenerator(allow_negative=False)
        for _ in range(20):
            result = gen.generate()
            answer = int(result["final_answer"])
            self.assertGreater(answer, 0, "Answer should be positive when allow_negative=False")


if __name__ == '__main__':
    unittest.main()
