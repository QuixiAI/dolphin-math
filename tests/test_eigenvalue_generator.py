import ast
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

from generators.eigenvalue_generator import EigenvalueGenerator
from helpers import DELIM


def parse_problem_matrix(problem):
    (matrix_txt,) = re.fullmatch(
        r"Find the characteristic polynomial, eigenvalues, and "
        r"eigenvectors of A = (\[\[.*\]\])\.",
        problem,
    ).groups()
    return ast.literal_eval(matrix_txt)


def trim(poly):
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_add(p, q):
    out = [0] * max(len(p), len(q))
    for i, value in enumerate(p):
        out[i] += value
    for i, value in enumerate(q):
        out[i] += value
    return trim(out)


def poly_mul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return trim(out)


def poly_neg(p):
    return [-value for value in p]


def det_poly(M):
    n = len(M)
    if n == 1:
        return M[0][0][:]
    total = [0]
    for j in range(n):
        minor = [
            [M[r][c] for c in range(n) if c != j]
            for r in range(1, n)
        ]
        term = poly_mul(M[0][j], det_poly(minor))
        if j % 2:
            term = poly_neg(term)
        total = poly_add(total, term)
    return trim(total)


def char_poly(A):
    n = len(A)
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append([-A[i][j], 1])
            else:
                row.append([-A[i][j]])
        matrix.append(row)
    return det_poly(matrix)


def eval_poly(poly, x):
    return sum(coeff * (x ** power) for power, coeff in enumerate(poly))


def integer_roots(poly):
    return [candidate for candidate in range(-20, 21)
            if eval_poly(poly, candidate) == 0]


def poly_text(poly):
    coeffs = list(reversed(poly))
    degree = len(coeffs) - 1
    pieces = []
    for i, coeff in enumerate(coeffs):
        power = degree - i
        if coeff == 0:
            continue
        abs_coeff = abs(coeff)
        if power == 0:
            body = str(abs_coeff)
        elif power == 1:
            body = "λ" if abs_coeff == 1 else f"{abs_coeff}λ"
        else:
            body = f"λ^{power}" if abs_coeff == 1 else (
                f"{abs_coeff}λ^{power}"
            )
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return " ".join(pieces)


def factor_text(root):
    if root == 0:
        return "λ"
    if root > 0:
        return f"(λ - {root})"
    return f"(λ + {-root})"


def factored_text(roots):
    return "*".join(factor_text(root) for root in roots)


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


def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


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
        [A[i][j] - (lam if i == j else 0) for j in range(len(A))]
        for i in range(len(A))
    ]


def null_vector(M):
    R, pivot_cols = rref(M)
    n = len(M[0])
    free_cols = [j for j in range(n) if j not in pivot_cols]
    vec = [Fraction(0) for _ in range(n)]
    vec[free_cols[0]] = Fraction(1)
    for row, pivot in enumerate(pivot_cols):
        vec[pivot] = -R[row][free_cols[0]]
    return primitive_int_vector(vec)


def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v)))
            for i in range(len(A))]


def oracle_answer(example):
    A = parse_problem_matrix(example["problem"])
    poly = char_poly(A)
    roots = integer_roots(poly)
    pairs = []
    for root in roots:
        vec = null_vector(subtract_lambda(A, root))
        pairs.append(f"λ={root}: span({vec})")
    return (f"p(λ)={poly_text(poly)} = {factored_text(roots)}; "
            f"eigenpairs {', '.join(pairs)}")


def shifted_matrix_label(lam):
    if lam < 0:
        return f"A + {-lam}I"
    if lam == 0:
        return "A"
    return f"A - {lam}I"


def check_step_arithmetic(example):
    A = parse_problem_matrix(example["problem"])
    poly = char_poly(A)
    roots = integer_roots(poly)
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "CHAR_POLY":
            if parts[1] != f"p(λ) = {poly_text(poly)}":
                return False
            if parts[2] != factored_text(roots):
                return False
        elif parts[0] == "EIGENVALUE":
            lam = int(re.fullmatch(r"λ = (-?\d+)", parts[1]).group(1))
            if eval_poly(poly, lam) != 0:
                return False
            if parts[2] != f"p({lam}) = 0":
                return False
        elif parts[0] == "EIGEN_MATRIX":
            label = parts[1]
            lam = next(root for root in roots
                       if shifted_matrix_label(root) == label)
            if ast.literal_eval(parts[2]) != subtract_lambda(A, lam):
                return False
        elif parts[0] == "EIGENVECTOR":
            label = parts[1].removesuffix(" times v = 0")
            lam = next(root for root in roots
                       if shifted_matrix_label(root) == label)
            vec = ast.literal_eval(parts[2])
            if matvec(subtract_lambda(A, lam), vec) != [0] * len(A):
                return False
        elif parts[0] == "CHECK":
            vec = ast.literal_eval(parts[1][2:])
            Av = ast.literal_eval(parts[2])
            lam_txt, lv_txt = parts[3].split("*v = ")
            lam = int(lam_txt)
            if Av != matvec(A, vec):
                return False
            if ast.literal_eval(lv_txt) != [lam * value for value in vec]:
                return False
    return True


class TestEigenvalueGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = EigenvalueGenerator()

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

    def test_variants_have_expected_dimension(self):
        for variant, dim in (("two", 2), ("three", 3)):
            gen = EigenvalueGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                A = parse_problem_matrix(result["problem"])
                self.assertEqual(len(A), dim)
                self.assertEqual(len(A[0]), dim)

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"--|\+ -|- -|\^1\b|(?<!\d)1λ")
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

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"eigenvalues_two", "eigenvalues_three"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            EigenvalueGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
