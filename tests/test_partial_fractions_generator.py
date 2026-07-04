import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.partial_fractions_generator import PartialFractionsGenerator
from helpers import DELIM


def to_py(expr):
    s = expr.replace("+ C", "").strip()
    s = s.replace("ln(abs(", "math.log(abs(")
    s = s.replace("^2", "**2")
    s = re.sub(r"(\d)x", r"\1*x", s)
    s = re.sub(r"(\d)math", r"\1*math", s)
    s = re.sub(r"(\d)\(", r"\1*(", s)
    s = re.sub(r"\)\(", ")*(", s)
    s = re.sub(r"x\(", "x*(", s)
    s = re.sub(r"\)x", ")*x", s)
    return s


def oracle_check(example):
    """A9 oracle: check the answer numerically far from all roots."""
    p = example["problem"]
    xs = (7.3, 8.6, 11.4)
    m = re.fullmatch(r"Decompose (.+) into partial fractions\.", p)
    if m:
        orig = to_py(m.group(1))
        dec = to_py(example["final_answer"])
        return all(abs(eval(orig, {"math": math, "x": x}) -
                       eval(dec, {"math": math, "x": x})) < 1e-9
                   for x in xs)
    m = re.fullmatch(r"Find ∫ (.+) dx\.", p)
    assert m, p
    integrand = to_py(m.group(1))
    F = to_py(example["final_answer"])
    h = 1e-6
    for x in xs:
        dF = (eval(F, {"math": math, "x": x + h}) -
              eval(F, {"math": math, "x": x - h})) / (2 * h)
        want = eval(integrand, {"math": math, "x": x})
        if abs(dF - want) > 1e-4 * max(1.0, abs(want)):
            return False
    return True


class TestPartialFractionsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PartialFractionsGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_matches_problem(self):
        """A9 oracle: decompositions and antiderivatives check out."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_pipe_safety(self):
        """No step field may contain a raw pipe (abs(), not bars)."""
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 5, s)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_setup_and_constants_steps_present(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"PARTFRAC_SETUP{DELIM}")
                                for s in result["steps"]))
            self.assertTrue(any(s.startswith(f"SUBST{DELIM}")
                                for s in result["steps"]))

    def test_no_degenerate_renders(self):
        for _ in range(300):
            result = self.gen.generate()
            joined = " ".join(result["steps"])
            for bad in ("1x", "--", "+ -", "- -", "/1 ", " 1ln"):
                self.assertNotIn(bad, joined, (bad, result["steps"]))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            PartialFractionsGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
