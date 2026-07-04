import ast
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.positive_definite_generator import PositiveDefiniteGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Use Sylvester's criterion to decide whether A=(\[\[.*?\]\]) "
    r"is positive definite\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def parse_matrix(problem):
    match = PROBLEM_RE.fullmatch(problem)
    if not match:
        raise AssertionError(problem)
    return ast.literal_eval(match.group(1))


def expected_flow(example):
    matrix = parse_matrix(example["problem"])
    a, b = matrix[0]
    _, c = matrix[1]
    ac = a * c
    b2 = b * b
    det = ac - b2
    positive = a > 0 and det > 0
    steps = [
        make_step("PD_SETUP", f"A={matrix_text(matrix)}",
                  "Sylvester criterion"),
        make_step("LEADING_MINOR", "Delta1", a),
        make_step("CHECK", "Delta1 > 0", f"{a} > 0",
                  "true" if a > 0 else "false"),
        make_step("M", a, c, ac),
        make_step("M", b, b, b2),
        make_step("S", ac, b2, det),
        make_step("LEADING_MINOR", "Delta2", det),
        make_step("CHECK", "Delta2 > 0", f"{det} > 0",
                  "true" if det > 0 else "false"),
        make_step("CHECK", "all leading minors positive",
                  "true" if positive else "false"),
    ]
    answer = "positive_definite" if positive else "not_positive_definite"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestPositiveDefiniteGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = PositiveDefiniteGenerator()

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
        for variant in PositiveDefiniteGenerator.VARIANTS:
            result = PositiveDefiniteGenerator(variant).generate()
            self.assertEqual(result["operation"], f"positive_definite_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)
            if variant == "positive":
                self.assertEqual(answer, "positive_definite")
            else:
                self.assertEqual(answer, "not_positive_definite")

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PositiveDefiniteGenerator("bogus")

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
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
