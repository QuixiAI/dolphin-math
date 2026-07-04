import unittest
import sys
import os
import random
from fractions import Fraction # Needed for checking final answer type

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.linear_simple_generator import LinearSimpleGenerator
from helpers import DELIM

class TestLinearSimpleGenerator(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.generator = LinearSimpleGenerator()
        # random.seed(46) # Optional: for predictable tests

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "linear_eq_simple")
        self.assertIn("problem", result)
        self.assertIsInstance(result["problem"], str)
        self.assertIn("steps", result)
        self.assertIsInstance(result["steps"], list)
        self.assertGreater(len(result["steps"]), 0, "Steps list should not be empty")
        self.assertIn("final_answer", result)
        self.assertIsInstance(result["final_answer"], str)

        # Check the final step format
        final_step = result["steps"][-1]
        self.assertTrue(final_step.startswith(f"Z{DELIM}"), f"Final step should start with Z{DELIM}")
        # Check if final answer in step matches the final_answer field
        self.assertEqual(final_step.split(DELIM)[1], result["final_answer"])

    def test_generate_consistency(self):
        """Generate multiple examples and check basic consistency."""
        for _ in range(10): # Generate a few examples
            result = self.generator.generate()
            # Re-run basic format checks
            self.assertIsInstance(result, dict)
            self.assertIn("problem_id", result)
            self.assertIn("operation", result)
            self.assertIn("problem", result)
            self.assertIn("steps", result)
            self.assertIn("final_answer", result)
            self.assertGreater(len(result["steps"]), 0)
            self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
            self.assertEqual(result["steps"][-1].split(DELIM)[1], result["final_answer"])

            # Check if problem string looks reasonable
            self.assertIn("Solve", result["problem"])
            self.assertIn("=", result["problem"])
            self.assertIn("x", result["problem"])

            # Check if final answer looks reasonable (starts with x=)
            # A0 convention: single solutions are bare values (no x= prefix)
            self.assertFalse(result["final_answer"].startswith("x="))
            # Check the bare answer is a valid fraction string
            try:
                Fraction(result["final_answer"])
            except (ValueError, ZeroDivisionError):
                self.fail(f"Final answer '{result['final_answer']}' is not a valid Fraction string.")


    def test_oracle_solves_equation_from_problem_text(self):
        """A9 oracle: parse both sides as a*x+b and solve exactly."""
        import re
        from fractions import Fraction

        def parse_side(text):
            text = text.replace(" ", "")
            a = b = Fraction(0)
            for tok in re.findall(r"[+-]?[^+-]+", text):
                if tok.endswith("x"):
                    c = tok[:-1]
                    a += Fraction(1 if c in ("", "+")
                                  else -1 if c == "-" else int(c))
                else:
                    b += Fraction(tok)
            return a, b

        for _ in range(500):
            result = self.generator.generate()
            eq = result["problem"].replace("Solve: ", "").replace("Solve ", "")
            lhs, rhs = eq.split(" = ")
            a1, b1 = parse_side(lhs)
            a2, b2 = parse_side(rhs)
            self.assertNotEqual(a1, a2, eq)
            expected = (b2 - b1) / (a1 - a2)
            self.assertEqual(Fraction(result["final_answer"]), expected, eq)


if __name__ == '__main__':
    unittest.main()
