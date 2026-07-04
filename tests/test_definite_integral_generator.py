import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.definite_integral_generator import (
    DefiniteIntegralGenerator,
)
from tests.test_derivative_power_rule_generator import parse_terms
from helpers import DELIM


def exact_integral(terms, a, b):
    total = Fraction(0)
    for c, n in terms:
        total += Fraction(c, n + 1) * (b ** (n + 1) - a ** (n + 1))
    return total


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"Evaluate ∫ from (-?\d+) to (-?\d+) of \((.+)\) "
                     r"dx using the Fundamental Theorem of Calculus\.",
                     p)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        terms = parse_terms(m.group(3))
        v = exact_integral(terms, a, b)
        assert v.denominator == 1
        return str(v.numerator)
    m = re.fullmatch(r"Find the average value of f\(x\) = (.+) on "
                     r"\[(-?\d+), (-?\d+)\]\.", p)
    assert m, p
    terms = parse_terms(m.group(1))
    a, b = int(m.group(2)), int(m.group(3))
    return str(exact_integral(terms, a, b) / (b - a))


class TestDefiniteIntegralGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DefiniteIntegralGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: exact Fraction integration."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_both_endpoints_evaluated(self):
        for _ in range(200):
            result = self.gen.generate()
            evals = [s for s in result["steps"]
                     if s.startswith(f"EVAL{DELIM}F(")]
            self.assertEqual(len(evals), 2)

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "E":
                    self.assertEqual(int(f[1].strip("()")) ** int(f[2]),
                                     int(f[3]), s)
                elif f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)

    def test_both_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"definite_integral_ftc",
                               "definite_integral_average"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            DefiniteIntegralGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
