import unittest
import random
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.circle_generator import CircleAreaCircumferenceGenerator
from helpers import DELIM


class TestCircleAreaCircumferenceGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = CircleAreaCircumferenceGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))

    def test_generate_consistency(self):
        for _ in range(20):
            result = self.generator.generate()
            self.assertIn("circle", result["problem"].lower())
            has_setup = any(s.startswith(f"CIRCLE_SETUP{DELIM}") for s in result["steps"])
            has_formula = any(s.startswith(f"CIRCLE_FORMULA{DELIM}") for s in result["steps"])
            self.assertTrue(has_setup, "Missing CIRCLE_SETUP step")
            self.assertTrue(has_formula, "Missing CIRCLE_FORMULA step")

    def test_area_from_radius(self):
        gen = CircleAreaCircumferenceGenerator(problem_type='area_from_radius')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "circle_area")
            self.assertIn("radius", result["problem"].lower())
            self.assertIn("area", result["problem"].lower())

    def test_circumference_from_radius(self):
        gen = CircleAreaCircumferenceGenerator(problem_type='circumference_from_radius')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "circle_circumference")
            self.assertIn("circumference", result["problem"].lower())

    def test_pi_symbol_mode(self):
        gen = CircleAreaCircumferenceGenerator(use_pi_symbol=True)
        result = gen.generate()
        self.assertIn("π", result["final_answer"])

    def test_decimal_mode(self):
        gen = CircleAreaCircumferenceGenerator(use_pi_symbol=False)
        result = gen.generate()
        # Should not have π in final answer
        self.assertNotIn("π", result["final_answer"])


if __name__ == '__main__':
    unittest.main()
