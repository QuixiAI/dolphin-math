import os
import random
import re
import sys
import unittest
from math import gcd, lcm

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.rational_expr_add_sub_generator import (
    RationalExprAddSubGenerator,
)
from generators.special_solution_equation_generator import lin
from helpers import DELIM


def oracle_answer(example):
    """Independently combines the two fractions from the problem text."""
    expr = example["problem"].split(": ", 1)[1]
    var = next(v for v in "xyn" if v in expr)

    m = re.fullmatch(
        rf"(\d+)/\(({var} [+-] \d+)\) ([+-]) (\d+)/\(({var} [+-] \d+)\)",
        expr)
    if m and m.group(2) == m.group(5):  # like denominators
        a, b = int(m.group(1)), int(m.group(4))
        total = a + b if m.group(3) == "+" else a - b
        return f"{total}/({m.group(2)})"

    mm = re.fullmatch(
        rf"(\d+)/\((\d+){var}\) ([+-]) (\d+)/\((\d+){var}\)", expr)
    if mm:  # monomial denominators
        a, mden, sgn, b, nden = (mm.group(1), mm.group(2), mm.group(3),
                                 mm.group(4), mm.group(5))
        a, b, mden, nden = int(a), int(b), int(mden), int(nden)
        L = lcm(mden, nden)
        total = (a * (L // mden) + b * (L // nden) if sgn == "+"
                 else a * (L // mden) - b * (L // nden))
        g = gcd(abs(total), L)
        num, den_c = total // g, L // g
        den_txt = var if den_c == 1 else f"{den_c}{var}"
        return f"{num}/({den_txt})"

    mb = re.fullmatch(
        rf"(\d+)/\(({var} [+-] \d+)\) ([+-]) (\d+)/\(({var} [+-] \d+)\)",
        expr)
    assert mb, expr
    a, b = int(mb.group(1)), int(mb.group(4))
    plus = mb.group(3) == "+"

    def const_of(s):
        m2 = re.fullmatch(rf"{var} ([+-]) (\d+)", s)
        return int(m2.group(2)) * (1 if m2.group(1) == "+" else -1)

    p, q = const_of(mb.group(2)), const_of(mb.group(5))
    x_coef = a + b if plus else a - b
    const = a * q + b * p if plus else a * q - b * p
    return f"({lin(x_coef, const, var)})/(({mb.group(2)})({mb.group(5)}))"


class TestRationalExprAddSubGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RationalExprAddSubGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "rational_expr_add_sub")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: combine independently; monomial results reduced."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "L":
                    self.assertEqual(lcm(int(f[1]), int(f[2])), int(f[3]), s)
                elif f[0] == "A" and f[1].lstrip("-").isdigit():
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "S" and f[1].lstrip("-").isdigit():
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "COMB_CONST":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(200):
            p = self.gen.generate()["problem"]
            dens = re.findall(r"/\(([^)]+)\)", p)
            if dens[0] == dens[1]:
                kinds.add("like")
            elif re.match(r"\d", dens[0]):
                kinds.add("monomial")
            else:
                kinds.add("binomial")
        self.assertEqual(kinds, {"like", "monomial", "binomial"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RationalExprAddSubGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
