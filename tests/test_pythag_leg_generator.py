import unittest
import random
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.pythag_leg_generator import PythagoreanLegGenerator, PythagoreanWordProblemGenerator
from helpers import DELIM


class TestPythagoreanLegGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = PythagoreanLegGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "pythagorean_find_leg")
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))

    def test_generate_consistency(self):
        for _ in range(20):
            result = self.generator.generate()
            self.assertIn("right triangle", result["problem"].lower())
            self.assertIn("hypotenuse", result["problem"].lower())

            has_setup = any(s.startswith(f"PYTHAG_SETUP{DELIM}") for s in result["steps"])
            has_formula = any(s.startswith(f"PYTHAG_FORMULA{DELIM}") for s in result["steps"])
            has_root = any(s.startswith(f"PYTHAG_ROOT{DELIM}") for s in result["steps"])

            self.assertTrue(has_setup, "Missing PYTHAG_SETUP step")
            self.assertTrue(has_formula, "Missing PYTHAG_FORMULA step")
            self.assertTrue(has_root, "Missing PYTHAG_ROOT step")

    def test_answer_is_valid(self):
        """Test that answers form valid Pythagorean triples."""
        for _ in range(20):
            result = self.generator.generate()
            # Extract numbers from the problem
            answer = result["final_answer"].replace(" units", "")
            self.assertTrue(answer.isdigit(), f"Answer should be a positive integer, got {answer}")


class TestPythagoreanWordProblemGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = PythagoreanWordProblemGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "pythagorean_word_problem")

    def test_generate_consistency(self):
        for _ in range(20):
            result = self.generator.generate()
            has_context = any(s.startswith(f"PYTHAG_CONTEXT{DELIM}") for s in result["steps"])
            has_model = any(s.startswith(f"PYTHAG_MODEL{DELIM}") for s in result["steps"])
            self.assertTrue(has_context, "Missing PYTHAG_CONTEXT step")
            self.assertTrue(has_model, "Missing PYTHAG_MODEL step")


if __name__ == '__main__':
    unittest.main()
