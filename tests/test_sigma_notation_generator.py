import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.sigma_notation_generator import SigmaNotationGenerator
from helpers import DELIM


def oracle_answer(example):
    """Independently expands the sigma from the problem text alone."""
    m = re.fullmatch(
        r"Expand and evaluate: Σ_\(k=(-?\d+)\)\^\((-?\d+)\) (.+)\.",
        example["problem"])
    assert m, example["problem"]
    lo, hi, expr = int(m.group(1)), int(m.group(2)), m.group(3)

    mm = re.fullmatch(r"(?:(\d+)·)?(\d+)\^k", expr)
    if mm:
        c = int(mm.group(1) or 1)
        b = int(mm.group(2))
        return str(sum(c * b ** k for k in range(lo, hi + 1)))
    mm = re.fullmatch(r"(\d*)k\^2", expr)
    if mm:
        a = int(mm.group(1) or 1)
        return str(sum(a * k * k for k in range(lo, hi + 1)))
    mm = re.fullmatch(r"\(?(\d*)k(?: ([+-]) (\d+))?\)?", expr)
    assert mm, expr
    a = int(mm.group(1) or 1)
    b = int(mm.group(3) or 0) * (1 if (mm.group(2) or "+") == "+" else -1)
    return str(sum(a * k + b for k in range(lo, hi + 1)))


class TestSigmaNotationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SigmaNotationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: expand and sum independently."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_one_term_per_index(self):
        for _ in range(300):
            result = self.gen.generate()
            m = re.search(r"k=(-?\d+)\)\^\((-?\d+)\)", result["problem"])
            lo, hi = int(m.group(1)), int(m.group(2))
            terms = [s.split(DELIM) for s in result["steps"]
                     if s.startswith(f"SIGMA_TERM{DELIM}")]
            self.assertEqual([t[1] for t in terms],
                             [f"k={k}" for k in range(lo, hi + 1)])

    def test_expand_line_matches_terms(self):
        for _ in range(300):
            result = self.gen.generate()
            vals = [int(s.split(DELIM)[3]) for s in result["steps"]
                    if s.startswith(f"SIGMA_TERM{DELIM}")]
            expand = next(s for s in result["steps"]
                          if s.startswith(f"SIGMA_EXPAND{DELIM}"))
            got = [int(v.strip("()")) for v in
                   expand.split(DELIM)[1].split(" + ")]
            self.assertEqual(got, vals)
            self.assertEqual(sum(vals), int(result["final_answer"]))

    def test_running_sum_chain(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)

    def test_zero_lower_bound_occurs_for_power(self):
        gen = SigmaNotationGenerator("power")
        lows = set()
        for _ in range(100):
            result = gen.generate()
            lows.add(int(re.search(r"k=(-?\d+)", result["problem"]).group(1)))
        self.assertIn(0, lows)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"sigma_notation_linear",
                               "sigma_notation_square",
                               "sigma_notation_power"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            SigmaNotationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
