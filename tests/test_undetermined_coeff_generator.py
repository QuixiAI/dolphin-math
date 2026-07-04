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

from generators.undetermined_coeff_generator import UndeterminedCoeffGenerator
from helpers import DELIM


def fmt_terms(raw_terms):
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        text = body if body and abs(coeff) == 1 else (
            f"{abs(coeff)}{body}" if body else str(abs(coeff))
        )
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def ode_lhs(p, q):
    return fmt_terms([(1, "y''"), (p, "y'"), (q, "y")])


def char_poly(p, q):
    return fmt_terms([(1, "r^2"), (p, "r"), (q, "")])


def exp_text(rate):
    if rate == 1:
        return "e^x"
    if rate == -1:
        return "e^(-x)"
    return f"e^({rate}x)"


def coeff_exp_text(coeff, rate):
    if coeff == 1:
        return exp_text(rate)
    if coeff == -1:
        return f"-{exp_text(rate)}"
    return f"{coeff}{exp_text(rate)}"


def factor_text(root):
    return f"(r - {root})" if root > 0 else f"(r + {abs(root)})"


def signed_join(terms):
    return fmt_terms(terms)


def hom_symbolic(r1, r2):
    return f"C1{exp_text(r1)} + C2{exp_text(r2)}"


def solution_text(c1, r1, c2, r2, particular_terms):
    return "y = " + signed_join(
        [(c1, exp_text(r1)), (c2, exp_text(r2))] + particular_terms
    )


def constant_equation_terms(a, b):
    return signed_join([(a, "C1"), (b, "C2")])


def plus_value(value):
    return f"+ {value}" if value > 0 else f"- {abs(value)}"


def split_terms(expr):
    if expr == "0":
        return []
    return [raw for raw in expr.replace(" - ", " + -").split(" + ")
            if raw]


def parse_ode_lhs(lhs):
    coeffs = {"y''": 0, "y'": 0, "y": 0}
    for raw in split_terms(lhs):
        sign = -1 if raw.startswith("-") else 1
        raw = raw[1:] if raw.startswith("-") else raw
        if raw == "y''":
            coeffs["y''"] += sign
        elif raw.endswith("y'"):
            prefix = raw[:-2]
            coeffs["y'"] += sign * (int(prefix) if prefix else 1)
        elif raw.endswith("y"):
            prefix = raw[:-1]
            coeffs["y"] += sign * (int(prefix) if prefix else 1)
        else:
            raise AssertionError(f"bad term {raw!r}")
    assert coeffs["y''"] == 1
    return coeffs["y'"], coeffs["y"]


def parse_coeff(text):
    if text in ("", "+"):
        return 1
    if text == "-":
        return -1
    return int(text)


def parse_rate(text):
    if text == "x":
        return 1
    inner = text[1:-1].removesuffix("x")
    if inner == "-":
        return -1
    return int(inner)


def parse_rhs(rhs):
    match = re.fullmatch(r"(-?\d*)e\^(x|\(-?\d*x\))", rhs)
    if match:
        return "exponential_forcing", parse_coeff(match.group(1)), parse_rate(
            match.group(2)
        )
    return "constant_forcing", int(rhs), None


def parse_problem(problem):
    match = re.fullmatch(
        r"Solve (.+) = (.+) with y\(0\) = (-?\d+) and y'\(0\) = "
        r"(-?\d+) by undetermined coefficients\.",
        problem,
    )
    assert match is not None, problem
    lhs, rhs, y0, v0 = match.groups()
    p, q = parse_ode_lhs(lhs)
    kind, rhs_coeff, rate = parse_rhs(rhs)
    return lhs, p, q, rhs, kind, rhs_coeff, rate, int(y0), int(v0)


def roots_from_coeffs(p, q):
    disc = p * p - 4 * q
    root = math.isqrt(disc)
    assert root * root == disc
    r1 = Fraction(-p - root, 2)
    r2 = Fraction(-p + root, 2)
    assert r1.denominator == 1 and r2.denominator == 1
    return sorted((r1.numerator, r2.numerator))


def constants_from_sum_deriv(r1, r2, hom_sum, hom_deriv):
    c1 = Fraction(hom_deriv - r2 * hom_sum, r1 - r2)
    c2 = Fraction(hom_sum) - c1
    assert c1.denominator == 1 and c2.denominator == 1
    return c1.numerator, c2.numerator


