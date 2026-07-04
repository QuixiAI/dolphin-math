import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.derivative_product_quotient_generator import (
    DerivativeProductQuotientGenerator,
)
from helpers import DELIM


def parse_lin(txt):
    m = re.fullmatch(r"(-?\d*)x(?: ([+-]) (\d+))?", txt.strip("()"))
    assert m, txt
    a = int(m.group(1) + "1") if m.group(1) in ("", "-") \
        else int(m.group(1))
    b = int(m.group(3) or 0) * (1 if (m.group(2) or "+") == "+" else -1)
    return a, b


def numeric_check(example):
    """The claimed derivative matches a secant of the original."""
    p = example["problem"]
    ans = example["final_answer"].replace("y' = ", "")
    x, h = 1.37, 1e-7

    m = re.fullmatch(r"Differentiate y = \(x\^2 ([+-]) (\d+)\)"
                     r"\((.+)\)\.", p)
    if m:
        pp = int(m.group(2)) * (1 if m.group(1) == "+" else -1)
        c, d = parse_lin(m.group(3))

        def f(t):
            return (t * t + pp) * (c * t + d)
        # evaluate the claimed polynomial via safe substitution
        s = ans.replace("^", "**")
        s = re.sub(r"(\d)x", r"\1*x", s)
        s = re.sub(r"(?<![\d*])x", "1*x", s)
        val = eval(s, {"x": x})
        secant = (f(x + h) - f(x)) / h
        return abs(val - secant) < 1e-3
    m = re.fullmatch(r"Differentiate y = \((.+)\)/\((.+)\)\.", p)
    assert m, p
    a, b = parse_lin(m.group(1))
    c, d = parse_lin(m.group(2))
    # keep the test point well away from the pole of the denominator
    x = next(t for t in (1.37, 0.21, -0.53, 2.9, -3.1)
             if abs(c * t + d) > 0.7)

    def f(t):
        return (a * t + b) / (c * t + d)
    mm = re.fullmatch(r"(-?\d+)/\((.+)\)\^2", ans)
    assert mm, ans
    k = int(mm.group(1))
    c2, d2 = parse_lin(mm.group(2))
    assert (c2, d2) == (c, d)
    val = k / (c * x + d) ** 2
    secant = (f(x + h) - f(x)) / h
    return abs(val - secant) < 1e-3


class TestDerivativeProductQuotientGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DerivativeProductQuotientGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_numeric_secant(self):
        """A9 oracle: the claimed derivative matches a secant."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertTrue(numeric_check(result),
                            (result["problem"], result["final_answer"]))

    def test_rule_stated(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"DERIV_RULE{DELIM}")
                                for s in result["steps"]))

    def test_quotient_numerator_is_constant(self):
        gen = DerivativeProductQuotientGenerator("quotient")
        for _ in range(200):
            result = gen.generate()
            self.assertRegex(result["final_answer"],
                             r"^y' = -?\d+/\(.+\)\^2$")
            # x-terms cancelled explicitly
            self.assertTrue(any(s.startswith(f"COMB_X{DELIM}") and
                                s.endswith(f"{DELIM}0")
                                for s in result["steps"]))

    def test_both_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"derivative_product_rule",
                               "derivative_quotient_rule"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            DerivativeProductQuotientGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
