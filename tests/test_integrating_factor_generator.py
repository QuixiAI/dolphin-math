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

from generators.integrating_factor_generator import IntegratingFactorGenerator
from helpers import DELIM


def exp_text(rate):
    if rate == 1:
        return "e^x"
    if rate == -1:
        return "e^(-x)"
    return f"e^({rate}x)"


def term_text(coeff, rate=None):
    if rate is None:
        return str(abs(coeff))
    body = exp_text(rate)
    return body if abs(coeff) == 1 else f"{abs(coeff)}{body}"


def coeff_exp_text(coeff, rate):
    if coeff == 1:
        return exp_text(rate)
    if coeff == -1:
        return f"-{exp_text(rate)}"
    return f"{coeff}{exp_text(rate)}"


def left_side_text(a):
    return "y' + y" if a == 1 else f"y' + {a}y"


def if_left_text(a):
    if a == 1:
        return f"{exp_text(a)}y' + {exp_text(a)}y"
    return f"{exp_text(a)}y' + {a}{exp_text(a)}y"


def solution_text(terms):
    pieces = []
    for coeff, rate in terms:
        if coeff == 0:
            continue
        body = term_text(coeff, rate)
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return "y = " + " ".join(pieces)


def parse_left_side(text):
    if text == "y' + y":
        return 1
    match = re.fullmatch(r"y' \+ (\d+)y", text)
    assert match is not None, text
    return int(match.group(1))


def parse_rhs(text):
    match = re.fullmatch(r"(?:(\d+))?e\^(?:x|\((\d+)x\))", text)
    if match:
        coeff = int(match.group(1) or 1)
        rate = int(match.group(2) or 1)
        return coeff, rate
    return int(text), None


def parse_problem(problem):
    match = re.fullmatch(
        r"Solve (y' \+ (?:\d+y|y)) = (.+) with y\(0\) = (-?\d+) "
        r"using an integrating factor\.",
        problem,
    )
    assert match is not None, problem
    a = parse_left_side(match.group(1))
    rhs_coeff, rhs_rate = parse_rhs(match.group(2))
    y0 = int(match.group(3))
    return a, rhs_coeff, rhs_rate, y0


def oracle_parts(example):
    a, rhs_coeff, rhs_rate, y0 = parse_problem(example["problem"])
    if rhs_rate is None:
        m = Fraction(rhs_coeff, a)
        assert m.denominator == 1
        C = y0 - m.numerator
        answer = solution_text([(m.numerator, None), (C, -a)])
        return {
            "variant": "constant_rhs",
            "a": a,
            "b": rhs_coeff,
            "m": m.numerator,
            "C": C,
            "y0": y0,
            "answer": answer,
        }
    denom = a + rhs_rate
    m = Fraction(rhs_coeff, denom)
    assert m.denominator == 1
    C = y0 - m.numerator
    answer = solution_text([(m.numerator, rhs_rate), (C, -a)])
    return {
        "variant": "exponential_rhs",
        "a": a,
        "k": rhs_rate,
        "c": rhs_coeff,
        "denom": denom,
        "m": m.numerator,
        "C": C,
        "y0": y0,
        "answer": answer,
    }


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    a = parts["a"]
    y0 = parts["y0"]
    m = parts["m"]
    C = parts["C"]
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "ODE_SETUP":
            if parts["variant"] == "constant_rhs":
                expected = f"{left_side_text(a)} = {parts['b']}, y(0) = {y0}"
            else:
                expected = (
                    f"{left_side_text(a)} = "
                    f"{coeff_exp_text(parts['c'], parts['k'])}, y(0) = {y0}"
                )
            if fields[1:] != [expected, "integrating factor"]:
                return False
        elif op == "IFACTOR":
            if fields[1:] != [f"mu = e^(∫ {a} dx)", exp_text(a)]:
                return False
        elif op == "MULTIPLY_IF":
            if parts["variant"] == "constant_rhs":
                expected_rhs = coeff_exp_text(parts["b"], a)
            else:
                expected_rhs = coeff_exp_text(parts["c"], a + parts["k"])
            if fields[1:] != [if_left_text(a), expected_rhs]:
                return False
        elif op == "REWRITE":
            if parts["variant"] == "constant_rhs":
                rhs = coeff_exp_text(parts["b"], a)
            else:
                rhs = coeff_exp_text(parts["c"], a + parts["k"])
            if fields[1:] != [f"({exp_text(a)}y)' = {rhs}"]:
                return False
        elif op == "A":
            if int(fields[1]) + int(fields[2]) != int(fields[3]):
                return False
        elif op == "D":
            if Fraction(int(fields[1]), int(fields[2])) != int(fields[3]):
                return False
        elif op == "ANTIDERIV":
            if parts["variant"] == "constant_rhs":
                integrand = coeff_exp_text(parts["b"], a)
                antiderivative = coeff_exp_text(m, a)
            else:
                integrand = coeff_exp_text(parts["c"], a + parts["k"])
                antiderivative = coeff_exp_text(m, a + parts["k"])
            if fields[1:] != [f"{integrand} dx", f"{antiderivative} + C"]:
                return False
        elif op == "SOLVE_Y":
            if parts["variant"] == "constant_rhs":
                left = f"{exp_text(a)}y = {coeff_exp_text(m, a)} + C"
                right = f"y = {m} + C{exp_text(-a)}"
            else:
                left = f"{exp_text(a)}y = {coeff_exp_text(m, a + parts['k'])} + C"
                right = f"y = {coeff_exp_text(m, parts['k'])} + C{exp_text(-a)}"
            if fields[1:] != [left, right]:
                return False
        elif op == "SUBST":
            if fields[1:] != ["x", "0", f"{y0} = {m} + C"]:
                return False
        elif op == "S":
            if int(fields[1]) - int(fields[2]) != int(fields[3]):
                return False
            if int(fields[3]) != C:
                return False
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    return True


def satisfies_ode(example):
    parts = oracle_parts(example)
    a = parts["a"]
    x = 0.37
    if parts["variant"] == "constant_rhs":
        m = parts["m"]
        C = parts["C"]
        y = m + C * math.exp(-a * x)
        y_prime = -a * C * math.exp(-a * x)
        rhs = parts["b"]
    else:
        m = parts["m"]
        k = parts["k"]
        C = parts["C"]
        y = m * math.exp(k * x) + C * math.exp(-a * x)
        y_prime = m * k * math.exp(k * x) - a * C * math.exp(-a * x)
        rhs = parts["c"] * math.exp(k * x)
    return abs((y_prime + a * y) - rhs) < 1e-9


class TestIntegratingFactorGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = IntegratingFactorGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_solution_satisfies_ode_and_initial_value(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = oracle_parts(result)
            self.assertEqual(parts["m"] + parts["C"], parts["y0"])
            self.assertTrue(satisfies_ode(result), result["problem"])

    def test_variants_are_available(self):
        for variant in ("constant_rhs", "exponential_rhs"):
            gen = IntegratingFactorGenerator(variant)
            for _ in range(100):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"integrating_factor_{variant}")
                self.assertEqual(oracle_parts(result)["variant"], variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            IntegratingFactorGenerator("bogus")

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1y|(?<!\d)1e|\+ -|--|e\^\(1x\)|e\^\(-1x\)")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))
            for raw_step in result["steps"]:
                self.assertIsNone(bad.search(raw_step), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                self.assertLessEqual(len(fields), 5, raw_step)
                self.assertNotIn("", fields[:1])


if __name__ == "__main__":
    unittest.main()
