import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.radical_equation_generator import RadicalEquationGenerator
from helpers import DELIM


def oracle_answer(example):
    """Independently solves the radical equation from the problem text,
    including domain/extraneous checking."""
    expr = example["problem"].split(": ", 1)[1]
    m = re.fullmatch(
        r"√\((\d*)x ([+-]) (\d+)\) = (?:(-?\d+)|x ([+-]) (\d+))$", expr)
    assert m, expr
    a = int(m.group(1) or 1)
    k = int(m.group(3)) * (1 if m.group(2) == "+" else -1)

    if m.group(4) is not None:          # rhs is a constant
        c = int(m.group(4))
        if c < 0:
            return "No solution"
        num = c * c - k
        assert num % a == 0
        return f"x = {num // a}"

    mm = int(m.group(6)) * (1 if m.group(5) == "+" else -1)
    # ax + k = (x + m)²  →  x² + (2m − a)x + (m² − k) = 0
    b_coef, c_coef = 2 * mm - a, mm * mm - k
    valid = []
    for cand in range(-200, 201):
        if cand * cand + b_coef * cand + c_coef == 0:
            rhs = cand + mm
            if rhs >= 0 and rhs * rhs == a * cand + k:
                valid.append(cand)
    assert valid, expr
    if len(valid) == 2:
        return f"x = {valid[0]} or x = {valid[1]}"
    return f"x = {valid[0]}"


class TestRadicalEquationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RadicalEquationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "radical_equation")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: re-solve including the extraneous filtering."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_every_candidate_tried_and_rejections_correct(self):
        """Every quadratic candidate gets a TRY; REJECT iff the two sides
        genuinely disagree; ACCEPTed roots make up the answer."""
        for _ in range(400):
            result = self.gen.generate()
            if "No solution" in result["final_answer"]:
                continue
            # only the root-candidate layer ("x = N"), not the
            # factoring pair-search layer ("(m, n)")
            seq = [s.split(DELIM) for s in result["steps"]
                   if s.split(DELIM)[0] in ("TRY", "REJECT", "ACCEPT")
                   and s.split(DELIM)[1].startswith("x = ")]
            accepted = []
            pending = None
            for f in seq:
                if f[0] == "TRY":
                    mm = re.fullmatch(
                        r"lhs: √(\d+) = (\d+), rhs: (-?\d+)", f[2])
                    self.assertIsNotNone(mm, str(f))
                    rad, lhs, rhs = (int(v) for v in mm.groups())
                    self.assertEqual(lhs * lhs, rad, str(f))
                    pending = (lhs, rhs, f[1])
                elif f[0] == "ACCEPT":
                    self.assertEqual(pending[0], pending[1], str(f))
                    accepted.append(int(pending[2].split("= ")[1]))
                    pending = None
                else:  # REJECT
                    self.assertNotEqual(pending[0], pending[1], str(f))
                    self.assertIn("extraneous", f[2], str(f))
                    pending = None
            expected = " or ".join(f"x = {v}" for v in sorted(accepted))
            self.assertEqual(expected, result["final_answer"])

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(300):
            result = self.gen.generate()
            if result["final_answer"] == "No solution":
                kinds.add("none")
            elif " or " in result["final_answer"]:
                kinds.add("both")
            elif any(s.startswith(f"REJECT{DELIM}")
                     for s in result["steps"]):
                kinds.add("extraneous")
            else:
                kinds.add("simple")
        self.assertEqual(kinds, {"none", "both", "extraneous", "simple"})

    def test_fixed_variant_constructor(self):
        gen = RadicalEquationGenerator("no_solution")
        for _ in range(10):
            self.assertEqual(gen.generate()["final_answer"], "No solution")
        with self.assertRaises(ValueError):
            RadicalEquationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
