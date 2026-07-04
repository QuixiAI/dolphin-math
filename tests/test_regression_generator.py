import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.regression_generator import RegressionGenerator
from generators.exponential_model_generator import dec
from helpers import DELIM


def parse_points(problem):
    return [(int(a), int(b)) for a, b in
            re.findall(r"\((\d+), (\d+)\)", problem)]


def parse_line(problem):
    """(a, b) from 'ŷ = a + bx' / 'ŷ = a - bx' / 'ŷ = bx' / 'ŷ = a'."""
    # Split on ". " (period-space ends the sentence); a decimal point
    # is followed by a digit, not a space, so it is not consumed.
    m = re.search(r"ŷ = (.+?)\. ", problem)
    expr = m.group(1).strip()
    mm = re.fullmatch(r"(-?[\d.]+) ([+-]) ([\d.]*)x", expr)
    if mm:
        a = Fraction(mm.group(1))
        coef = Fraction(mm.group(3)) if mm.group(3) else Fraction(1)
        b = coef if mm.group(2) == "+" else -coef
        return a, b
    mm = re.fullmatch(r"(-?[\d.]*)x", expr)
    if mm:
        c = mm.group(1)
        return Fraction(0), (Fraction(-1) if c == "-" else
                             Fraction(c) if c else Fraction(1))
    return Fraction(expr), Fraction(0)


def lsq(points):
    n = len(points)
    xb = Fraction(sum(x for x, _ in points), n)
    yb = Fraction(sum(y for _, y in points), n)
    sxy = sum((x - xb) * (y - yb) for x, y in points)
    sxx = sum((x - xb) ** 2 for x, _ in points)
    syy = sum((y - yb) ** 2 for _, y in points)
    b = Fraction(sxy, sxx)
    a = yb - b * xb
    return a, b, sxy, sxx, syy


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    if p.startswith("Find the least-squares regression line"):
        a, b, *_ = lsq(parse_points(p))
        from generators.regression_generator import line_txt
        return ans == line_txt(a, b)
    if p.startswith("Find the correlation coefficient"):
        _, _, sxy, sxx, syy = lsq(parse_points(p))
        r = sxy / math.sqrt(sxx * syy)
        return abs(float(Fraction(ans)) - r) < 1e-9
    if p.startswith("Find r^2"):
        _, _, sxy, sxx, syy = lsq(parse_points(p))
        return Fraction(ans) == Fraction(sxy * sxy, sxx * syy)
    m = re.search(r"residual at the point \((\d+), (\d+)\)", p)
    if m:
        j, yj = int(m.group(1)), int(m.group(2))
        a, b = parse_line(p)
        return Fraction(ans) == yj - (a + b * j)
    m = re.search(r"Predict ŷ when x = (\d+)", p)
    assert m, p
    j = int(m.group(1))
    a, b = parse_line(p)
    return Fraction(ans) == a + b * j


class TestRegressionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RegressionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: independent least-squares recomputation."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_r_is_clean_and_bounded(self):
        gen = RegressionGenerator("correlation")
        for _ in range(200):
            result = gen.generate()
            r = float(Fraction(result["final_answer"]))
            self.assertLess(abs(r), 1.0)      # |r| = 1 excluded
            # r is an exact tenth by construction.
            self.assertEqual(round(r * 10), r * 10)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_formula_steps_present(self):
        for v, code in (("line", "SLOPE_FORMULA"),
                        ("correlation", "CORR_FORMULA"),
                        ("r_squared", "RSQ_FORMULA")):
            gen = RegressionGenerator(v)
            for _ in range(50):
                result = gen.generate()
                self.assertTrue(any(s.startswith(f"{code}{DELIM}")
                                    for s in result["steps"]))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 5)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RegressionGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
