import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.synthetic_division_generator import (
    SyntheticDivisionGenerator,
)
from tests.test_polynomial_long_division_generator import (
    parse_poly,
    poly_value,
)
from helpers import DELIM


def oracle_check(example):
    """Q·(x - r) + rem = dividend at sample points; row is consistent."""
    m = re.fullmatch(
        r"Use synthetic division to divide \((.+)\) by \((.+)\)\.",
        example["problem"])
    assert m, example["problem"]
    dividend = parse_poly(m.group(1), "x")
    divisor = parse_poly(m.group(2), "x")

    ans = example["final_answer"]
    mm = re.fullmatch(r"(.+?) ([+-]) (\d+)/\((.+)\)", ans)
    if mm:
        quotient = parse_poly(mm.group(1), "x")
        rem = int(mm.group(3)) * (1 if mm.group(2) == "+" else -1)
    else:
        quotient = parse_poly(ans, "x")
        rem = 0

    for x in (-3, -1, 0, 2, 5):
        if poly_value(quotient, x) * poly_value(divisor, x) + rem != \
                poly_value(dividend, x):
            return False
    return True


class TestSyntheticDivisionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SyntheticDivisionGenerator()

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

    def test_r_matches_divisor_with_sign_flip(self):
        for _ in range(300):
            result = self.gen.generate()
            setup = result["steps"][0].split(DELIM)
            r = int(setup[2].replace("r = ", ""))
            m = re.search(r"by \(x ([+-]) (\d+)\)", result["problem"])
            c = int(m.group(2)) * (1 if m.group(1) == "+" else -1)
            self.assertEqual(r, -c, result["problem"])

    def test_multiply_add_rhythm(self):
        for _ in range(300):
            result = self.gen.generate()
            coefs = [int(v) for v in
                     next(s for s in result["steps"]
                          if s.startswith(f"COEFFS{DELIM}"))
                     .split(DELIM)[1].split(", ")]
            r = int(result["steps"][0].split(DELIM)[2].replace("r = ", ""))
            bottom = [int(v) for v in
                      next(s for s in result["steps"]
                           if s.startswith(f"SYN_ROW{DELIM}"))
                      .split(DELIM)[1].split(", ")]
            # recompute the synthetic row
            expect = [coefs[0]]
            for c in coefs[1:]:
                expect.append(c + r * expect[-1])
            self.assertEqual(bottom, expect)
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)

    def test_missing_term_placeholder(self):
        gen = SyntheticDivisionGenerator("missing_term")
        for _ in range(150):
            result = gen.generate()
            coeff_step = next(s for s in result["steps"]
                              if s.startswith(f"COEFFS{DELIM}"))
            f = coeff_step.split(DELIM)
            self.assertIn("0 inserted", f[2], coeff_step)
            self.assertIn("0", f[1].split(", "), coeff_step)

    def test_quartic_has_extra_column(self):
        gen = SyntheticDivisionGenerator("quartic")
        for _ in range(100):
            result = gen.generate()
            self.assertIn("^4", result["problem"])
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertEqual(ops.count("M"), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            SyntheticDivisionGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
