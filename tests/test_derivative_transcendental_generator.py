import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.derivative_transcendental_generator import (
    DerivativeTranscendentalGenerator,
)
from helpers import DELIM


def to_py(expr):
    """Converts the generator's math text into evaluable Python."""
    s = expr
    s = re.sub(r"sec\^2\(([^)]+)\)", r"(1/@COS@(\1)**2)", s)
    s = s.replace("sin(", "@SIN@(").replace("cos(", "@COS@(")
    s = s.replace("tan(", "@TAN@(").replace("ln(", "@LOG@(")
    s = re.sub(r"e\^\(([^)]+)\)", r"@EXP@(\1)", s)
    s = re.sub(r"(\d+)\^x", r"\1**x", s)
    s = re.sub(r"ln (\d+)", r"*@LOG@(\1)", s)
    s = s.replace("·", "*")
    s = re.sub(r"(\d)x", r"\1*x", s)
    s = re.sub(r"(\d) ?@", r"\1*@", s)
    s = re.sub(r"(\d) \(", r"\1*(", s)
    s = re.sub(r"x ?@", "x*@", s)
    s = s.replace("@COS@", "math.cos").replace("@SIN@", "math.sin") \
        .replace("@TAN@", "math.tan").replace("@LOG@", "math.log") \
        .replace("@EXP@", "math.exp")
    return s


def numeric_check(example):
    m = re.fullmatch(r"Differentiate y = (.+)\.", example["problem"])
    body = to_py(m.group(1))
    ans = to_py(example["final_answer"].replace("y' = ", ""))
    ok_points = 0
    for x in (0.43, 0.91, 1.37, 9.7):
        try:
            h = 1e-6
            f_hi = eval(body, {"math": math, "x": x + h})
            f_lo = eval(body, {"math": math, "x": x - h})
            secant = (f_hi - f_lo) / (2 * h)
            claimed = eval(ans, {"math": math, "x": x})
        except ValueError:
            continue  # outside a log domain; try another point
        scale = max(1.0, abs(claimed))
        if abs(secant - claimed) / scale > 1e-3:
            return False
        ok_points += 1
    return ok_points >= 1


class TestDerivativeTranscendentalGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DerivativeTranscendentalGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_numeric_secant(self):
        """A9 oracle: central-difference agreement."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(numeric_check(result),
                            (result["problem"], result["final_answer"]))

    def test_ln_kx_collapses_to_c_over_x(self):
        gen = DerivativeTranscendentalGenerator("log")
        found = False
        for _ in range(200):
            result = gen.generate()
            if re.search(r"ln\(\dx\)", result["problem"]):
                found = True
                self.assertRegex(result["final_answer"],
                                 r"^y' = -?\d*/x$|^y' = 1/x$")
                self.assertTrue(any(s.startswith(f"CANCEL{DELIM}")
                                    for s in result["steps"]))
        self.assertTrue(found)

    def test_rule_always_stated(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"DERIV_RULE{DELIM}")
                                for s in result["steps"]))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            DerivativeTranscendentalGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
