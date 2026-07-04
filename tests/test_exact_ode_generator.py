import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.exact_ode_generator import ExactODEGenerator
from helpers import DELIM


def fmt_linear(raw_terms):
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        if body:
            text = body if abs(coeff) == 1 else f"{abs(coeff)}*{body}"
        else:
            text = str(abs(coeff))
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def fmt_quadratic(a, b, c, d, e):
    return fmt_linear([
        (a, "x^2"),
        (b, "y^2"),
        (c, "x*y"),
        (d, "x"),
        (e, "y"),
    ])


def fmt_eval_y_terms(b, e, y):
    return fmt_linear([(b, f"({y})^2"), (e, f"({y})")])


def split_terms(expr):
    if expr == "0":
        return []
    return [raw for raw in expr.replace(" - ", " + -").split(" + ")
            if raw]


def parse_linear(expr):
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


def parse_problem(problem):
    solve = re.fullmatch(
        r"Solve \((.+)\) dx \+ \((.+)\) dy = 0 with y\(0\) = (-?\d+)\.",
        problem,
    )
    if solve:
        M, N, y0 = solve.groups()
        return "solve_exact", M, N, int(y0)
    test = re.fullmatch(
        r"Test whether \((.+)\) dx \+ \((.+)\) dy = 0 is exact\.",
        problem,
    )
    assert test is not None, problem
    M, N = test.groups()
    return "test", M, N, None


def potential_value(a, b, c, d, e, x, y):
    return a * x * x + b * y * y + c * x * y + d * x + e * y


def oracle_parts(example):
    kind, M, N, y0 = parse_problem(example["problem"])
    px, py, d = parse_linear(M)
    nx, qy, e = parse_linear(N)
    exact = py == nx
    if kind == "test":
        if exact:
            answer = f"exact because M_y = N_x = {py}"
            variant = "exact_test"
        else:
            answer = f"not exact because M_y = {py} and N_x = {nx}"
            variant = "not_exact_test"
        return {
            "variant": variant,
            "M": M,
            "N": N,
            "M_y": py,
            "N_x": nx,
            "answer": answer,
        }

    assert exact
    a = Fraction(px, 2)
    b = Fraction(qy, 2)
    assert a.denominator == 1
    assert b.denominator == 1
    a = a.numerator
    b = b.numerator
    c = py
    constant = potential_value(a, b, c, d, e, 0, y0)
    phi = fmt_quadratic(a, b, c, d, e)
    return {
        "variant": "solve_exact",
        "M": M,
        "N": N,
        "M_y": py,
        "N_x": nx,
        "a": a,
        "b": b,
        "c": c,
        "d": d,
        "e": e,
        "y0": y0,
        "phi": phi,
        "constant": constant,
        "answer": f"{phi} = {constant}",
    }


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "ODE_SETUP":
            equation = f"({parts['M']}) dx + ({parts['N']}) dy = 0"
            if parts["variant"] == "solve_exact":
                expected = [equation, f"y(0) = {parts['y0']}; solve"]
            else:
                expected = [equation, "test exactness"]
            if fields[1:] != expected:
                return False
        elif op == "PARTIAL_RESULT" and fields[1] == "M_y":
            if int(fields[2]) != parts["M_y"]:
                return False
        elif op == "PARTIAL_RESULT" and fields[1] == "N_x":
            if int(fields[2]) != parts["N_x"]:
                return False
        elif op == "CHECK":
            if parts["variant"] == "not_exact_test":
                expected = [
                    "M_y != N_x",
                    f"{parts['M_y']} != {parts['N_x']}",
                    "not exact",
                ]
            else:
                expected = [
                    "M_y = N_x",
                    f"{parts['M_y']} = {parts['N_x']}",
                    "exact",
                ]
            if fields[1:] != expected:
                return False
        elif op == "D":
            if Fraction(int(fields[1]), int(fields[2])) != int(fields[3]):
                return False
        elif op == "POTENTIAL_BUILD":
            if parts["variant"] != "solve_exact":
                return False
            if fields[1] == "integrate M dx":
                expected = fmt_linear([
                    (parts["a"], "x^2"),
                    (parts["c"], "x*y"),
                    (parts["d"], "x"),
                    (1, "g(y)"),
                ])
                if fields[2:] != [expected, "g(y) remains"]:
                    return False
            elif fields[1] == "solve g'(y)":
                g_prime = fmt_linear([(2 * parts["b"], "y"),
                                      (parts["e"], "")])
                g_y = fmt_linear([(parts["b"], "y^2"),
                                  (parts["e"], "y")])
                if fields[2:] != [f"g'(y) = {g_prime}", f"g(y) = {g_y}"]:
                    return False
        elif op == "PARTIAL_RESULT" and fields[1] == "F_y":
            expected = fmt_linear([(parts["c"], "x"), (1, "g'(y)")])
            if fields[2] != expected:
                return False
        elif op == "EXACT_MATCH":
            partial_F_y = fmt_linear([(parts["c"], "x"), (1, "g'(y)")])
            if fields[1:] != ["F_y = N", f"{partial_F_y} = {parts['N']}"]:
                return False
        elif op == "POTENTIAL_RESULT":
            if fields[1:] != ["F(x,y)", parts["phi"]]:
                return False
        elif op == "EVAL":
            expected_expr = fmt_eval_y_terms(parts["b"], parts["e"],
                                             parts["y0"])
            expected = [f"F(0,{parts['y0']})", expected_expr,
                        str(parts["constant"])]
            if fields[1:] != expected:
                return False
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    return True


class TestExactODEGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ExactODEGenerator()

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

    def test_solve_variant_potential_derivatives_match_M_and_N(self):
        gen = ExactODEGenerator("solve_exact")
        for _ in range(200):
            result = gen.generate()
            parts = oracle_parts(result)
            px, py, d = parse_linear(parts["M"])
            nx, qy, e = parse_linear(parts["N"])
            self.assertEqual(2 * parts["a"], px)
            self.assertEqual(parts["c"], py)
            self.assertEqual(parts["d"], d)
            self.assertEqual(parts["c"], nx)
            self.assertEqual(2 * parts["b"], qy)
            self.assertEqual(parts["e"], e)

    def test_variants_are_available(self):
        for variant in ("exact_test", "not_exact_test", "solve_exact"):
            gen = ExactODEGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"], f"exact_ode_{variant}")
                self.assertEqual(oracle_parts(result)["variant"], variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ExactODEGenerator("bogus")

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1\*|\+ -|--")
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
