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

from generators.matrix_exponential_generator import MatrixExponentialGenerator
from helpers import DELIM


def fmt_matrix(M):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]"
                           for row in M) + "]"


def parse_problem_matrix(problem):
    (matrix_txt,) = re.fullmatch(
        r"Find e\^\(At\) for A = (\[\[.*\]\]) by diagonalization\.",
        problem,
    ).groups()
    return ast.literal_eval(matrix_txt)


def matmul(A, B):
    return [
        [sum(A[i][k] * B[k][j] for k in range(len(B)))
         for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v)))
            for i in range(len(A))]


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


def exp_text(lam):
    if lam == 1:
        return "e^t"
    if lam == -1:
        return "e^(-t)"
    return f"e^({lam}t)"


def combo_text(terms):
    pieces = []
    for coeff, lam in terms:
        if coeff == 0:
            continue
        body = exp_text(lam) if abs(coeff) == 1 else (
            f"{abs(coeff)}*{exp_text(lam)}"
        )
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return " ".join(pieces) if pieces else "0"


def symbolic_matrix(entries):
    return "[" + ", ".join(
        "[" + ", ".join(row) + "]" for row in entries
    ) + "]"


def exp_parts(A):
    lambdas = eigenvalues(A)
    vectors = [null_vector(subtract_lambda(A, lam)) for lam in lambdas]
    P = columns_to_matrix(vectors)
    P_inv = inverse_2x2(P)
    D = [[lambdas[0], 0], [0, lambdas[1]]]
    entries = []
    records = []
    for i in range(2):
        row = []
        record_row = []
        for j in range(2):
            terms = [
                (P[i][0] * P_inv[0][j], lambdas[0]),
                (P[i][1] * P_inv[1][j], lambdas[1]),
            ]
            row.append(combo_text(terms))
            record_row.append(terms)
        entries.append(row)
        records.append(record_row)
    return lambdas, vectors, P, P_inv, D, entries, records


def oracle_answer(example):
    A = parse_problem_matrix(example["problem"])
    *_, entries, _ = exp_parts(A)
    return f"e^(At)={symbolic_matrix(entries)}"


def parse_scalar_vector(text):
    if text.startswith("v = "):
        return 1, ast.literal_eval(text.removeprefix("v = "))
    if text.startswith("-v = "):
        return -1, ast.literal_eval(text.removeprefix("-v = "))
    lam_txt, lv_txt = text.split("*v = ")
    return int(lam_txt), ast.literal_eval(lv_txt)


def value_at_zero(records):
    return [[sum(coeff for coeff, _ in row[j])
             for j in range(2)] for row in records]


def derivative_at_zero(records):
    return [[sum(coeff * lam for coeff, lam in row[j])
             for j in range(2)] for row in records]


def check_step_arithmetic(example):
    A = parse_problem_matrix(example["problem"])
    lambdas, vectors, P, P_inv, D, entries, records = exp_parts(A)
    expD = [[exp_text(lambdas[0]), "0"], ["0", exp_text(lambdas[1])]]
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "EIGENVECTOR":
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
        elif parts[0] == "EXP_DIAG":
            if parts[2] != symbolic_matrix(expD):
                return False
        elif parts[0] == "EXP_ENTRY":
            i, j = ast.literal_eval(parts[1])
            expected = entries[i - 1][j - 1]
            if parts[2] != expected or parts[3] != expected:
                return False
        elif parts[0] == "CHECK" and parts[1] == "t = 0":
            if ast.literal_eval(parts[2]) != value_at_zero(records):
                return False
    return derivative_at_zero(records) == A


class TestMatrixExponentialGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = MatrixExponentialGenerator()

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

    def test_step_arithmetic_and_symbolic_checks(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_exp_at_zero_and_derivative(self):
        for _ in range(300):
            result = self.gen.generate()
            A = parse_problem_matrix(result["problem"])
            *_, records = exp_parts(A)
            self.assertEqual(value_at_zero(records), [[1, 0], [0, 1]])
            self.assertEqual(derivative_at_zero(records), A)

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
                self.assertNotIn(f"{DELIM}{DELIM}", raw_step)


if __name__ == "__main__":
    unittest.main()
