import unittest
import random
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.statistics_generator import (
    MeanGenerator,
    MedianGenerator,
    ModeGenerator,
    RangeGenerator,
    MeanAbsoluteDeviationGenerator,
)
from helpers import DELIM


class TestMeanGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = MeanGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "mean")
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)

    def test_generate_consistency(self):
        for _ in range(20):
            result = self.generator.generate()
            self.assertIn("mean", result["problem"].lower())
            has_sum = any(s.startswith(f"STAT_SUM{DELIM}") for s in result["steps"])
            has_count = any(s.startswith(f"STAT_COUNT{DELIM}") for s in result["steps"])
            has_divide = any(s.startswith(f"STAT_DIVIDE{DELIM}") for s in result["steps"])
            self.assertTrue(has_sum)
            self.assertTrue(has_count)
            self.assertTrue(has_divide)


class TestMedianGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = MedianGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["operation"], "median")

    def test_odd_count(self):
        gen = MedianGenerator(force_odd=True)
        for _ in range(10):
            result = gen.generate()
            # Should not have average step for odd count
            has_order = any(s.startswith(f"STAT_ORDER{DELIM}") for s in result["steps"])
            self.assertTrue(has_order)

    def test_even_count(self):
        gen = MedianGenerator(force_odd=False)
        for _ in range(10):
            result = gen.generate()
            has_average = any(s.startswith(f"STAT_AVERAGE{DELIM}") for s in result["steps"])
            self.assertTrue(has_average, "Even count should have average step")


class TestModeGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = ModeGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("mode", result["operation"])

    def test_unimodal(self):
        gen = ModeGenerator(mode_type='unimodal')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "mode")
            # Answer should be a single number
            self.assertTrue(result["final_answer"].isdigit())

    def test_bimodal(self):
        gen = ModeGenerator(mode_type='bimodal')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "mode_bimodal")
            self.assertIn("and", result["final_answer"])

    def test_no_mode(self):
        gen = ModeGenerator(mode_type='no_mode')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "mode_none")
            self.assertEqual(result["final_answer"], "No mode")


class TestRangeGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = RangeGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["operation"], "range")

    def test_generate_consistency(self):
        for _ in range(10):
            result = self.generator.generate()
            self.assertIn("range", result["problem"].lower())
            has_min = any(s.startswith(f"STAT_MIN{DELIM}") for s in result["steps"])
            has_max = any(s.startswith(f"STAT_MAX{DELIM}") for s in result["steps"])
            has_range = any(s.startswith(f"STAT_RANGE{DELIM}") for s in result["steps"])
            self.assertTrue(has_min)
            self.assertTrue(has_max)
            self.assertTrue(has_range)


class TestMeanAbsoluteDeviationGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = MeanAbsoluteDeviationGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["operation"], "mean_absolute_deviation")

    def test_generate_consistency(self):
        for _ in range(10):
            result = self.generator.generate()
            self.assertIn("MAD", result["problem"])
            has_mean = any(s.startswith(f"STAT_MEAN{DELIM}") for s in result["steps"])
            has_deviation = any(s.startswith(f"STAT_DEVIATION{DELIM}") for s in result["steps"])
            has_mad = any(s.startswith(f"STAT_MAD{DELIM}") for s in result["steps"])
            self.assertTrue(has_mean)
            self.assertTrue(has_deviation)
            self.assertTrue(has_mad)


if __name__ == '__main__':
    unittest.main()
