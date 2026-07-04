import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.integration_by_parts_generator import (
    IntegrationByPartsGenerator,
)
from helpers import DELIM


def to_py(expr):
    s = expr.replace("+ C", "").strip()
    s = s.replace("e^(-x)", "math.exp(-x)").replace("e^x", "math.exp(x)")
    s = s.replace("sin(x)", "math.sin(x)").replace("cos(x)",
                                                   "math.cos(x)")
    s = s.replace("ln(x)", "math.log(x)")
    s = re.sub(r"(\d)x", r"\1*x", s)
    s = re.sub(r"(\d)·", r"\1*", s)
    s = re.sub(r"(\d) ?math", r"\1*math", s)
    s = re.sub(r"x ?math", "x*math", s)
    s = re.sub(r"x\(", "x*(", s)
    s = re.sub(r"(\d)\(", r"\1*(", s)
    s = re.sub(r"\)\(", ")*(", s)
    return s


def numeric_check(example):
    m = re.fullmatch(r"Find ∫ (.+) dx\.", example["problem"])
    integrand = to_py(m.group(1))
    F = to_py(example["final_answer"])
    for x in (0.6, 1.4, 2.3):
        h = 1e-6
        dF = (eval(F, {"math": math, "x": x + h}) -
              eval(F, {"math": math, "x": x - h})) / (2 * h)
        want = eval(integrand, {"math": math, "x": x})
        if abs(dF - want) / max(1.0, abs(want)) > 1e-3:
            return False
    return True


class TestIntegrationByPartsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = IntegrationByPartsGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_derivative_recovers_integrand(self):
        """A9 oracle: d/dx F equals the integrand numerically."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(numeric_check(result),
                            (result["problem"], result["final_answer"]))

    def test_parts_choice_recorded(self):
        for _ in range(200):
            result = self.gen.generate()
            choice = next(s for s in result["steps"]
                          if s.startswith(f"PARTS_CHOOSE{DELIM}"))
            self.assertIn("u = ", choice)
            self.assertIn("v = ", choice)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            IntegrationByPartsGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
