import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.compound_probability_generator import (
    CompoundProbabilityIndependentGenerator,
    CompoundProbabilityDependentGenerator,
)
from helpers import DELIM


class TestCompoundProbabilityIndependentGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = CompoundProbabilityIndependentGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "compound_probability_independent")
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))

    def test_generate_consistency(self):
        for _ in range(20):
            result = self.generator.generate()
            has_setup = any(s.startswith(f"PROB_SETUP{DELIM}") for s in result["steps"])
            has_independent = any(s.startswith(f"PROB_INDEPENDENT{DELIM}") for s in result["steps"])
            has_multiply = any(s.startswith(f"PROB_MULTIPLY{DELIM}") for s in result["steps"])

            self.assertTrue(has_setup, "Missing PROB_SETUP step")
            self.assertTrue(has_independent, "Missing PROB_INDEPENDENT step")
            self.assertTrue(has_multiply, "Missing PROB_MULTIPLY step")

    def test_answer_is_fraction(self):
        for _ in range(10):
            result = self.generator.generate()
            # Answer should be in fraction form (contains /)
            self.assertIn("/", result["final_answer"])


class TestCompoundProbabilityDependentGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = CompoundProbabilityDependentGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "compound_probability_dependent")

    def test_generate_consistency(self):
        for _ in range(20):
            result = self.generator.generate()
            has_setup = any(s.startswith(f"PROB_SETUP{DELIM}") for s in result["steps"])
            has_dependent = any(s.startswith(f"PROB_DEPENDENT{DELIM}") for s in result["steps"])
            has_conditional = any(s.startswith(f"PROB_CONDITIONAL{DELIM}") for s in result["steps"])

            self.assertTrue(has_setup, "Missing PROB_SETUP step")
            self.assertTrue(has_dependent, "Missing PROB_DEPENDENT step")
            self.assertTrue(has_conditional, "Missing PROB_CONDITIONAL step")

    def test_without_replacement_context(self):
        """Test that problems mention 'without replacement'."""
        for _ in range(10):
            result = self.generator.generate()
            self.assertIn("without replacement", result["problem"].lower())


if __name__ == '__main__':
    unittest.main()
