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

from generators.lhopital_generator import LHopitalGenerator
from helpers import DELIM


def to_fn(expr):
    """Limit body -> callable, for the handful of shapes used."""
    s = expr.replace("^", "**")
    s = re.sub(r"sin\((\d+)x\)", r"math.sin(\1*x)", s)
    s = re.sub(r"cos\((\d+)x\)", r"math.cos(\1*x)", s)
    s = re.sub(r"e\*\*\((\d+)x\)", r"math.exp(\1*x)", s)
    s = s.replace("ln(x)", "math.log(x)")
    s = re.sub(r"(\d)x", r"\1*x", s)
    s = re.sub(r"(\d)\(", r"\1*(", s)
    s = re.sub(r"\)\(", ")*(", s)
    return lambda x: eval(s, {"math": math, "x": x})


def oracle_check(example):
    m = re.fullmatch(r"Evaluate lim x→(-?\d+) of (.+) using L'Hôpital's "
                     r"rule\.", example["problem"])
    assert m, example["problem"]
    a, body = int(m.group(1)), m.group(2)
    f = to_fn(body)
    want = float(Fraction(example["final_answer"]))
    eps = 1e-6
    lo, hi = f(a - eps), f(a + eps)
    return abs(lo - want) < 1e-3 and abs(hi - want) < 1e-3


class TestLHopitalGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LHopitalGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_numeric_limits(self):
        """A9 oracle: numeric evaluation on both sides of the point."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_indeterminate_checked_before_each_application(self):
        for _ in range(200):
            result = self.gen.generate()
            checks = [s for s in result["steps"]
                      if s.startswith(f"CHECK{DELIM}")]
            self.assertGreaterEqual(len(checks), 1)
            self.assertTrue(all("0/0" in c for c in checks))

    def test_double_applies_twice(self):
        gen = LHopitalGenerator("double")
        for _ in range(100):
            result = gen.generate()
            checks = [s for s in result["steps"]
                      if s.startswith(f"CHECK{DELIM}")]
            self.assertEqual(len(checks), 2)
            self.assertIn("again", checks[1])

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            LHopitalGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
