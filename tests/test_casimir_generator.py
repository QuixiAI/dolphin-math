import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.casimir_generator import CasimirGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Verify the spin-1 Casimir for hbar=([^ ]+) using Jplus=.*"
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ", ".join(fraction_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def diag(values):
    return [
        [values[i] if i == j else Fraction(0) for j in range(len(values))]
        for i in range(len(values))
    ]


def mat_add(A, B):
    return [
        [A[i][j] + B[i][j] for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def mat_scale(A, scalar):
    return [[scalar * value for value in row] for row in A]


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return Fraction(match.group(1))


def expected_flow(example):
    hbar = parse_problem(example["problem"])
    hbar_sq = hbar ** 2
    two_hbar_sq = 2 * hbar_sq
    j_plus_j_minus = diag([2 * hbar_sq, 2 * hbar_sq, 0])
    j_minus_j_plus = diag([0, 2 * hbar_sq, 2 * hbar_sq])
    ladder_sum = mat_add(j_plus_j_minus, j_minus_j_plus)
    ladder_half = mat_scale(ladder_sum, Fraction(1, 2))
    jz_sq = diag([hbar_sq, 0, hbar_sq])
    casimir = mat_add(jz_sq, ladder_half)
    identity_target = diag([two_hbar_sq, two_hbar_sq, two_hbar_sq])
    steps = [
        make_step("CASIMIR_SETUP", "spin=1", f"hbar={fraction_text(hbar)}",
                  "J^2=Jz^2+(J+J-+J-J+)/2"),
        make_step("E", fraction_text(hbar), 2, fraction_text(hbar_sq)),
        make_step("MATRIX_PRODUCT", "Jz^2", matrix_text(jz_sq)),
        make_step("MATRIX_PRODUCT", "J+J-", matrix_text(j_plus_j_minus)),
        make_step("MATRIX_PRODUCT", "J-J+", matrix_text(j_minus_j_plus)),
        make_step("MATRIX_ADD", "J+J- + J-J+", matrix_text(ladder_sum)),
        make_step("MATRIX_SCALE", "1/2 ladder sum",
                  matrix_text(ladder_half)),
        make_step("MATRIX_ADD", "Jz^2 + ladder half",
                  matrix_text(casimir)),
        make_step("A", 1, 1, 2),
        make_step("M", 2, fraction_text(hbar_sq),
                  fraction_text(two_hbar_sq)),
        make_step("CHECK", "J^2", f"{fraction_text(two_hbar_sq)}I",
                  "verified"),
    ]
    answer = (
        f"J^2 = {fraction_text(two_hbar_sq)}I = "
        f"{matrix_text(identity_target)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestCasimirGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CasimirGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_scalar_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
