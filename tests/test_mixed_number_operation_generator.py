import unittest
import random
import sys
import os
from fractions import Fraction
from unittest.mock import patch

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.mixed_number_operation_generator import MixedNumberOperationGenerator
from helpers import DELIM


class TestMixedNumberOperationGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests

    def _parse_value(self, s: str):
        s = s.strip()
        if " " in s:
            whole_str, frac_str = s.split(" ", 1)
            num_str, den_str = frac_str.split("/")
            return Fraction(int(whole_str)) + Fraction(int(num_str), int(den_str))
        if "/" in s:
            num_str, den_str = s.split("/")
            return Fraction(int(num_str), int(den_str))
        return Fraction(int(s), 1)

    def _assert_common(self, res, op_name):
        for key in ["problem_id", "operation", "problem", "steps", "final_answer"]:
            self.assertIn(key, res)
        self.assertEqual(res["operation"], op_name)
        self.assertTrue(res["steps"] and res["steps"][-1].startswith(f"Z{DELIM}"))
        # Conversions present
        self.assertTrue(any(s.startswith(f"MIX_IMPROPER{DELIM}") for s in res["steps"]))

    def _compute_expected(self, problem_str, op_symbol):
        left_part, right_part = problem_str.split(f" {op_symbol} ")
        w1, rest1 = left_part.strip().split(" ", 1)
        n1, d1 = rest1.split("/")
        w2, rest2 = right_part.strip().split(" ", 1)
        n2, d2 = rest2.split("/")
        frac1 = Fraction(int(w1) * int(d1) + int(n1), int(d1))
        frac2 = Fraction(int(w2) * int(d2) + int(n2), int(d2))
        if op_symbol == '+':
            return frac1 + frac2
        if op_symbol == '-':
            return frac1 - frac2
        if op_symbol == '*':
            return frac1 * frac2
        return frac1 / frac2

    def test_addition_flow(self):
        gen = MixedNumberOperationGenerator('+')
        res = gen.generate()
        self._assert_common(res, "mixed_number_add")
        expected = self._compute_expected(res["problem"], '+')
        self.assertEqual(self._parse_value(res["final_answer"]), expected)

    def test_subtraction_non_negative(self):
        gen = MixedNumberOperationGenerator('-')
        res = gen.generate()
        self._assert_common(res, "mixed_number_sub")
        expected = self._compute_expected(res["problem"], '-')
        self.assertGreaterEqual(expected, 0)
        # Ensure no negative final answer for now
        if '/' in res["final_answer"]:
            self.assertFalse(res["final_answer"].startswith("-"))
        else:
            self.assertGreaterEqual(int(res["final_answer"]), 0)

    def test_multiplication_flow(self):
        gen = MixedNumberOperationGenerator('*')
        res = gen.generate()
        self._assert_common(res, "mixed_number_mult")
        expected = self._compute_expected(res["problem"], '*')
        self.assertEqual(self._parse_value(res["final_answer"]), expected)

    def test_division_flow(self):
        gen = MixedNumberOperationGenerator('/')
        res = gen.generate()
        self._assert_common(res, "mixed_number_div")
        expected = self._compute_expected(res["problem"], '/')
        self.assertEqual(self._parse_value(res["final_answer"]), expected)
        self.assertTrue(any(s.startswith(f"I{DELIM}") for s in res["steps"]), "Expected inversion step for division")

    def test_borrow_guard_for_subtraction(self):
        # Force frac1 < frac2 then ensure generator swaps to keep non-negative
        with patch(
            "generators.mixed_number_operation_generator.MixedNumberOperationGenerator._pick_mixed",
            side_effect=[(0, 1, 2), (3, 1, 2)],
        ):
            gen = MixedNumberOperationGenerator('-')
            res = gen.generate()
        expected = self._compute_expected(res["problem"], '-')
        self.assertGreaterEqual(expected, 0)


if __name__ == "__main__":
    unittest.main()
