import unittest
import random
import sys
import os
from fractions import Fraction
from decimal import Decimal

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.fraction_decimal_percent_converter import FractionDecimalPercentConverter
from helpers import DELIM


class TestFractionDecimalPercentConverter(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests

    def test_generate_format(self):
        gen = FractionDecimalPercentConverter()
        res = gen.generate()
        for key in ["problem_id", "operation", "problem", "steps", "final_answer"]:
            self.assertIn(key, res)
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))

    def test_frac_to_dec_round_trip(self):
        gen = FractionDecimalPercentConverter()
        # Force frac_to_dec
        with unittest.mock.patch("generators.fraction_decimal_percent_converter.random.choice", side_effect=[ "frac_to_dec" ]):
            res = gen.generate()
        if res["operation"] == "convert_frac_to_dec":
            num_den = res["problem"].split()[1]
            num, den = num_den.split("/")[0], num_den.split("/")[1]
            expected = (Decimal(int(num)) / Decimal(int(den))).normalize()
            self.assertAlmostEqual(Decimal(res["final_answer"]), expected)


if __name__ == "__main__":
    unittest.main()
