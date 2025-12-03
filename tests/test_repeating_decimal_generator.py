import unittest
from unittest.mock import patch

from generators.repeating_decimal_generator import RepeatingDecimalGenerator
from helpers import DELIM


class TestRepeatingDecimalGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = RepeatingDecimalGenerator()

    def test_terminating(self):
        with patch("generators.repeating_decimal_generator.random.choice", return_value=8), \
             patch("generators.repeating_decimal_generator.random.randint", return_value=1):
            res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertIn("terminating", res["final_answer"])
        self.assertIn("0.125", res["final_answer"])

    def test_repeating(self):
        with patch("generators.repeating_decimal_generator.random.choice", return_value=3), \
             patch("generators.repeating_decimal_generator.random.randint", return_value=1):
            res = self.gen.generate()
        self.assertIn("repeating", res["final_answer"])
        self.assertTrue(res["final_answer"].startswith("0.333333"))


if __name__ == "__main__":
    unittest.main()
