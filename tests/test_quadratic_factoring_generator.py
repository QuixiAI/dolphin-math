import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.quadratic_factoring_generator import QuadraticFactoringGenerator
from helpers import DELIM


def oracle_roots(example):
    """Independently derives the roots from the problem text alone."""
    expr = example["problem"].split(": ", 1)[1]
    var = next(v for v in "xyn" if v in expr)

    m = re.fullmatch(
        rf"(\d*){var}\^2 ([+-]) (\d*){var}(?: ([+-]) (\d+))? = (-?\d+)", expr)
    assert m, expr
    a = int(m.group(1) or 1)
    b = int(m.group(3) or 1) * (1 if m.group(2) == "+" else -1)
    c = int(m.group(5) or 0) * (1 if (m.group(4) or "+") == "+" else -1)
    rhs = int(m.group(6))
    c -= rhs  # move rhs across: ax² + bx + c = 0

    if a != 1:                      # gcf variant: ax² + bx = 0
        assert c == 0
        assert b % a == 0
        return var, sorted((0, -b // a))
    # monic with integer roots
    for p in range(-90, 91):
        if p != 0 or c == 0:
            q_num = -b - p
            if p * q_num == c:
                return var, sorted((p, q_num))
    raise AssertionError(f"no integer roots for {expr}")


class TestQuadraticFactoringGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = QuadraticFactoringGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_roots_and_answer_format(self):
        """A9 oracle: roots re-derived from the problem text; answer is
        'x = r1 or x = r2' with roots ascending (A0)."""
        for _ in range(400):
            result = self.gen.generate()
            var, roots = oracle_roots(result)
            self.assertEqual(result["final_answer"],
                             f"{var} = {roots[0]} or {var} = {roots[1]}",
                             result["problem"])

    def test_check_substitutions_are_zero(self):
        """Each CHECK substitutes a root and must land exactly on 0."""
        for _ in range(400):
            result = self.gen.generate()
            checks = [s for s in result["steps"]
                      if s.startswith(f"CHECK{DELIM}")]
            self.assertEqual(len(checks), 2)
            for s in checks:
                f = s.split(DELIM)
                self.assertEqual(f[2].rsplit("= ", 1)[1], "0", s)
                self.assertEqual(f[3], "0", s)

    def test_zero_product_split_matches_roots(self):
        for _ in range(300):
            result = self.gen.generate()
            var, roots = oracle_roots(result)
            zp = next(s for s in result["steps"]
                      if s.startswith(f"ZERO_PRODUCT{DELIM}"))
            split = zp.split(DELIM)[2]
            self.assertIn(" or ", split)
            results = [s.split(DELIM) for s in result["steps"]
                       if s.startswith(f"EQ_RESULT{DELIM}")]
            self.assertEqual(sorted(int(f[2]) for f in results), roots)

    def test_variants_reachable_and_structured(self):
        seen = set()
        moves = 0
        for _ in range(150):
            result = self.gen.generate()
            seen.add(result["operation"])
            if any(s.startswith(f"MOVE_TERM{DELIM}") for s in result["steps"]):
                moves += 1
        self.assertEqual(seen, {"quadratic_by_factoring",
                                "quadratic_by_factoring_gcf"})
        self.assertGreater(moves, 20, "rearrange variant should appear")

    def test_trial_and_error_present_for_trinomials(self):
        gen = QuadraticFactoringGenerator("standard")
        for _ in range(50):
            result = gen.generate()
            codes = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertIn("TRY", codes)
            self.assertIn("ACCEPT", codes)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            QuadraticFactoringGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
