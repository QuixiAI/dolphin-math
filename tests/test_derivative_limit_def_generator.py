import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.derivative_limit_def_generator import (
    DerivativeLimitDefGenerator,
)
from tests.test_polynomial_long_division_generator import (
    parse_poly,
    poly_value,
)
from helpers import DELIM


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"Use the limit definition of the derivative to "
                     r"find f'\(x\) for f\(x\) = (.+)\.", p)
    if m:
        coefs = parse_poly(m.group(1), "x")
        a = coefs.get(2, 0)
        b = coefs.get(1, 0)
        # derivative 2a x + b, rendered like poly_txt
        head = {1: "x", -1: "-x"}.get(2 * a, f"{2 * a}x")
        want = head if b == 0 else \
            f"{head} + {b}" if b > 0 else f"{head} - {-b}"
        return f"f'(x) = {want}"
    m = re.fullmatch(r"Use the limit definition of the derivative to "
                     r"find f'\((-?\d+)\) for f\(x\) = (.+)\.", p)
    assert m, p
    pt = int(m.group(1))
    coefs = parse_poly(m.group(2), "x")
    # numeric derivative via tiny secant, rounded
    h = 1e-7
    d = (poly_value(coefs, pt + h) - poly_value(coefs, pt)) / h
    return f"f'({pt}) = {round(d)}"


class TestDerivativeLimitDefGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DerivativeLimitDefGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: symbolic derivative or a numeric secant."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_h_factored_and_cancelled(self):
        for _ in range(200):
            result = self.gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertIn("FACTOR_GROUP", ops)
            self.assertIn("CANCEL", ops)
            self.assertLess(ops.index("FACTOR_GROUP"),
                            ops.index("CANCEL"))
            # the SUBST h -> 0 comes after the cancel
            last_subst = max(i for i, s in enumerate(result["steps"])
                             if s.startswith(f"SUBST{DELIM}"))
            self.assertGreater(last_subst, ops.index("CANCEL"))

    def test_at_point_numeric_work(self):
        gen = DerivativeLimitDefGenerator("at_point")
        for _ in range(200):
            result = gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1].strip("()")) ** int(f[2]),
                                     int(f[3]), s)

    def test_both_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"derivative_limit_general",
                               "derivative_limit_at_point"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            DerivativeLimitDefGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
