import ast
import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.diagonalization_generator import DiagonalizationGenerator
from helpers import DELIM


def fmt_matrix(M):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]"
                           for row in M) + "]"


def parse_problem(problem):
    matrix_txt, k_txt = re.fullmatch(
        r"Diagonalize A = (\[\[.*\]\]) and compute A\^(\d+)\.",
        problem,
    ).groups()
    return ast.literal_eval(matrix_txt), int(k_txt)


def matmul(A, B):
    return [
        [sum(A[i][k] * B[k][j] for k in range(len(B)))
         for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v)))
            for i in range(len(A))]


def matrix_power(A, k):
    result = [[1, 0], [0, 1]]
    for _ in range(k):
        result = matmul(result, A)
    return result


def inverse_2x2(A):
    a, b = A[0]
    c, d = A[1]
    det = a * d - b * c
    return [[d // det, -b // det], [-c // det, a // det]]


def eigenvalues(A):
    trace = A[0][0] + A[1][1]
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    disc = trace * trace - 4 * det
    root = math.isqrt(disc)
    assert root * root == disc
    return sorted([(trace - root) // 2, (trace + root) // 2])


def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


def rref(M):
    work = [[Fraction(v) for v in row] for row in M]
    rows, cols = len(work), len(work[0])
    pivot_cols = []
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows)
                      if work[r][col] != 0), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [v / scale for v in work[pivot_row]]
        for r in range(rows):
            if r == pivot_row or work[r][col] == 0:
                continue
            factor = work[r][col]
            work[r] = [
                work[r][j] - factor * work[pivot_row][j]
                for j in range(cols)
            ]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == rows:
            break
    return work, pivot_cols


def primitive_int_vector(vec):
    scale = 1
    for value in vec:
        scale = lcm(scale, value.denominator)
    ints = [value.numerator * (scale // value.denominator) for value in vec]
    common = 0
    for value in ints:
        common = gcd(common, abs(value))
    ints = [value // common for value in ints]
    first = next(value for value in ints if value != 0)
    if first < 0:
        ints = [-value for value in ints]
    return ints


def subtract_lambda(A, lam):
    return [
        [A[i][j] - (lam if i == j else 0) for j in range(2)]
        for i in range(2)
    ]


def null_vector(M):
    R, pivot_cols = rref(M)
    free_cols = [j for j in range(2) if j not in pivot_cols]
    vec = [Fraction(0), Fraction(0)]
    vec[free_cols[0]] = Fraction(1)
    for row, pivot in enumerate(pivot_cols):
        vec[pivot] = -R[row][free_cols[0]]
    return primitive_int_vector(vec)


def columns_to_matrix(cols):
    return [[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]]


def poly_text(lambdas):
    trace = sum(lambdas)
    det = lambdas[0] * lambdas[1]
    coeffs = [1, -trace, det]
    pieces = ["λ^2"]
    if coeffs[1] > 0:
        body = "λ" if coeffs[1] == 1 else f"{coeffs[1]}λ"
        pieces.append(f"+ {body}")
    elif coeffs[1] < 0:
        body = "λ" if coeffs[1] == -1 else f"{abs(coeffs[1])}λ"
        pieces.append(f"- {body}")
    if coeffs[2] > 0:
        pieces.append(f"+ {coeffs[2]}")
    elif coeffs[2] < 0:
        pieces.append(f"- {abs(coeffs[2])}")
    return " ".join(pieces)


def factor_text(root):
    if root > 0:
        return f"(λ - {root})"
    return f"(λ + {-root})"


def oracle_parts(A, k):
    lambdas = eigenvalues(A)
    vectors = [null_vector(subtract_lambda(A, lam)) for lam in lambdas]
    P = columns_to_matrix(vectors)
    P_inv = inverse_2x2(P)
    D = [[lambdas[0], 0], [0, lambdas[1]]]
    Dk = [[lambdas[0] ** k, 0], [0, lambdas[1] ** k]]
    Ak = matmul(matmul(P, Dk), P_inv)
    return lambdas, P, P_inv, D, Dk, Ak


def oracle_answer(example):
    A, k = parse_problem(example["problem"])
    _, P, P_inv, D, _, Ak = oracle_parts(A, k)
    return (f"P={fmt_matrix(P)}, D={fmt_matrix(D)}, "
            f"P^-1={fmt_matrix(P_inv)}, A^{k}={fmt_matrix(Ak)}")


def eval_integer_expr(expr):
    expr = re.sub(r"-?\d+", lambda m: f"Fraction({m.group(0)})", expr)
    return eval(expr, {"__builtins__": {}, "Fraction": Fraction}, {})


def parse_scalar_vector(text):
    if text.startswith("v = "):
        return 1, ast.literal_eval(text.removeprefix("v = "))
    if text.startswith("-v = "):
        return -1, ast.literal_eval(text.removeprefix("-v = "))
    lam_txt, lv_txt = text.split("*v = ")
    return int(lam_txt), ast.literal_eval(lv_txt)


def check_step_arithmetic(example):
    A, k = parse_problem(example["problem"])
    lambdas, P, P_inv, D, Dk, Ak = oracle_parts(A, k)
    factored = "*".join(factor_text(lam) for lam in lambdas)
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "CHAR_POLY":
            if parts[1] != f"p(λ) = {poly_text(lambdas)}":
                return False
            if parts[2] != factored:
                return False
        elif parts[0] == "E":
            if int(parts[1]) ** int(parts[2]) != int(parts[3]):
                return False
        elif parts[0] == "EIGENVECTOR":
            lam = int(parts[1].split(" = ")[1])
            vec = ast.literal_eval(parts[2])
            if matvec(subtract_lambda(A, lam), vec) != [0, 0]:
                return False
        elif parts[0] == "CHECK" and parts[1].startswith("A*"):
            vec = ast.literal_eval(parts[1][2:])
            Av = ast.literal_eval(parts[2])
            lam, lv = parse_scalar_vector(parts[3])
            if Av != matvec(A, vec):
                return False
            if lv != [lam * value for value in vec]:
                return False
        elif parts[0] == "DIAG_FORM":
            if parts[1] != f"P = {fmt_matrix(P)}":
                return False
            if parts[2] != f"D = {fmt_matrix(D)}":
                return False
            if parts[3] != f"P^-1 = {fmt_matrix(P_inv)}":
                return False
        elif parts[0] == "D_POWER":
            if parts[1] != f"D^{k}" or parts[2] != fmt_matrix(Dk):
                return False
        elif parts[0] == "POWER_ENTRY":
            if eval_integer_expr(parts[2]) != Fraction(parts[3]):
                return False
            i, j = ast.literal_eval(parts[1])
            if Ak[i - 1][j - 1] != int(parts[3]):
                return False
        elif parts[0] == "CHECK" and parts[1] == f"direct A^{k}":
            if ast.literal_eval(parts[2]) != matrix_power(A, k):
                return False
    return True


class TestDiagonalizationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DiagonalizationGenerator()

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

    def test_power_entries_cover_matrix(self):
        for _ in range(100):
            result = self.gen.generate()
            entries = [s for s in result["steps"]
                       if s.startswith(f"POWER_ENTRY{DELIM}")]
            self.assertEqual(len(entries), 4)

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"--|\+ -|- -|\^1\b|(?<!\d)1λ|(?<!\d)1\*")
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
                self.assertNotIn(f"{DELIM}{DELIM}", raw_step)


if __name__ == "__main__":
    unittest.main()
