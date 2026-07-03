import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.factor_special_forms_generator import FactorSpecialFormsGenerator
from helpers import DELIM


def parse_poly(s, var):
    """Polynomial string -> {power: coef} (handles ^2, ^3, bare, const)."""
    out = {}
    for part in s.replace(" - ", " + -").split(" + "):
        part = part.strip()
        m = re.fullmatch(rf"(-?\d*)(?:{var}(?:\^(\d+))?)?", part)
        assert m and part, (s, part)
        coef = {"": 1, "-": -1}.get(m.group(1), None)
        if coef is None:
            coef = int(m.group(1))
        power = 0
        if var in part:
            power = int(m.group(2)) if m.group(2) else 1
        out[power] = out.get(power, 0) + coef
    return {p: c for p, c in out.items() if c != 0}


def poly_mul(p1, p2):
    out = {}
    for e1, c1 in p1.items():
        for e2, c2 in p2.items():
            out[e1 + e2] = out.get(e1 + e2, 0) + c1 * c2
    return {p: c for p, c in out.items() if c != 0}


def expand_answer(ans, var):
    """'(2x + 3)(4x^2 - 6x + 9)' or '(2x + 3)^2' -> {power: coef}."""
    factors = re.findall(r"\(([^)]+)\)(?:\^(\d+))?", ans)
    assert factors, ans
    result = {0: 1}
    for inner, exp in factors:
        p = parse_poly(inner, var)
        for _ in range(int(exp) if exp else 1):
            result = poly_mul(result, p)
    return result


class TestFactorSpecialFormsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FactorSpecialFormsGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_expansion(self):
        """A9 oracle: the factored answer must expand to the problem
        polynomial exactly, and the roots must be coprime (no hidden GCF)."""
        for _ in range(400):
            result = self.gen.generate()
            original_txt = result["problem"].split(": ", 1)[1]
            var = next(v for v in "xyn" if v in original_txt)
            original = parse_poly(original_txt, var)
            expanded = expand_answer(result["final_answer"], var)
            self.assertEqual(expanded, original, result["final_answer"])
            coefs = [abs(c) for c in original.values()]
            g = 0
            for c in coefs:
                g = gcd(g, c)
            self.assertEqual(g, 1, f"hidden GCF in {original_txt}")

    def test_pattern_checks_verified(self):
        """The PST middle-term CHECK and expansion CHECKs must be true."""
        for _ in range(400):
            result = self.gen.generate()
            original_txt = result["problem"].split(": ", 1)[1]
            var = next(v for v in "xyn" if v in original_txt)
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "ROOT" and f[1].isdigit():
                    self.assertEqual(int(f[2]) ** 2, int(f[1]), s)
                elif f[0] == "CBRT" and f[1].isdigit():
                    self.assertEqual(int(f[2]) ** 3, int(f[1]), s)
                elif f[0] == "CHECK" and f[1] == "middle_term":
                    self.assertEqual(f[2].rsplit("= ", 1)[1], f[3], s)
                elif f[0] == "CHECK" and f[1] in ("foil", "expand"):
                    self.assertEqual(parse_poly(f[2], var),
                                     parse_poly(f[3], var), s)

    def test_all_variants_reachable(self):
        seen = {self.gen.generate()["operation"] for _ in range(120)}
        self.assertEqual(seen, {"factor_difference_of_squares",
                                "factor_perfect_square",
                                "factor_sum_of_cubes",
                                "factor_difference_of_cubes"})

    def test_pst_signs_both_appear(self):
        gen = FactorSpecialFormsGenerator("perfect_square")
        signs = {"+" if "+ " in gen.generate()["final_answer"] else "-"
                 for _ in range(60)}
        self.assertEqual(signs, {"+", "-"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            FactorSpecialFormsGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
