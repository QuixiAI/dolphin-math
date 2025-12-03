import unittest
import random
import sys
import os

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.scaling_generator import ScalingGenerator, SimilarFiguresScaleGenerator
from helpers import DELIM


class TestScalingGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = ScalingGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertIn(result["operation"], ["scale_find_actual", "scale_find_scaled"])
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
            self.assertIn("operation", result)

            # Problem should mention scale
            self.assertIn("scale", result["problem"].lower())

            # Check for scale steps
            has_setup_step = any(s.startswith(f"SCALE_SETUP{DELIM}") for s in result["steps"])
            self.assertTrue(has_setup_step, "Missing SCALE_SETUP step")

    def test_find_actual_problems(self):
        """Test that find_actual problems multiply correctly."""
        for _ in range(10):
            result = self.generator.generate()
            if result["operation"] == "scale_find_actual":
                # Should have SCALE_MULT step
                has_mult_step = any(s.startswith(f"SCALE_MULT{DELIM}") for s in result["steps"])
                self.assertTrue(has_mult_step, "Missing SCALE_MULT step for find_actual problem")

    def test_find_scaled_problems(self):
        """Test that find_scaled problems divide correctly."""
        for _ in range(10):
            result = self.generator.generate()
            if result["operation"] == "scale_find_scaled":
                # Should have SCALE_DIV step
                has_div_step = any(s.startswith(f"SCALE_DIV{DELIM}") for s in result["steps"])
                self.assertTrue(has_div_step, "Missing SCALE_DIV step for find_scaled problem")


class TestSimilarFiguresScaleGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = SimilarFiguresScaleGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertIn(result["operation"], ["similar_scale_factor", "similar_missing_side"])
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)

    def test_generate_consistency(self):
        """Generate multiple examples and check consistency."""
        for _ in range(10):
            result = self.generator.generate()

            # Problem should mention similar figures
            self.assertIn("similar", result["problem"].lower())

            # Check for similar figures steps
            has_setup_step = any(s.startswith(f"SIMILAR_SETUP{DELIM}") for s in result["steps"])
            has_scale_step = any(s.startswith(f"SIMILAR_SCALE{DELIM}") for s in result["steps"])
            self.assertTrue(has_setup_step, "Missing SIMILAR_SETUP step")
            self.assertTrue(has_scale_step, "Missing SIMILAR_SCALE step")


if __name__ == '__main__':
    unittest.main()
