import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.rational_expr_simplify_generator import (
    RationalExprSimplifyGenerator,
)
from generators.factor_trinomial_generator import binomial
from helpers import DELIM


def parse_trinomial(s, var):
    """'x^2 - x - 6' -> (b, c); returns None if not a monic trinomial."""
    m = re.fullmatch(rf"{var}\^2 ([+-]) (\d*){var} ([+-]) (\d+)", s)
    if not m:
        return None
    b = int(m.group(2) or 1) * (1 if m.group(1) == "+" else -1)
    c = int(m.group(4)) * (1 if m.group(3) == "+" else -1)
    return b, c


def int_roots(b, c):
    """Integer roots of x² + bx + c (assumes they exist)."""
    for p in range(-100, 101):
        if p * p + b * p + c == 0:
            q = -b - p
            if p * q == c:
                return sorted((p, q))
    raise AssertionError((b, c))


def oracle_answer(example):
    """Independently factors and cancels from the problem text alone."""
    expr = example["problem"].split(": ", 1)[1]
    var = next(v for v in "xyn" if v in expr)
    m = re.fullmatch(r"\((.+)\)/\((.+)\)", expr)
    num_txt, den_txt = m.group(1), m.group(2)

    gm = re.fullmatch(rf"(\d+){var}\^2 ([+-]) (\d+){var}", num_txt)
    if gm:  # gcf_monomial
        A = int(gm.group(1))
        B = int(gm.group(3)) * (1 if gm.group(2) == "+" else -1)
        g = int(re.fullmatch(rf"(\d+){var}", den_txt).group(1))
        assert gcd(A, abs(B)) == g
        a, b = A // g, B // g
        return f"{a}{var} + {b}" if b > 0 else f"{a}{var} - {-b}"

    b_n, c_n = parse_trinomial(num_txt, var)
    num_roots = int_roots(b_n, c_n)

    den_tri = parse_trinomial(den_txt, var)
    if den_tri is None:  # over_binomial
        dm = re.fullmatch(rf"{var} ([+-]) (\d+)", den_txt)
        d_root = int(dm.group(2)) * (-1 if dm.group(1) == "+" else 1)
        assert d_root in num_roots
        other = [r for r in num_roots if r != d_root][0]
        return binomial(var, -other).strip("()")

    den_roots = int_roots(*den_tri)
    shared = set(num_roots) & set(den_roots)
    assert len(shared) == 1, expr
    s = shared.pop()
    top = [r for r in num_roots if r != s][0]
    bottom = [r for r in den_roots if r != s][0]
    return f"{binomial(var, -top)}/{binomial(var, -bottom)}"


class TestRationalExprSimplifyGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RationalExprSimplifyGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "rational_expr_simplify")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: factor and cancel independently."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_cancel_step_present_with_shared_factor(self):
        for _ in range(300):
            result = self.gen.generate()
            cancel = next(s for s in result["steps"]
                          if s.startswith(f"CANCEL{DELIM}"))
            f = cancel.split(DELIM)
            # the cancelled factor must appear in the last pre-cancel REWRITE
            rewrites = [s for s in result["steps"]
                        if s.startswith(f"REWRITE{DELIM}")]
            self.assertIn(f[1], rewrites[-1], cancel)
            self.assertEqual(f[2], result["final_answer"], cancel)

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(200):
            p = self.gen.generate()["problem"]
            den = re.search(r"\)/\((.+)\)$", p).group(1)
            if "^2" in den:
                kinds.add("two_trinomials")
            elif re.match(r"\d", den):
                kinds.add("gcf_monomial")
            else:
                kinds.add("over_binomial")
        self.assertEqual(kinds, {"two_trinomials", "gcf_monomial",
                                 "over_binomial"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RationalExprSimplifyGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
