import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.tangent_line_generator import (
    TangentLineGenerator,
    line_txt,
)
from tests.test_polynomial_long_division_generator import (
    parse_poly,
    poly_value,
)
from helpers import DELIM


def oracle_answer(example):
    m = re.fullmatch(r"Find the equation of the (tangent|normal) line "
                     r"to f\(x\) = (.+) at x = (-?\d+)\.",
                     example["problem"])
    assert m, example["problem"]
    kind, f_txt, a = m.group(1), m.group(2), int(m.group(3))
    coefs = parse_poly(f_txt, "x")
    fa = poly_value(coefs, a)
    fp = sum(c * p * a ** (p - 1) for p, c in coefs.items() if p >= 1)
    slope = Fraction(fp) if kind == "tangent" else Fraction(-1, fp)
    return line_txt(slope, fa - slope * a)


class TestTangentLineGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TangentLineGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_line_passes_through_the_point(self):
        for _ in range(300):
            result = self.gen.generate()
            m = re.fullmatch(r"Find the equation of the (?:\w+) line to "
                             r"f\(x\) = (.+) at x = (-?\d+)\.",
                             result["problem"])
            coefs = parse_poly(m.group(1), "x")
            a = int(m.group(2))
            fa = poly_value(coefs, a)
            slope, k = parse_line(result["final_answer"])
            self.assertEqual(slope * a + k, fa,
                             result["final_answer"])

    def test_normal_slope_is_negative_reciprocal(self):
        gen = TangentLineGenerator("normal")
        for _ in range(200):
            result = gen.generate()
            m = re.fullmatch(r"Find the equation of the normal line to "
                             r"f\(x\) = (.+) at x = (-?\d+)\.",
                             result["problem"])
            coefs = parse_poly(m.group(1), "x")
            a = int(m.group(2))
            fp = sum(c * p * a ** (p - 1)
                     for p, c in coefs.items() if p >= 1)
            slope, _ = parse_line(result["final_answer"])
            self.assertEqual(slope * fp, -1)

    def test_both_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"tangent_line", "normal_line"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            TangentLineGenerator("bogus")


def parse_line(txt):
    """'y = (-1/4)x + 9/2' -> (Fraction, Fraction)."""
    body = txt.replace("y = ", "")
    m = re.fullmatch(r"(?:\(?(-?\d+(?:/\d+)?)\)?)?(-?)x"
                     r"(?: ([+-]) (\d+(?:/\d+)?))?", body)
    if m:
        if m.group(1):
            slope = Fraction(m.group(1))
        else:
            slope = Fraction(-1 if m.group(2) == "-" else 1)
        k = Fraction(m.group(4) or 0) * \
            (1 if (m.group(3) or "+") == "+" else -1)
        return slope, k
    return Fraction(0), Fraction(body)


if __name__ == "__main__":
    unittest.main()
