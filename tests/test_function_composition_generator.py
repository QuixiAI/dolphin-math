import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.function_composition_generator import (
    FunctionCompositionGenerator,
)
from helpers import DELIM


def parse_rule(rule, var):
    """'3x + 5', 'x^2 - 4', '4t' -> callable."""
    m = re.fullmatch(rf"{var}\^2(?: ([+-]) (\d+))?", rule)
    if m:
        c = int(m.group(2) or 0) * (1 if (m.group(1) or "+") == "+" else -1)
        return lambda x: x * x + c
    m = re.fullmatch(rf"(-?\d+){var}(?: ([+-]) (\d+))?", rule)
    assert m, rule
    a = int(m.group(1))
    b = int(m.group(3) or 0) * (1 if (m.group(2) or "+") == "+" else -1)
    return lambda x: a * x + b


def compose_value(example, x):
    """True composed value at x, from the problem text."""
    p = example["problem"]
    m = re.fullmatch(
        r"Given ([a-z])\(([a-z])\) = (.+) and ([a-z])\(\2\) = (.+), "
        r"find (?:\((\w) ∘ (\w)\)|(\w)\((\w))\(?(-?\w+)\)+"
        r"( as a simplified expression)?\.", p)
    assert m, p
    var = m.group(2)
    rules = {m.group(1): parse_rule(m.group(3), var),
             m.group(4): parse_rule(m.group(5), var)}
    outer = m.group(6) or m.group(8)
    inner = m.group(7) or m.group(9)
    return rules[outer](rules[inner](x))


def poly_value(expr, var, x):
    """Evaluates an answer string like '6x - 5' or '3x^2 + 7' at x."""
    m = re.fullmatch(rf"(-?\d+){var}(\^2)?(?: ([+-]) (\d+))?", expr)
    assert m, expr
    a = int(m.group(1))
    c = int(m.group(4) or 0) * (1 if (m.group(3) or "+") == "+" else -1)
    return a * x * x + c if m.group(2) else a * x + c


class TestFunctionCompositionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FunctionCompositionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_numeric_oracle_from_problem_text(self):
        """A9 oracle: evaluate the composition inside-out independently."""
        gen = FunctionCompositionGenerator("numeric")
        for _ in range(500):
            result = gen.generate()
            m = re.search(r"\((-?\d+)\)+\.$", result["problem"])
            k = Fraction(m.group(1))
            self.assertEqual(str(compose_value(result, k)),
                             result["final_answer"], result["problem"])

    def test_symbolic_answer_matches_at_sample_points(self):
        """A9 oracle: the claimed rule agrees with the true composition."""
        gen = FunctionCompositionGenerator("symbolic")
        for _ in range(500):
            result = gen.generate()
            var = re.search(r"\(([a-z])\) =", result["problem"]).group(1)
            for x in (Fraction(0), Fraction(1), Fraction(-1), Fraction(3)):
                self.assertEqual(
                    poly_value(result["final_answer"], var, x),
                    compose_value(result, x),
                    result["problem"] + " -> " + result["final_answer"])

    def test_numeric_evaluates_inner_first(self):
        gen = FunctionCompositionGenerator("numeric")
        for _ in range(300):
            result = gen.generate()
            evals = [s.split(DELIM)[1] for s in result["steps"]
                     if s.startswith(f"EVAL{DELIM}")]
            self.assertEqual(len(evals), 2)
            # first EVAL is the inner call g(k); second is the nested call
            self.assertRegex(evals[0], r"^[a-z]\(-?\d+\)$")
            self.assertRegex(evals[1], r"^[a-z]\([a-z]\(-?\d+\)\)$")
            self.assertIn(evals[0], evals[1])

    def test_ring_notation_gets_funcop_unfold(self):
        for _ in range(300):
            result = self.gen.generate()
            has_ring = "∘" in result["problem"]
            has_unfold = any(s.startswith(f"FUNC_OP{DELIM}")
                             for s in result["steps"])
            self.assertEqual(has_ring, has_unfold, result["problem"])

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1].strip("()")) ** int(f[2]),
                                     int(f[3]), s)

    def test_symbolic_dist_is_correct(self):
        """DIST result equals multiplier times inner rule at sample points."""
        gen = FunctionCompositionGenerator("symbolic")
        for _ in range(300):
            result = gen.generate()
            var = re.search(r"\(([a-z])\) =", result["problem"]).group(1)
            d = next(s.split(DELIM) for s in result["steps"]
                     if s.startswith(f"DIST{DELIM}"))
            mult = int(d[1])
            for x in (Fraction(2), Fraction(-1)):
                inner_v = parse_rule(d[2], var)(x)
                self.assertEqual(poly_value(d[3], var, x), mult * inner_v, d)

    def test_all_variants_and_notations_reachable(self):
        ops, notations = set(), set()
        for _ in range(200):
            result = self.gen.generate()
            ops.add(result["operation"])
            notations.add("ring" if "∘" in result["problem"] else "nested")
        self.assertEqual(ops, {"function_composition_numeric",
                               "function_composition_symbolic"})
        self.assertEqual(notations, {"ring", "nested"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            FunctionCompositionGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
