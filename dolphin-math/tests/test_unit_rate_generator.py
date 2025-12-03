import unittest
import sys
import os

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.unit_rate_generator import UnitRateGenerator, UnitRateFromTableGenerator
from helpers import DELIM


class TestUnitRateGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = UnitRateGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "unit_rate")
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
            self.assertIn("problem_id", result)
            self.assertIn("operation", result)
            self.assertIn("problem", result)
            self.assertIn("steps", result)
            self.assertIn("final_answer", result)

            # Problem should ask about cost/time per unit
            self.assertTrue("1 " in result["problem"] or "1 " in result["final_answer"])

            # Check for unit rate steps
            has_setup_step = any(s.startswith(f"UNIT_RATE_SETUP{DELIM}") for s in result["steps"])
            has_div_step = any(s.startswith(f"UNIT_RATE_DIV{DELIM}") for s in result["steps"])
            self.assertTrue(has_setup_step, "Missing UNIT_RATE_SETUP step")
            self.assertTrue(has_div_step, "Missing UNIT_RATE_DIV step")


class TestUnitRateFromTableGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = UnitRateFromTableGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "unit_rate_table")
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)

        # Final answer should be a valid integer
        try:
            int(result["final_answer"])
        except ValueError:
            self.fail(f"Final answer '{result['final_answer']}' is not a valid integer")

    def test_generate_consistency(self):
        """Generate multiple examples and check consistency."""
        for _ in range(10):
            result = self.generator.generate()

            # Check for table-specific steps
            has_table_step = any(s.startswith(f"UNIT_RATE_TABLE{DELIM}") for s in result["steps"])
            self.assertTrue(has_table_step, "Missing UNIT_RATE_TABLE step")


if __name__ == '__main__':
    unittest.main()
