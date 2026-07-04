import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.separable_ode_generator import SeparableODEGenerator
from helpers import DELIM


def oracle_check(example):
    """Verify the solution satisfies the ODE and IC numerically."""
    p = example["problem"]
    ans = example["final_answer"]
    h = 1e-6

    m = re.fullmatch(r"Solve dy/dt = (-?\d+)y with y\(0\) = (\d+)\.", p)
    if m:
        k, y0 = int(m.group(1)), int(m.group(2))
        mm = re.fullmatch(r"y = (\d+)e\^\((-?\d*)t\)", ans)
        if not mm:
            return False
        A = int(mm.group(1))
        kk = mm.group(2)
        kk = int(kk + "1") if kk in ("", "-") else int(kk)

        def y(t):
            return A * math.exp(kk * t)
        dy = (y(0.5 + h) - y(0.5 - h)) / (2 * h)
        return A == y0 and abs(dy - k * y(0.5)) < 1e-3
    m = re.fullmatch(r"A quantity satisfies dy/dt = ky and (doubles|"
                     r"halves) every (\d+) hours\. Find k exactly\.", p)
    if m:
        T = int(m.group(2))
        want = (f"k = ln(2)/{T}" if m.group(1) == "doubles"
                else f"k = -ln(2)/{T}")
        return ans == want
    m = re.fullmatch(r"Solve dy/dx = x\^2/y\^2 with y\(0\) = (\d+)\.", p)
    if m:
        c = int(m.group(1))
        mm = re.fullmatch(r"y = ∛\(x\^3 \+ (\d+)\)", ans)
        if not mm or int(mm.group(1)) != c ** 3:
            return False

        def y(x):
            return (x ** 3 + c ** 3) ** (1 / 3)
        x = 0.8
        dy = (y(x + h) - y(x - h)) / (2 * h)
        return abs(dy - x * x / y(x) ** 2) < 1e-3 and \
            abs(y(0) - c) < 1e-9
    m = re.fullmatch(r"Solve dy/dx = y\^2 with y\(0\) = (\d+)\.", p)
    assert m, p
    a = int(m.group(1))
    mm = re.fullmatch(r"y = (\d+)/\(1 - (\d*)x\)", ans)
    if not mm:
        return False
    A = int(mm.group(1))
    B = int(mm.group(2) or 1)
    if A != a or B != a:
        return False

    def y(x):
        return A / (1 - B * x)
    x = 0.1 / a
    dy = (y(x + h) - y(x - h)) / (2 * h)
    return abs(dy - y(x) ** 2) < 1e-2 and abs(y(0) - a) < 1e-9


class TestSeparableODEGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SeparableODEGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_solution_satisfies_ode(self):
        """A9 oracle: the solution satisfies the ODE and the IC."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_separate_step_present(self):
        for v in ("exponential", "power", "reciprocal"):
            gen = SeparableODEGenerator(v)
            for _ in range(50):
                result = gen.generate()
                self.assertTrue(any(s.startswith(f"SEPARATE{DELIM}")
                                    for s in result["steps"]))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            SeparableODEGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
