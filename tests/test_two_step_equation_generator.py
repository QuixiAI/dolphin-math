import unittest
import random
import sys
import os

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.two_step_equation_generator import TwoStepEquationGenerator
from helpers import DELIM


class TestTwoStepEquationGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = TwoStepEquationGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "two_step_equation")
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
            has_simplify_step = any(s.startswith(f"EQ_SIMPLIFY{DELIM}") for s in result["steps"])
            has_result_step = any(s.startswith(f"EQ_RESULT{DELIM}") for s in result["steps"])

            self.assertTrue(has_setup_step, "Missing EQ_SETUP step")
            self.assertTrue(has_simplify_step, "Missing EQ_SIMPLIFY step")
            self.assertTrue(has_result_step, "Missing EQ_RESULT step")

            # Should have at least 2 EQ_OP_BOTH steps (two-step equation)
            op_steps = [s for s in result["steps"] if s.startswith(f"EQ_OP_BOTH{DELIM}")]
            self.assertGreaterEqual(len(op_steps), 2, "Two-step equation should have at least 2 operations")

            # Final answer should be a valid integer
            try:
                int(result["final_answer"])
            except ValueError:
                self.fail(f"Final answer '{result['final_answer']}' is not a valid integer")

    def test_standard_problem_type(self):
        """Test standard problem type (ax + b = c)."""
        gen = TwoStepEquationGenerator(problem_type='standard')
        for _ in range(5):
            result = gen.generate()
            # Should have + in the equation
            self.assertIn("+", result["problem"])

    def test_subtract_problem_type(self):
        """Test subtract problem type (ax - b = c)."""
        gen = TwoStepEquationGenerator(problem_type='subtract')
        for _ in range(5):
            result = gen.generate()
            # Should have - in the equation
            self.assertIn("-", result["problem"])

    def test_distribute_problem_type(self):
        """Test distribute problem type (a(x + b) = c)."""
        gen = TwoStepEquationGenerator(problem_type='distribute')
        for _ in range(5):
            result = gen.generate()
            # Should have parentheses
            self.assertIn("(", result["problem"])

    def test_fraction_problem_type(self):
        """Test fraction problem type (x/a + b = c)."""
        gen = TwoStepEquationGenerator(problem_type='fraction')
        for _ in range(5):
            result = gen.generate()
            # Should have x/
            self.assertIn("x/", result["problem"])


if __name__ == '__main__':
    unittest.main()
