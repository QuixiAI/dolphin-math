import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.rational_root_generator import RationalRootGenerator
from tests.test_polynomial_long_division_generator import parse_poly
from helpers import DELIM


def poly_at(coefs, x):
    return sum(c * x ** p for p, c in coefs.items())


def get_coefs(example):
    m = re.fullmatch(r"Use the rational root theorem to find a rational "
                     r"root of P\(x\) = (.+)\.", example["problem"])
    assert m, example["problem"]
    return parse_poly(m.group(1), "x")


class TestRationalRootGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RationalRootGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_root_is_exact(self):
        """A9 oracle: the answer really is a root, exactly."""
        for _ in range(500):
            result = self.gen.generate()
            coefs = get_coefs(result)
            r = Fraction(result["final_answer"].replace("x = ", ""))
            self.assertEqual(poly_at(coefs, r), 0, result["problem"])

    def test_every_try_value_is_true_and_rejects_are_honest(self):
        for _ in range(300):
            result = self.gen.generate()
            coefs = get_coefs(result)
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "TRY":
                    cand = Fraction(f[1].replace("x = ", ""))
                    claimed = Fraction(f[2].split(" = ", 1)[1])
                    self.assertEqual(poly_at(coefs, cand), claimed, s)
                elif f[0] == "REJECT":
                    self.assertIn("≠ 0", f[2], s)

    def test_sweep_ends_with_accept_of_the_answer(self):
        for _ in range(300):
            result = self.gen.generate()
            accepts = [s for s in result["steps"]
                       if s.startswith(f"ACCEPT{DELIM}")]
            self.assertEqual(len(accepts), 1)
            self.assertEqual(accepts[0].split(DELIM)[1],
                             result["final_answer"])

    def test_root_is_in_candidate_list(self):
        for _ in range(300):
            result = self.gen.generate()
            cand_step = next(s for s in result["steps"]
                             if s.startswith(f"CANDIDATES{DELIM}"))
            cands = {Fraction(v.lstrip("±")) for v in
                     cand_step.split(DELIM)[1].split(", ")}
            r = Fraction(result["final_answer"].replace("x = ", ""))
            self.assertIn(abs(r), cands, cand_step)

    def test_sweep_order_is_by_magnitude_positive_first(self):
        for _ in range(200):
            result = self.gen.generate()
            tried = [Fraction(s.split(DELIM)[1].replace("x = ", ""))
                     for s in result["steps"]
                     if s.startswith(f"TRY{DELIM}")]
            keys = [(abs(v), v < 0) for v in tried]
            self.assertEqual(keys, sorted(keys), tried)

    def test_fraction_roots_occur(self):
        gen = RationalRootGenerator("fraction_root")
        for _ in range(50):
            result = gen.generate()
            self.assertIn("/", result["final_answer"])

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RationalRootGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
