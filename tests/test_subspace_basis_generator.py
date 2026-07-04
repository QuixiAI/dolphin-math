import ast
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.subspace_basis_generator import SubspaceBasisGenerator
from helpers import DELIM


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def fmt_matrix(M):
    return "[" + ", ".join(
        "[" + ", ".join(fmt_frac(v) for v in row) + "]" for row in M
    ) + "]"


def parse_problem_matrix(problem):
    (matrix_txt,) = re.fullmatch(
        r"Find the RREF, rank, null space basis, and column space basis "
        r"for A = (\[\[.*\]\])\.",
        problem,
    ).groups()
    return ast.literal_eval(matrix_txt)


def rref(A):
    M = [[Fraction(v) for v in row] for row in A]
    rows, cols = len(M), len(M[0])
    pivot_cols = []
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows)
                      if M[r][col] != 0), None)
        if pivot is None:
            continue
        M[pivot_row], M[pivot] = M[pivot], M[pivot_row]
        scale = M[pivot_row][col]
        M[pivot_row] = [v / scale for v in M[pivot_row]]
        for r in range(rows):
            if r == pivot_row or M[r][col] == 0:
                continue
            factor = M[r][col]
            M[r] = [
                M[r][j] - factor * M[pivot_row][j]
                for j in range(cols)
            ]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == rows:
            break
    return M, pivot_cols


def null_basis(R, pivot_cols):
    n = len(R[0])
    free_cols = [j for j in range(n) if j not in pivot_cols]
    basis = []
    for free in free_cols:
        vec = [Fraction(0) for _ in range(n)]
        vec[free] = Fraction(1)
        for row, pivot in enumerate(pivot_cols):
            vec[pivot] = -R[row][free]
        basis.append(vec)
    return basis


def column_basis(A, pivot_cols):
    return [[A[i][col] for i in range(len(A))] for col in pivot_cols]


def oracle_answer(example):
    A = parse_problem_matrix(example["problem"])
    R, pivot_cols = rref(A)
    return (f"rank {len(pivot_cols)}; "
            f"null basis {fmt_matrix(null_basis(R, pivot_cols))}; "
            f"column basis {fmt_matrix(column_basis(A, pivot_cols))}")


def parse_row_op(text):
    match = re.fullmatch(
        r"R(\d+) -> R\1 ([+-]) (?:(\d+)·)?R(\d+)",
        text,
    )
    target, sign, coeff, source = match.groups()
    delta = int(coeff or 1)
    if sign == "-":
        delta = -delta
    return int(target) - 1, int(source) - 1, delta


def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v)))
            for i in range(len(A))]


def check_step_arithmetic(example):
    A = parse_problem_matrix(example["problem"])
    work = [row[:] for row in A]
    R, pivot_cols = rref(A)
    saw_rref = False
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "ROW_OP":
            target, source, delta = parse_row_op(parts[1])
            new_row = [
                work[target][j] + delta * work[source][j]
                for j in range(len(work[target]))
            ]
            if new_row != ast.literal_eval(parts[2]):
                return False
            work[target] = new_row
        elif parts[0] == "RREF_RESULT":
            if fmt_matrix(R) != parts[2]:
                return False
            if fmt_matrix(work) != parts[2]:
                return False
            saw_rref = True
        elif parts[0] == "PIVOT_COLS":
            cols = ", ".join(str(col + 1) for col in pivot_cols)
            if parts[1] != f"columns {cols}":
                return False
            if parts[2] != f"rank = {len(pivot_cols)}":
                return False
        elif parts[0] == "NULL_VECTOR":
            vec = [Fraction(v) for v in ast.literal_eval(parts[2])]
            if matvec([[Fraction(v) for v in row] for row in A], vec) != [
                    0, 0, 0]:
                return False
        elif parts[0] == "COL_BASIS":
            if ast.literal_eval(parts[2]) != column_basis(A, pivot_cols):
                return False
    return saw_rref


class TestSubspaceBasisGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SubspaceBasisGenerator()

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

    def test_variants_have_expected_rank(self):
        for variant, rank in (("rank2", 2), ("rank3", 3)):
            gen = SubspaceBasisGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertIn(f"rank {rank};", result["final_answer"])

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1\*|\+ 0|--|\+ -")
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
        self.assertEqual(ops, {"subspace_basis_rank2",
                               "subspace_basis_rank3"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            SubspaceBasisGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
