import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.polynomial_long_division_generator import (
    PolynomialLongDivisionGenerator,
)
from helpers import DELIM


def parse_poly(text, var):
    """'x^3 - 2x^2 - 5x + 6' -> {3: 1, 2: -2, 1: -5, 0: 6}."""
    coefs = {}
    for sign, coef, has_var, power in re.findall(
            rf"([+-]?) ?(\d*)({var})?(?:\^(\d+))?", text):
        if not coef and not has_var:
            continue
        c = int(coef) if coef else 1
        if sign == "-":
            c = -c
        p = int(power) if power else (1 if has_var else 0)
        coefs[p] = coefs.get(p, 0) + c
    return coefs


def poly_value(coefs, x):
    return sum(c * x ** p for p, c in coefs.items())


def oracle_check(example):
    """Q·D + R must equal the dividend at several sample points."""
    m = re.fullmatch(r"Divide: \((.+)\) ÷ \((.+)\)\.", example["problem"])
    assert m, example["problem"]
    var = "y" if "y" in example["problem"] else "x"
    dividend = parse_poly(m.group(1), var)
    divisor = parse_poly(m.group(2), var)

    ans = example["final_answer"]
    mm = re.fullmatch(rf"(.+?) ([+-]) (\d+)/\((.+)\)", ans)
    if mm:
        quotient = parse_poly(mm.group(1), var)
        rem = int(mm.group(3)) * (1 if mm.group(2) == "+" else -1)
        assert mm.group(4) == m.group(2)
    else:
        quotient = parse_poly(ans, var)
        rem = 0

    for x in (-3, -1, 0, 2, 5):
        lhs = poly_value(quotient, x) * poly_value(divisor, x) + rem
        if lhs != poly_value(dividend, x):
            return False
    return True


class TestPolynomialLongDivisionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PolynomialLongDivisionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_identity(self):
        """A9 oracle: quotient·divisor + remainder = dividend."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_three_full_cycles(self):
        for _ in range(200):
            result = self.gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertEqual(ops.count("DIV_TERM"), 3)
            self.assertEqual(ops.count("MUL_TERM"), 3)
            self.assertEqual(ops.count("POLY_SUB"), 3)
            self.assertEqual(ops.count("B"), 2)
            self.assertEqual(ops.count("R"), 1)

    def test_remainder_step_matches_answer(self):
        for _ in range(300):
            result = self.gen.generate()
            r = next(s for s in result["steps"]
                     if s.startswith(f"R{DELIM}"))
            rem = int(r.split(DELIM)[1])
            if rem == 0:
                self.assertNotIn("/", result["final_answer"])
            else:
                self.assertIn(f"{abs(rem)}/(", result["final_answer"])

    def test_dividend_has_no_missing_terms(self):
        for _ in range(300):
            result = self.gen.generate()
            m = re.match(r"Divide: \((.+)\) ÷", result["problem"])
            var = "y" if "y" in result["problem"] else "x"
            coefs = parse_poly(m.group(1), var)
            self.assertEqual(sorted(coefs), [0, 1, 2, 3])
            self.assertTrue(all(c != 0 for c in coefs.values()))

    def test_zero_and_nonzero_remainders_occur(self):
        kinds = set()
        for _ in range(200):
            kinds.add("/" in self.gen.generate()["final_answer"])
        self.assertEqual(kinds, {True, False})

    def test_nonmonic_divisors_occur(self):
        gen = PolynomialLongDivisionGenerator("nonmonic")
        for _ in range(100):
            result = gen.generate()
            m = re.search(r"÷ \((\d)", result["problem"])
            self.assertIsNotNone(m, result["problem"])

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            PolynomialLongDivisionGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
