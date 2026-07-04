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

from generators.laplace_ivp_generator import LaplaceIVPGenerator
from helpers import DELIM


def exp_t(rate):
    if rate == 1:
        return "e^t"
    if rate == -1:
        return "e^(-t)"
    return f"e^({rate}t)"


def coeff_exp_t(coeff, rate):
    if coeff == 1:
        return exp_t(rate)
    if coeff == -1:
        return f"-{exp_t(rate)}"
    return f"{coeff}{exp_t(rate)}"


def left_text(a):
    return "y' + y" if a == 1 else f"y' + {a}y"


def signed_join(terms):
    pieces = []
    for coeff, body in terms:
        if coeff == 0:
            continue
        text = body if abs(coeff) == 1 else f"{abs(coeff)}{body}"
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def solution_text(C, a, m, c):
    return "y = " + signed_join([(C, exp_t(-a)), (m, exp_t(c))])


def denom_a(a):
    return f"(s + {a})"


def denom_c(c):
    return f"(s - {c})"


def frac_piece(coeff, denom):
    return f"1/{denom}" if abs(coeff) == 1 else f"{abs(coeff)}/{denom}"


def partial_frac_text(C, a, m, c):
    pieces = []
    for coeff, body in ((C, frac_piece(C, denom_a(a))),
                        (m, frac_piece(m, denom_c(c)))):
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return " ".join(pieces)


def subtract_value_text(left, value):
    return f"{left} - {value}" if value >= 0 else f"{left} + {abs(value)}"


def plus_y_term(coeff):
    return "+ Y" if coeff == 1 else f"+ {coeff}Y"


def signed_number(value):
    return f"+ {value}" if value > 0 else f"- {abs(value)}"


def combined_numerator(y0, c, b):
    factor = f"(s - {c})" if abs(y0) == 1 else f"{abs(y0)}(s - {c})"
    first = factor if y0 > 0 else f"-{factor}"
    return f"{first} {signed_number(b)}"


def parse_coeff(text):
    if text == "":
        return 1
    if text == "-":
        return -1
    return int(text)


def parse_rate(text):
    if text == "t":
        return 1
    inner = text[1:-1].removesuffix("t")
    if inner == "-":
        return -1
    return int(inner)


def parse_rhs(rhs):
    match = re.fullmatch(r"(-?\d*)e\^(t|\(-?\d*t\))", rhs)
    assert match is not None, rhs
    return parse_coeff(match.group(1)), parse_rate(match.group(2))


def parse_problem(problem):
    match = re.fullmatch(
        r"Use Laplace transforms to solve (y' \+ (?:(\d+)y|y)) = "
        r"(.+), y\(0\) = (-?\d+)\. Table: .+",
        problem,
    )
    assert match is not None, problem
    left, a_txt, rhs, y0 = match.groups()
    return {
        "a": int(a_txt or 1),
        "left": left,
        "rhs": rhs,
        "y0": int(y0),
    }


def oracle_parts(example):
    parts = parse_problem(example["problem"])
    b, c = parse_rhs(parts["rhs"])
    den_sum = parts["a"] + c
    m = Fraction(b, den_sum)
    assert m.denominator == 1
    m = m.numerator
    C = parts["y0"] - m
    return {
        **parts,
        "b": b,
        "c": c,
        "den_sum": den_sum,
        "m": m,
        "C": C,
        "cover_a_num": parts["y0"] * (-den_sum) + b,
        "cover_a_den": -den_sum,
        "answer": solution_text(C, parts["a"], m, c),
    }


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def solution_satisfies_ode(example):
    parts = oracle_parts(example)
    t = 0.37
    C, a, m, c = parts["C"], parts["a"], parts["m"], parts["c"]
    y = C * math.exp(-a * t) + m * math.exp(c * t)
    yp = -a * C * math.exp(-a * t) + c * m * math.exp(c * t)
    rhs = parts["b"] * math.exp(c * t)
    y0 = C + m
    return abs(yp + a * y - rhs) < 1e-9 and y0 == parts["y0"]


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    combined_num = combined_numerator(parts["y0"], parts["c"], parts["b"])
    Y_combined = (
        f"({combined_num})/({denom_a(parts['a'])}{denom_c(parts['c'])})"
    )
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "ODE_SETUP":
            expected = [
                f"{left_text(parts['a'])} = {parts['rhs']}, "
                f"y(0) = {parts['y0']}",
                "Laplace transform",
            ]
            if fields[1:] != expected:
                return False
        elif op == "LAPLACE" and fields[1].startswith("L[y'"):
            expected = [
                f"L[{left_text(parts['a'])}]",
                f"({subtract_value_text('sY', parts['y0'])}) "
                f"{plus_y_term(parts['a'])}",
            ]
            if fields[1:] != expected:
                return False
        elif op == "SOLVE_Y":
            expected = [
                f"{subtract_value_text(f'(s + {parts['a']})Y', parts['y0'])} "
                f"= {parts['b']}/{denom_c(parts['c'])}",
                f"Y = {Y_combined}",
            ]
            if fields[1:] != expected:
                return False
        elif op == "PARTIAL_FRAC":
            if fields[1:] != [
                "Y(s)",
                partial_frac_text(parts["C"], parts["a"], parts["m"],
                                  parts["c"]),
            ]:
                return False
        elif op == "A":
            if int(fields[1]) + int(fields[2]) != int(fields[3]):
                return False
        elif op == "M":
            if int(fields[1]) * int(fields[2]) != int(fields[3]):
                return False
        elif op == "D":
            if Fraction(int(fields[1]), int(fields[2])) != int(fields[3]):
                return False
        elif op == "INVERSE_LAPLACE" and fields[1].endswith(denom_a(parts["a"])):
            if fields[2] != coeff_exp_t(parts["C"], -parts["a"]):
                return False
        elif op == "INVERSE_LAPLACE" and fields[1].endswith(denom_c(parts["c"])):
            if fields[2] != coeff_exp_t(parts["m"], parts["c"]):
                return False
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    return True


class TestLaplaceIVPGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LaplaceIVPGenerator()

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

    def test_solution_satisfies_ode_and_initial_value(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(solution_satisfies_ode(result), result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_fixed_variant_constructor(self):
        gen = LaplaceIVPGenerator("first_order_exp")
        result = gen.generate()
        self.assertEqual(result["operation"], "laplace_ivp_first_order_exp")
        with self.assertRaises(ValueError):
            LaplaceIVPGenerator("bogus")

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<![A-Za-z0-9])1y|(?<![A-Za-z0-9])1e|1Y|\+ -|--")
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
