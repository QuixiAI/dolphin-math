import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.radical_add_sub_generator import RadicalAddSubGenerator
from helpers import DELIM


def parse_terms(expr):
    """'√50 + 3√18 - √2' -> [(sign·coef, radicand), ...]."""
    expr = expr.replace(" - ", " + -").split(" + ")
    out = []
    for t in expr:
        m = re.fullmatch(r"(-?)(\d*)√(\d+)", t.strip())
        assert m, t
        coef = int(m.group(2) or 1) * (-1 if m.group(1) else 1)
        out.append((coef, int(m.group(3))))
    return out


def simplify(coef, n):
    """coef·√n -> (coef·s, f) with f square-free."""
    s = 1
    for cand in range(1, int(n ** 0.5) + 1):
        if n % (cand * cand) == 0:
            s = cand
    return coef * s, n // (s * s)


def oracle_answer(example):
    """Simplifies every term and combines like radicands, from text alone."""
    expr = example["problem"].split(": ", 1)[1]
    terms = [simplify(c, n) for c, n in parse_terms(expr)]
    cores = {f for _, f in terms}
    if len(cores) == 1:
        f = cores.pop()
        total = sum(c for c, _ in terms)
        assert total != 0
        return ("√%d" % f if total == 1 else
                "-√%d" % f if total == -1 else f"{total}√{f}")
    # unlike: simplified terms joined in original order
    out = ""
    for i, (c, f) in enumerate(terms):
        t = ("√%d" % f if abs(c) == 1 else f"{abs(c)}√{f}")
        if i == 0:
            out = t if c > 0 else f"-{t}"
        else:
            out += f" + {t}" if c > 0 else f" - {t}"
    return out


class TestRadicalAddSubGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RadicalAddSubGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "radical_add_sub")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: simplify and combine independently from the text."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_combine_step_arithmetic(self):
        """A/S steps on radical terms must have correct coefficients."""
        term_re = re.compile(r"(-?)(\d*)√(\d+)")
        def coef(t):
            m = term_re.fullmatch(t)
            return int(m.group(2) or 1) * (-1 if m.group(1) else 1)
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "A":
                    self.assertEqual(coef(f[1]) + coef(f[2]), coef(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(coef(f[1]) - coef(f[2]), coef(f[3]), s)
                elif f[0] == "SQUARE_FACTOR":
                    m = re.fullmatch(r"(\d+) × (\d+)", f[2])
                    self.assertEqual(int(m.group(1)) * int(m.group(2)),
                                     int(f[1]), s)

    def test_unlike_case_appears_with_verdict(self):
        unlike = 0
        for _ in range(300):
            result = self.gen.generate()
            has_verdict = any(s.startswith(f"UNLIKE_RADICALS{DELIM}")
                              for s in result["steps"])
            has_combine = any(s.split(DELIM)[0] in ("A", "S")
                              for s in result["steps"])
            self.assertNotEqual(has_verdict, has_combine, result["problem"])
            if has_verdict:
                unlike += 1
                self.assertIn("√", result["final_answer"])
                self.assertTrue(" + " in result["final_answer"] or
                                " - " in result["final_answer"])
        self.assertGreater(unlike, 30)


if __name__ == "__main__":
    unittest.main()
