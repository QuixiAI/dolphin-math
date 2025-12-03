import unittest
import sys
import os

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.two_step_inequality_generator import TwoStepInequalityGenerator
from helpers import DELIM


class TestTwoStepInequalityGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = TwoStepInequalityGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "two_step_inequality")
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
            has_simplify_step = any(s.startswith(f"INEQ_SIMPLIFY{DELIM}") for s in result["steps"])
            has_result_step = any(s.startswith(f"INEQ_RESULT{DELIM}") for s in result["steps"])

            self.assertTrue(has_setup_step, "Missing INEQ_SETUP step")
            self.assertTrue(has_simplify_step, "Missing INEQ_SIMPLIFY step")
            self.assertTrue(has_result_step, "Missing INEQ_RESULT step")

            # Should have at least 2 INEQ_OP_BOTH steps
            op_steps = [s for s in result["steps"] if s.startswith(f"INEQ_OP_BOTH{DELIM}")]
            self.assertGreaterEqual(len(op_steps), 2, "Two-step inequality should have at least 2 operations")

            # Final answer should contain a relation symbol
            has_relation = any(rel in result["final_answer"] for rel in ['<', '>', '≤', '≥'])
            self.assertTrue(has_relation, f"Final answer '{result['final_answer']}' should contain a relation symbol")

    def test_inequality_flip_with_negative(self):
        """Test that inequalities flip when dividing/multiplying by negative."""
        gen = TwoStepInequalityGenerator(include_negative_coefficient=True)
        flips_found = 0
        for _ in range(50):
            result = gen.generate()
            if any(s.startswith(f"INEQ_FLIP{DELIM}") for s in result["steps"]):
                flips_found += 1

        # Should find at least some flips
        self.assertGreater(flips_found, 0, "Should have some problems that require flipping the inequality")

    def test_standard_problem_type(self):
        """Test standard problem type (ax + b < c)."""
        gen = TwoStepInequalityGenerator(problem_type='standard')
        for _ in range(5):
            result = gen.generate()
            self.assertIn("+", result["problem"])

    def test_subtract_problem_type(self):
        """Test subtract problem type (ax - b > c)."""
        gen = TwoStepInequalityGenerator(problem_type='subtract')
        for _ in range(5):
            result = gen.generate()
            self.assertIn("-", result["problem"])

    def test_distribute_problem_type(self):
        """Test distribute problem type (a(x + b) ≤ c)."""
        gen = TwoStepInequalityGenerator(problem_type='distribute')
        for _ in range(5):
            result = gen.generate()
            self.assertIn("(", result["problem"])

    def test_fraction_problem_type(self):
        """Test fraction problem type (x/a + b ≥ c)."""
        gen = TwoStepInequalityGenerator(problem_type='fraction')
        for _ in range(5):
            result = gen.generate()
            self.assertIn("x/", result["problem"])


if __name__ == '__main__':
    unittest.main()
