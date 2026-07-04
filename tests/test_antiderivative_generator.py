import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.antiderivative_generator import AntiderivativeGenerator
from helpers import DELIM


def to_py(expr):
    """Math text -> evaluable Python."""
    s = expr.replace("+ C", "").strip()
    s = re.sub(r"sec\^2\((\d*)x\)",
               lambda m: f"(1/math.cos({m.group(1) or 1}*x)**2)", s)
    s = s.replace("^", "**")
    s = re.sub(r"(sin|cos|tan)\((\d*)x\)",
               lambda m: f"math.{m.group(1)}({m.group(2) or 1}*x)", s)
    s = s.replace("ln(abs(x))", "math.log(abs(x))")
    s = re.sub(r"e\*\*\((\d+)x\)", r"math.exp(\1*x)", s)
    s = re.sub(r"(\d)x", r"\1*x", s)
    s = re.sub(r"(\d) ?math", r"\1*math", s)
    s = re.sub(r"(\d) \(", r"\1*(", s)
    return s


def numeric_check(example):
    """F'(x) must equal the integrand at sample points."""
    m = re.fullmatch(r"Find ∫ (.+) dx\.", example["problem"])
    body = m.group(1)
    if body.startswith("(") and body.endswith(")"):
        body = body[1:-1]
    integrand = to_py(body)
    F = to_py(example["final_answer"])
    for x in (0.7, 1.3, 2.1):
        h = 1e-6
        f_hi = eval(F, {"math": math, "x": x + h})
        f_lo = eval(F, {"math": math, "x": x - h})
        dF = (f_hi - f_lo) / (2 * h)
        want = eval(integrand, {"math": math, "x": x})
        if abs(dF - want) / max(1.0, abs(want)) > 1e-3:
            return False
    return True


class TestAntiderivativeGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = AntiderivativeGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_derivative_recovers_integrand(self):
        """A9 oracle: d/dx of the claimed F equals the integrand."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(numeric_check(result),
                            (result["problem"], result["final_answer"]))

    def test_plus_c_always_present(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(result["final_answer"].endswith("+ C"))

    def test_division_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "D":
                    self.assertEqual(int(f[1]), int(f[2]) * int(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            AntiderivativeGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
