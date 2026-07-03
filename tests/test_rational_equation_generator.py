import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.rational_equation_generator import RationalEquationGenerator
from helpers import DELIM


def oracle_answer(example):
    """Independently solves with restriction filtering, from text alone."""
    expr = example["problem"].split(": ", 1)[1]

    m = re.fullmatch(r"(-?\d+)/x = (\d+)/(-?\d+)", expr)
    if m:  # proportion
        a, b, c = (int(v) for v in m.groups())
        x = Fraction(a * c, b)
        assert x.denominator == 1 and x != 0
        return f"x = {x.numerator}"

    m = re.fullmatch(r"(-?\d+)/x \+ (\d+) = (-?\d+)", expr)
    if m:  # sum form
        a, b, c = (int(v) for v in m.groups())
        x = Fraction(a, c - b)
        assert x.denominator == 1 and x != 0
        return f"x = {x.numerator}"

    m = re.fullmatch(r"\(x \+ (\d+)\)/\(x ([+-]) (\d+)\) = (-?\d+)/\(x \2 \3\)",
                     expr)
    if m:  # no_solution family: candidate is q − c
        c = int(m.group(1))
        r = int(m.group(3)) * (-1 if m.group(2) == "+" else 1)
        q = int(m.group(4))
        candidate = q - c
        return "No solution" if candidate == r else f"x = {candidate}"

    m = re.fullmatch(r"x\^2/\(x - (\d+)\) = (\d+)/\(x - \1\)", expr)
    assert m, expr
    r = int(m.group(1))
    assert int(m.group(2)) == r * r
    # candidates ±r; +r restricted
    return f"x = {-r}"


class TestRationalEquationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RationalEquationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "rational_equation")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: re-solve with restriction filtering."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_domain_note_always_first_move(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(result["steps"][1].startswith(f"DOMAIN_NOTE{DELIM}"),
                            result["steps"][:2])

    def test_rejections_cite_the_restriction(self):
        for _ in range(300):
            result = self.gen.generate()
            note = next(s for s in result["steps"]
                        if s.startswith(f"DOMAIN_NOTE{DELIM}"))
            restricted = note.split(DELIM)[1].split("≠ ")[1]
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "REJECT":
                    self.assertEqual(f[1], f"x = {restricted}", s)
                    self.assertIn("denominator zero", f[2], s)

    def test_valid_candidates_verified_with_fractions(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "TRY" and f[2].startswith("lhs: "):
                    mm = re.fullmatch(r"lhs: (-?[\d/]+), rhs: (-?[\d/]+)",
                                      f[2])
                    self.assertIsNotNone(mm, s)
                    self.assertEqual(Fraction(mm.group(1)),
                                     Fraction(mm.group(2)), s)

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(200):
            result = self.gen.generate()
            p = result["problem"]
            if "x^2" in p:
                kinds.add("mixed")
            elif result["final_answer"] == "No solution":
                kinds.add("none")
            elif "(x + " in p:
                kinds.add("none_family_valid")
            elif "+ " in p.split(" = ")[0] and "/x" in p:
                kinds.add("sum")
            else:
                kinds.add("proportion")
        self.assertIn("mixed", kinds)
        self.assertIn("none", kinds)
        self.assertIn("sum", kinds)
        self.assertIn("proportion", kinds)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RationalEquationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
