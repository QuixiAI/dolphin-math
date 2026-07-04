import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.partial_derivative_generator import PartialDerivativeGenerator
from helpers import DELIM


def parse_poly(text):
    terms = []
    if text == "0":
        return terms
    for raw in text.split(" + "):
        c = 1
        mx = 0
        ny = 0
        for factor in raw.split("*"):
            if factor.isdigit():
                c = int(factor)
            elif factor == "x":
                mx = 1
            elif factor.startswith("x^"):
                mx = int(factor[2:])
            elif factor == "y":
                ny = 1
            elif factor.startswith("y^"):
                ny = int(factor[2:])
            else:
                raise AssertionError(f"bad factor {factor!r}")
        terms.append((c, mx, ny))
    return terms


def d_terms(terms, var):
    out = []
    for c, mx, ny in terms:
        if var == "x" and mx:
            out.append((c * mx, mx - 1, ny))
        elif var == "y" and ny:
            out.append((c * ny, mx, ny - 1))
    return out


def fmt_term(c, mx, ny):
    pieces = []
    if c != 1 or (mx == 0 and ny == 0):
        pieces.append(str(c))
    if mx:
        pieces.append("x" if mx == 1 else f"x^{mx}")
    if ny:
        pieces.append("y" if ny == 1 else f"y^{ny}")
    return "*".join(pieces) if pieces else "0"


def fmt_poly(terms):
    combined = {}
    for c, mx, ny in terms:
        combined[(mx, ny)] = combined.get((mx, ny), 0) + c
    ordered = [(c, mx, ny) for (mx, ny), c in combined.items() if c]
    ordered.sort(key=lambda t: (-t[1], -t[2], -t[0]))
    return " + ".join(fmt_term(*t) for t in ordered) if ordered else "0"


def oracle_answer(example):
    problem = example["problem"]
    poly, target = re.fullmatch(
        r"Let f\(x,y\) = (.+)\. Find (f_[xy]{1,2})\.",
        problem,
    ).groups()
    terms = parse_poly(poly)
    if target == "f_x":
        return fmt_poly(d_terms(terms, "x"))
    if target == "f_y":
        return fmt_poly(d_terms(terms, "y"))
    if target == "f_xx":
        return fmt_poly(d_terms(d_terms(terms, "x"), "x"))
    if target == "f_yy":
        return fmt_poly(d_terms(d_terms(terms, "y"), "y"))
    return fmt_poly(d_terms(d_terms(terms, "x"), "y"))


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "PARTIAL_RULE":
            term = parse_poly(parts[1])
            var = parts[2][-1]
            if fmt_poly(d_terms(term, var)) != parts[3]:
                return False
        elif parts[0] == "CHECK" and parts[1] == "f_xy = f_yx":
            if parts[3] != "Clairaut equality":
                return False
    return True


class TestPartialDerivativeGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PartialDerivativeGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_mixed_has_clairaut_check(self):
        gen = PartialDerivativeGenerator("mixed_xy")
        for _ in range(100):
            result = gen.generate()
            self.assertTrue(any(s.startswith(f"CHECK{DELIM}f_xy = f_yx")
                                for s in result["steps"]))

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1\*|x\^1|y\^1|\+ 0")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 5)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            PartialDerivativeGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
