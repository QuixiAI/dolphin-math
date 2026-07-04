import ast
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.matrix_calculus_generator import MatrixCalculusGenerator
from helpers import DELIM


LINEAR_RE = re.compile(
    r"For a=(\([^)]+\)) and x=(\([^)]+\)), compute grad_x\(a\^T x\) "
    r"and the value a\^T x\."
)
QUAD_RE = re.compile(
    r"For A=(\[\[.*?\]\]) and x=(\([^)]+\)), compute "
    r"grad_x\(x\^T A x\) using \(A\+A\^T\)x\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def vector_text(values):
    return "(" + ",".join(str(value) for value in values) + ")"


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def expected_linear(problem):
    match = LINEAR_RE.fullmatch(problem)
    a = list(ast.literal_eval(match.group(1)))
    x = list(ast.literal_eval(match.group(2)))
    term0 = a[0] * x[0]
    term1 = a[1] * x[1]
    value = term0 + term1
    steps = [
        make_step("MC_SETUP", "expression=a^T x", f"a={vector_text(a)}",
                  f"x={vector_text(x)}"),
        make_step("GRADIENT_FORMULA", "grad_x(a^T x)=a"),
        make_step("M", a[0], x[0], term0),
        make_step("M", a[1], x[1], term1),
        make_step("A", term0, term1, value),
        make_step("GRAD_ENTRY", "g1", a[0]),
        make_step("GRAD_ENTRY", "g2", a[1]),
    ]
    answer = f"grad={vector_text(a)}; value={value}"
    return steps, answer


def expected_quadratic(problem):
    match = QUAD_RE.fullmatch(problem)
    matrix = ast.literal_eval(match.group(1))
    x = list(ast.literal_eval(match.group(2)))
    symmetric = [
        [matrix[row][col] + matrix[col][row] for col in range(2)]
        for row in range(2)
    ]
    gradient = [
        symmetric[row][0] * x[0] + symmetric[row][1] * x[1]
        for row in range(2)
    ]
    steps = [
        make_step("MC_SETUP", "expression=x^T A x",
                  f"A={matrix_text(matrix)}", f"x={vector_text(x)}"),
        make_step("GRADIENT_FORMULA", "grad_x(x^T A x)=(A+A^T)x"),
        make_step("MATRIX_SUM", "B=A+A^T"),
    ]
    for row in range(2):
        for col in range(2):
            steps.append(make_step("A", matrix[row][col], matrix[col][row],
                                   symmetric[row][col]))
            steps.append(make_step("MAT_ENTRY", f"B{row + 1}{col + 1}",
                                   symmetric[row][col]))
    for row in range(2):
        term0 = symmetric[row][0] * x[0]
        term1 = symmetric[row][1] * x[1]
        value = term0 + term1
        steps.extend([
            make_step("M", symmetric[row][0], x[0], term0),
            make_step("M", symmetric[row][1], x[1], term1),
            make_step("A", term0, term1, value),
            make_step("GRAD_ENTRY", f"g{row + 1}", value),
        ])
    answer = f"grad={vector_text(gradient)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if LINEAR_RE.fullmatch(problem):
        steps, answer = expected_linear(problem)
    elif QUAD_RE.fullmatch(problem):
        steps, answer = expected_quadratic(problem)
    else:
        raise AssertionError(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestMatrixCalculusGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MatrixCalculusGenerator()

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

    def test_variants_are_available(self):
        for variant in MatrixCalculusGenerator.VARIANTS:
            result = MatrixCalculusGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"matrix_calculus_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MatrixCalculusGenerator("bogus")

    def test_arithmetic_steps(self):
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

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
