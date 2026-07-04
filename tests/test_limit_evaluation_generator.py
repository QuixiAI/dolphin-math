import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.limit_evaluation_generator import LimitEvaluationGenerator
from helpers import DELIM


def to_lambda(expr):
    """Converts a limit expression to a Python-evaluable function."""
    s = expr
    s = s.replace("√(", "math.sqrt(").replace("^", "**")
    s = re.sub(r"√(\d+)", r"math.sqrt(\1)", s)
    s = re.sub(r"(\d)x", r"\1*x", s)
    s = re.sub(r"(\d)\(", r"\1*(", s)
    s = re.sub(r"\)\(", ")*(", s)
    return lambda x: eval(s, {"math": math, "abs": abs, "x": x})


def claimed_value(ans):
    if ans == "∞":
        return math.inf
    if ans == "-∞":
        return -math.inf
    return float(Fraction(ans))


def oracle_check(example):
    """Numeric limit: evaluate near the point (or at huge x)."""
    m = re.fullmatch(r"Evaluate lim x→(-?\d+|∞)(⁻|⁺)? of (.+)\.",
                     example["problem"])
    assert m, example["problem"]
    target, side, expr = m.group(1), m.group(2), m.group(3)
    f = to_lambda(expr)
    want = claimed_value(example["final_answer"])
    if target == "∞":
        got = f(1e7)
        if math.isinf(want):
            return (got > 1e6) if want > 0 else (got < -1e6)
        return abs(got - want) < 1e-5
    a = int(target)
    eps = 1e-7
    if side == "⁻":
        return abs(f(a - eps) - want) < 1e-4
    if side == "⁺":
        return abs(f(a + eps) - want) < 1e-4
    return (abs(f(a + eps) - want) < 1e-4 and
            abs(f(a - eps) - want) < 1e-4)


class TestLimitEvaluationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LimitEvaluationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_numeric_limits(self):
        """A9 oracle: numeric evaluation near the limit point."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_indeterminate_forms_detected(self):
        for v in ("factor_cancel", "rationalize"):
            gen = LimitEvaluationGenerator(v)
            for _ in range(100):
                result = gen.generate()
                self.assertTrue(any("0/0" in s for s in result["steps"]),
                                result["steps"])

    def test_infinity_uses_degree_compare(self):
        gen = LimitEvaluationGenerator("infinity")
        answers = set()
        for _ in range(200):
            result = gen.generate()
            self.assertTrue(any(s.startswith(f"DEGREE_COMPARE{DELIM}")
                                for s in result["steps"]))
            a = result["final_answer"]
            answers.add("inf" if "∞" in a else ("zero" if a == "0"
                                                else "ratio"))
        self.assertEqual(answers, {"inf", "zero", "ratio"})

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 5)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            LimitEvaluationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
