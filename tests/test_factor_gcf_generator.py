import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.factor_gcf_generator import FactorGCFGenerator
from helpers import DELIM


def parse_mono(s, var):
    """'12x^3' / '18x' / '-6' / 'x' / '-x^2' -> (coef, power)."""
    s = s.strip()
    m = re.fullmatch(rf"(-?\d*)(?:{var}(?:\^(\d+))?)?", s)
    assert m and (m.group(1) or var in s), s
    coef_txt = m.group(1)
    coef = {"": 1, "-": -1}.get(coef_txt, None)
    if coef is None:
        coef = int(coef_txt)
    power = 0
    if var in s:
        power = int(m.group(2)) if m.group(2) else 1
    return coef, power


def parse_poly(s, var):
    """Polynomial string -> {power: coef}."""
    parts = s.replace(" - ", " + -").split(" + ")
    out = {}
    for part in parts:
        c, p = parse_mono(part, var)
        out[p] = out.get(p, 0) + c
    return out


def oracle_check(example):
    """Verifies the factored answer from the problem text alone.

    The expansion must reproduce the original AND the factor must be
    maximal (quotient coefficients coprime, quotient has a constant term).
    """
    original_txt = example["problem"].split(": ", 1)[1]
    var = next(v for v in "xynt" if v in original_txt)
    original = parse_poly(original_txt, var)

    m = re.fullmatch(rf"(-?\d*{var}?(?:\^\d+)?)\((.+)\)",
                     example["final_answer"])
    assert m, example["final_answer"]
    g_coef, g_pow = parse_mono(m.group(1), var)
    quotient = parse_poly(m.group(2), var)

    expanded = {p + g_pow: c * g_coef for p, c in quotient.items()}
    assert expanded == original, (expanded, original)

    q_gcd = 0
    for c in quotient.values():
        q_gcd = gcd(q_gcd, abs(c))
    assert q_gcd == 1, "GCF not fully factored out (coefficients)"
    assert min(quotient) == 0, "GCF not fully factored out (variable)"
    return True


class TestFactorGCFGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FactorGCFGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "factor_gcf")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_expansion_and_maximality(self):
        """A9 oracle: expand the answer, compare with the problem, and
        confirm the factor is maximal."""
        for _ in range(400):
            self.assertTrue(oracle_check(self.gen.generate()))

    def test_step_arithmetic(self):
        """GCF_COEFF and DIV_TERM steps must be independently true."""
        for _ in range(300):
            result = self.gen.generate()
            expr = result["problem"].split(": ", 1)[1]
            var = next(v for v in "xynt" if v in expr)
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "GCF_COEFF":
                    nums = [int(n) for n in f[1].split(", ")]
                    g = 0
                    for n in nums:
                        g = gcd(g, n)
                    self.assertEqual(g, int(f[2]), s)
                elif f[0] == "DIV_TERM":
                    tc, tp = parse_mono(f[1], var)
                    gc, gp = parse_mono(f[2], var)
                    qc, qp = parse_mono(f[3], var)
                    self.assertEqual((tc, tp), (gc * qc, gp + qp), s)

    def test_two_and_three_term_problems(self):
        term_counts = set()
        for _ in range(60):
            result = self.gen.generate()
            original = result["problem"].split(": ", 1)[1]
            term_counts.add(len(original.replace(" - ", " + ").split(" + ")))
        self.assertEqual(term_counts, {2, 3})

    def test_numeric_only_gcf_appears(self):
        for _ in range(100):
            result = self.gen.generate()
            gcf = next(s for s in result["steps"]
                       if s.startswith(f"GCF_RESULT{DELIM}"))
            if gcf.split(DELIM)[1].isdigit():
                return
        self.fail("numeric-only GCF variant never generated")


if __name__ == "__main__":
    unittest.main()
