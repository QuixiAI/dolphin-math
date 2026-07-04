import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.lagrange_multiplier_generator import LagrangeMultiplierGenerator
from helpers import DELIM


def split_terms(expr):
    if expr == "0":
        return []
    return [raw for raw in expr.replace(" - ", " + -").split(" + ")
            if raw]


def parse_linear_coeffs(expr):
    coeffs = {"x": 0, "y": 0}
    const = 0
    for raw in split_terms(expr):
        sign = -1 if raw.startswith("-") else 1
        raw = raw[1:] if raw.startswith("-") else raw
        coeff = sign
        var = None
        for factor in raw.split("*"):
            if factor.isdigit():
                coeff *= int(factor)
            elif factor in coeffs:
                var = factor
            else:
                raise AssertionError(f"bad factor {factor!r} in {expr!r}")
        if var is None:
            const += coeff
        else:
            coeffs[var] += coeff
    return coeffs["x"], coeffs["y"], const


def parse_quadratic_objective(expr):
    a = 0
    b = 0
    for raw in split_terms(expr):
        sign = -1 if raw.startswith("-") else 1
        raw = raw[1:] if raw.startswith("-") else raw
        coeff = sign
        body = []
        for factor in raw.split("*"):
            if factor.isdigit():
                coeff *= int(factor)
            else:
                body.append(factor)
        if body == ["x^2"]:
            a += coeff
        elif body == ["y^2"]:
            b += coeff
        else:
            raise AssertionError(f"bad quadratic term {raw!r}")
    return a, b


def parse_product_objective(expr):
    exps = {"x": 0, "y": 0}
    for factor in expr.split("*"):
        if factor in exps:
            exps[factor] += 1
        elif factor.startswith("x^"):
            exps["x"] += int(factor[2:])
        elif factor.startswith("y^"):
            exps["y"] += int(factor[2:])
        else:
            raise AssertionError(f"bad product factor {factor!r}")
    return exps["x"], exps["y"]


def oracle_answer(example):
    problem = example["problem"]
    if problem.startswith("Minimize"):
        f_txt, constraint = re.fullmatch(
            r"Minimize f\(x,y\) = (.+) subject to (.+) using "
            r"Lagrange multipliers\.",
            problem,
        ).groups()
        left, rhs = constraint.rsplit(" = ", 1)
        a, b = parse_quadratic_objective(f_txt)
        p, q, const = parse_linear_coeffs(left)
        assert const == 0
        r = Fraction(rhs)
        denom = Fraction(p * p, 2 * a) + Fraction(q * q, 2 * b)
        lam = r / denom
        x0 = lam * p / (2 * a)
        y0 = lam * q / (2 * b)
        value = a * x0 * x0 + b * y0 * y0
        assert x0.denominator == y0.denominator == value.denominator == 1
        return (f"minimum at ({x0.numerator}, {y0.numerator}); "
                f"value {value.numerator}")

    f_txt, total = re.fullmatch(
        r"Maximize f\(x,y\) = (.+) subject to x \+ y = (\d+), "
        r"with x > 0 and y > 0, using Lagrange multipliers\.",
        problem,
    ).groups()
    m, n = parse_product_objective(f_txt)
    total = int(total)
    x0 = Fraction(m * total, m + n)
    y0 = Fraction(n * total, m + n)
    value = (x0 ** m) * (y0 ** n)
    assert x0.denominator == y0.denominator == value.denominator == 1
    return f"maximum at ({x0.numerator}, {y0.numerator}); value {value.numerator}"


def parse_factor(text):
    text = text.strip()
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]
    return Fraction(text)


def eval_product_ratio(expr):
    top, bottom = expr.split("/")
    product = Fraction(1)
    for factor in top.split("*"):
        product *= parse_factor(factor)
    return product / parse_factor(bottom)


def eval_arith(expr):
    return Fraction(eval(expr.replace("^", "**"),
                         {"__builtins__": {}}, {}))


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "POINT_FROM_LAMBDA":
            if eval_product_ratio(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] == "CONSTRAINT_SUBST" and parts[2].startswith(("x =", "y =")):
            if eval_product_ratio(parts[2].split(" = ", 1)[1]) != Fraction(parts[3]):
                return False
        elif parts[0] == "EVAL":
            if eval_arith(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] == "CHECK" and parts[1] == "constraint":
            left, right = parts[2].split(" = ")
            if eval_arith(left) != Fraction(right) or parts[3] != "satisfied":
                return False
    return True


class TestLagrangeMultiplierGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LagrangeMultiplierGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_variant_goals(self):
        cases = {
            "quadratic_line": "minimum",
            "product_sum": "maximum",
        }
        for variant, word in cases.items():
            gen = LagrangeMultiplierGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertIn(word, result["final_answer"])

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1\*|\+ 0|--")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 2)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            LagrangeMultiplierGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
