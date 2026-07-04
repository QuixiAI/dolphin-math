import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.mean_value_theorem_generator import (
    MeanValueTheoremGenerator,
)
from tests.test_polynomial_long_division_generator import (
    parse_poly,
    poly_value,
)
from helpers import DELIM


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"Find the value c guaranteed by the Mean Value "
                     r"Theorem for f\(x\) = (.+) on "
                     r"\[(-?\d+), (-?\d+)\]\.", p)
    if m:
        coefs = parse_poly(m.group(1), "x")
        a1, a2 = int(m.group(2)), int(m.group(3))
        slope = (poly_value(coefs, a2) - poly_value(coefs, a1)) \
            // (a2 - a1)
        # f' = 2x + b -> c = (slope - b)/2
        b = coefs.get(1, 0)
        c = (slope - b) // 2
        assert a1 < c < a2
        # verify f'(c) equals the average slope exactly
        assert 2 * c + b == slope
        return f"c = {c}"
    m = re.fullmatch(r"Does the Intermediate Value Theorem guarantee "
                     r"that f\(x\) = (.+) has a root in "
                     r"\[(-?\d+), (-?\d+)\]\?", p)
    assert m, p
    coefs = parse_poly(m.group(1), "x")
    a1, a2 = int(m.group(2)), int(m.group(3))
    f1, f2 = poly_value(coefs, a1), poly_value(coefs, a2)
    if f1 * f2 < 0:
        return f"Yes — a root exists in ({a1}, {a2})"
    return "Inconclusive — the IVT does not guarantee a root here"


class TestMeanValueTheoremGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = MeanValueTheoremGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_mvt_theorem_and_interval_check(self):
        gen = MeanValueTheoremGenerator("mvt")
        for _ in range(200):
            result = gen.generate()
            self.assertTrue(any(s.startswith(f"THEOREM{DELIM}")
                                for s in result["steps"]))
            self.assertTrue(any("inside the interval" in s
                                for s in result["steps"]))

    def test_ivt_both_outcomes_occur(self):
        gen = MeanValueTheoremGenerator("ivt")
        outcomes = set()
        for _ in range(200):
            result = gen.generate()
            outcomes.add(result["final_answer"].startswith("Yes"))
        self.assertEqual(outcomes, {True, False})

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "E":
                    self.assertEqual(int(f[1].strip("()")) ** int(f[2]),
                                     int(f[3]), s)
                elif f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)

    def test_both_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"mvt_application", "ivt_application"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            MeanValueTheoremGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