def oracle_parts(example):
    lhs, p, q, rhs, variant, rhs_coeff, rate, y0, v0 = parse_problem(
        example["problem"]
    )
    r1, r2 = roots_from_coeffs(p, q)
    if variant == "constant_forcing":
        A_part = Fraction(rhs_coeff, q)
        assert A_part.denominator == 1
        A_part = A_part.numerator
        hom_sum = y0 - A_part
        hom_deriv = v0
        c1, c2 = constants_from_sum_deriv(r1, r2, hom_sum, hom_deriv)
        answer = solution_text(c1, r1, c2, r2, [(A_part, "")])
    else:
        denom = rate * rate + p * rate + q
        A_part = Fraction(rhs_coeff, denom)
        assert A_part.denominator == 1
        A_part = A_part.numerator
        hom_sum = y0 - A_part
        hom_deriv = v0 - rate * A_part
        c1, c2 = constants_from_sum_deriv(r1, r2, hom_sum, hom_deriv)
        answer = solution_text(c1, r1, c2, r2,
                               [(A_part, exp_text(rate))])
    return {
        "variant": variant,
        "lhs": lhs,
        "p": p,
        "q": q,
        "rhs": rhs,
        "rhs_coeff": rhs_coeff,
        "rate": rate,
        "r1": r1,
        "r2": r2,
        "A_part": A_part,
        "hom_sum": hom_sum,
        "hom_deriv": hom_deriv,
        "c1": c1,
        "c2": c2,
        "y0": y0,
        "v0": v0,
        "answer": answer,
    }


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def solution_values(parts, x):
    r1, r2 = parts["r1"], parts["r2"]
    c1, c2 = parts["c1"], parts["c2"]
    e1 = math.exp(r1 * x)
    e2 = math.exp(r2 * x)
    y = c1 * e1 + c2 * e2
    yp = c1 * r1 * e1 + c2 * r2 * e2
    ypp = c1 * r1 * r1 * e1 + c2 * r2 * r2 * e2
    if parts["variant"] == "constant_forcing":
        y += parts["A_part"]
    else:
        k = parts["rate"]
        ep = math.exp(k * x)
        y += parts["A_part"] * ep
        yp += parts["A_part"] * k * ep
        ypp += parts["A_part"] * k * k * ep
    return y, yp, ypp


def solution_satisfies_ode(example):
    parts = oracle_parts(example)
    x = 0.29
    y, yp, ypp = solution_values(parts, x)
    left = ypp + parts["p"] * yp + parts["q"] * y
    if parts["variant"] == "constant_forcing":
        rhs = parts["rhs_coeff"]
    else:
        rhs = parts["rhs_coeff"] * math.exp(parts["rate"] * x)
    y0, v0, _ = solution_values(parts, 0)
    return (abs(left - rhs) < 1e-8 and
            abs(y0 - parts["y0"]) < 1e-9 and
            abs(v0 - parts["v0"]) < 1e-9)


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "ODE_SETUP":
            expected = [
                f"{ode_lhs(parts['p'], parts['q'])} = {parts['rhs']}",
                f"y(0) = {parts['y0']}, y'(0) = {parts['v0']}",
            ]
            if fields[1:] != expected:
                return False
        elif op == "CHAR_EQ":
            if fields[1:] != ["assume y=e^(rx)",
                              f"{char_poly(parts['p'], parts['q'])} = 0"]:
                return False
        elif op == "FACTOR":
            expected = f"{factor_text(parts['r1'])}{factor_text(parts['r2'])} = 0"
            if fields[1:] != [char_poly(parts["p"], parts["q"]), expected]:
                return False
        elif op == "HOM_SOL":
            if fields[1:] != ["y_h",
                              f"y_h = {hom_symbolic(parts['r1'], parts['r2'])}"]:
                return False
        elif op == "APPLY_OPERATOR":
            if parts["variant"] == "constant_forcing":
                expected = ["L[A]",
                            f"{parts['q']}A = {parts['rhs_coeff']}"]
            else:
                k = parts["rate"]
                k2 = k * k
                pk = parts["p"] * k
                expected = [
                    f"L[A{exp_text(k)}]",
                    f"A({fmt_terms([(k2, ''), (pk, ''), (parts['q'], '')])})"
                    f"{exp_text(k)}",
                ]
            if fields[1:] != expected:
                return False
        elif op == "M":
            if int(fields[1]) * int(fields[2]) != int(fields[3]):
                return False
        elif op == "A":
            if int(fields[1]) + int(fields[2]) != int(fields[3]):
                return False
        elif op == "S":
            if int(fields[1]) - int(fields[2]) != int(fields[3]):
                return False
        elif op == "D":
            if Fraction(int(fields[1]), int(fields[2])) != int(fields[3]):
                return False
        elif op == "PARTICULAR":
            if parts["variant"] == "constant_forcing":
                expected = ["y_p", str(parts["A_part"])]
            else:
                expected = ["y_p",
                            coeff_exp_text(parts["A_part"], parts["rate"])]
            if fields[1:] != expected:
                return False
        elif op == "SOLVE_CONST":
            if fields[1:] != [f"C1 = {parts['c1']}",
                              f"C2 = {parts['c2']}"]:
                return False
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    return True


class TestUndeterminedCoeffGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = UndeterminedCoeffGenerator()

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

    def test_solution_satisfies_ode_and_initial_conditions(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(solution_satisfies_ode(result), result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_variants_are_available(self):
        for variant in ("constant_forcing", "exponential_forcing"):
            gen = UndeterminedCoeffGenerator(variant)
            for _ in range(80):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"undetermined_coeff_{variant}")
                self.assertEqual(oracle_parts(result)["variant"], variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            UndeterminedCoeffGenerator("bogus")

    def test_no_degenerate_rendering(self):
        bad = re.compile(
            r"(?<![A-Za-z0-9])1y|(?<![A-Za-z0-9])1r|"
            r"(?<![A-Za-z0-9])1e|1C|\+ -|--"
        )
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
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
