import unittest
import random
import sys
import os

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.exponent_generator import (
    ExponentEvaluationGenerator,
    ExponentRulesGenerator,
    ScientificNotationGenerator,
    RootsAndRadicalsGenerator,
)
from helpers import DELIM


class TestExponentEvaluationGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = ExponentEvaluationGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "exponent_evaluation")
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)

        # Check final step
        final_step = result["steps"][-1]
        self.assertTrue(final_step.startswith(f"Z{DELIM}"))

    def test_generate_consistency(self):
        """Generate multiple examples and check consistency."""
        for _ in range(20):
            result = self.generator.generate()

            # Problem should contain 'Evaluate' and '^'
            self.assertIn("Evaluate", result["problem"])
            self.assertIn("^", result["problem"])

            # Check for exponent steps
            has_setup_step = any(s.startswith(f"EXP_SETUP{DELIM}") for s in result["steps"])
            has_expand_step = any(s.startswith(f"EXP_EXPAND{DELIM}") for s in result["steps"])

            self.assertTrue(has_setup_step, "Missing EXP_SETUP step")
            self.assertTrue(has_expand_step, "Missing EXP_EXPAND step")

            # Final answer should be a valid integer
            try:
                int(result["final_answer"])
            except ValueError:
                self.fail(f"Final answer '{result['final_answer']}' is not a valid integer")

    def test_negative_base_allowed(self):
        """Test that negative bases are generated when allowed."""
        gen = ExponentEvaluationGenerator(allow_negative_base=True)
        negative_found = False
        for _ in range(50):
            result = gen.generate()
            if "(-" in result["problem"]:
                negative_found = True
                break
        self.assertTrue(negative_found, "Should generate some problems with negative bases")

    def test_no_negative_base(self):
        """Test that no negative bases when disabled."""
        gen = ExponentEvaluationGenerator(allow_negative_base=False)
        for _ in range(20):
            result = gen.generate()
            self.assertNotIn("(-", result["problem"])


class TestExponentRulesGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = ExponentRulesGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertTrue(result["operation"].startswith("exponent_"))
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)

    def test_generate_consistency(self):
        """Generate multiple examples and check consistency."""
        for _ in range(20):
            result = self.generator.generate()

            # Problem should contain 'Simplify' or 'Evaluate'
            self.assertTrue("Simplify" in result["problem"] or "Evaluate" in result["problem"])

            # Check for rule steps
            has_setup_step = any(s.startswith(f"EXP_RULE_SETUP{DELIM}") for s in result["steps"])
            self.assertTrue(has_setup_step, "Missing EXP_RULE_SETUP step")

    def test_product_rule(self):
        """Test product rule generation."""
        gen = ExponentRulesGenerator(rule='product')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "exponent_product_rule")
            self.assertIn("·", result["problem"])

    def test_quotient_rule(self):
        """Test quotient rule generation."""
        gen = ExponentRulesGenerator(rule='quotient')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "exponent_quotient_rule")
            self.assertIn("/", result["problem"])

    def test_power_rule(self):
        """Test power rule generation."""
        gen = ExponentRulesGenerator(rule='power')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "exponent_power_rule")
            self.assertIn(")^", result["problem"])

    def test_negative_exponent_rule(self):
        """Test negative exponent rule generation."""
        gen = ExponentRulesGenerator(rule='negative')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "exponent_negative_rule")
            self.assertIn("(-", result["problem"])

    def test_zero_exponent_rule(self):
        """Test zero exponent rule generation."""
        gen = ExponentRulesGenerator(rule='zero')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "exponent_zero_rule")
            self.assertIn("^0", result["problem"])
            self.assertEqual(result["final_answer"], "1")


class TestScientificNotationGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = ScientificNotationGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertTrue(result["operation"].startswith("scientific_notation"))
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)

    def test_to_scientific(self):
        """Test conversion to scientific notation."""
        gen = ScientificNotationGenerator(problem_type='to_scientific')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "scientific_notation_convert_to")
            self.assertIn("scientific notation", result["problem"])
            self.assertIn("×", result["final_answer"])
            self.assertIn("10^", result["final_answer"])

    def test_from_scientific(self):
        """Test conversion from scientific notation."""
        gen = ScientificNotationGenerator(problem_type='from_scientific')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "scientific_notation_convert_from")
            self.assertIn("standard form", result["problem"])

    def test_multiply(self):
        """Test multiplication in scientific notation."""
        gen = ScientificNotationGenerator(problem_type='multiply')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "scientific_notation_multiply")
            self.assertIn("Multiply", result["problem"])

    def test_divide(self):
        """Test division in scientific notation."""
        gen = ScientificNotationGenerator(problem_type='divide')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "scientific_notation_divide")
            self.assertIn("Divide", result["problem"])


class TestRootsAndRadicalsGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = RootsAndRadicalsGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)

    def test_square_perfect(self):
        """Test perfect square root evaluation."""
        gen = RootsAndRadicalsGenerator(problem_type='square_perfect')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "square_root_perfect")
            self.assertIn("√", result["problem"])
            # Answer should be a simple integer
            try:
                int(result["final_answer"])
            except ValueError:
                self.fail(f"Perfect square answer should be integer, got {result['final_answer']}")

    def test_cube_perfect(self):
        """Test perfect cube root evaluation."""
        gen = RootsAndRadicalsGenerator(problem_type='cube_perfect')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "cube_root_perfect")
            self.assertIn("∛", result["problem"])
            # Answer should be a simple integer
            try:
                int(result["final_answer"])
            except ValueError:
                self.fail(f"Perfect cube answer should be integer, got {result['final_answer']}")

    def test_simplify_square(self):
        """Test simplifying square roots."""
        gen = RootsAndRadicalsGenerator(problem_type='simplify_square')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "simplify_radical")
            self.assertIn("Simplify", result["problem"])
            # Answer should be in form a√b
            self.assertIn("√", result["final_answer"])


if __name__ == '__main__':
    unittest.main()
