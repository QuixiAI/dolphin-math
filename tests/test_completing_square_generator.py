import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.completing_square_generator import CompletingSquareGenerator
from helpers import DELIM


def parse_quadratic(expr, var):
    """'x^2 + 6x - 7' -> (b, c)."""
    m = re.fullmatch(
        rf"{var}\^2 ([+-]) (\d*){var} ([+-]) (\d+)", expr)
    assert m, expr
    b = int(m.group(2) or 1) * (1 if m.group(1) == "+" else -1)
    c = int(m.group(4)) * (1 if m.group(3) == "+" else -1)
    return b, c


def oracle_answer(example):
    """Independently solves / converts from the problem text alone."""
    p = example["problem"]
    var = next(v for v in "xyn" if f"{v}^2" in p)

    if example["operation"] == "vertex_form_by_completing_square":
        expr = p.split(": y = ", 1)[1]
        b, c = parse_quadratic(expr, var)
        assert b % 2 == 0
        h = b // 2
        v = c - h * h
        pst = f"({var} + {h})^2" if h > 0 else f"({var} - {-h})^2"
        v_txt = f" + {v}" if v > 0 else f" - {-v}" if v < 0 else ""
        return f"y = {pst}{v_txt}"

    expr = p.split(": ", 1)[1][: -len(" = 0")]
    b, c = parse_quadratic(expr, var)
    assert b % 2 == 0
    h = b // 2
    k = h * h - c
    assert k > 0
    r = int(k ** 0.5)
    if r * r == k:
        lo, hi = sorted((-h - r, -h + r))
        return f"{var} = {lo} or {var} = {hi}"
    return f"{var} = {-h} - √{k} or {var} = {-h} + √{k}"


class TestCompletingSquareGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CompletingSquareGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: re-solve / re-convert from the problem text alone."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_complete_square_arithmetic(self):
        """The halve-and-square move and PST rewrite must be true."""
        for _ in range(400):
            result = self.gen.generate()
            cs = next(s for s in result["steps"]
                      if s.startswith(f"COMPLETE_SQUARE{DELIM}"))
            f = cs.split(DELIM)
            m1 = re.fullmatch(r"half of (-?\d+) = (-?\d+)", f[1])
            self.assertIsNotNone(m1, cs)
            self.assertEqual(int(m1.group(1)), 2 * int(m1.group(2)), cs)
            m2 = re.fullmatch(r"\(?(-?\d+)\)?\^2 = (\d+)", f[2])
            self.assertIsNotNone(m2, cs)
            self.assertEqual(int(m2.group(1)) ** 2, int(m2.group(2)), cs)
            self.assertEqual(int(m1.group(2)), int(m2.group(1)), cs)

    def test_solve_checks_land_on_zero(self):
        gen = CompletingSquareGenerator("solve")
        for _ in range(200):
            result = gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "CHECK" and "√" not in f[2]:
                    self.assertEqual(f[2].rsplit("= ", 1)[1], "0", s)

    def test_both_modes_and_irrational_reachable(self):
        ops = set()
        irrational = 0
        for _ in range(200):
            result = self.gen.generate()
            ops.add(result["operation"])
            if "√" in result["final_answer"]:
                irrational += 1
        self.assertEqual(ops, {"completing_the_square",
                               "vertex_form_by_completing_square"})
        self.assertGreater(irrational, 15)

    def test_fixed_mode_constructor(self):
        gen = CompletingSquareGenerator("vertex")
        for _ in range(10):
            self.assertEqual(gen.generate()["operation"],
                             "vertex_form_by_completing_square")
        with self.assertRaises(ValueError):
            CompletingSquareGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
