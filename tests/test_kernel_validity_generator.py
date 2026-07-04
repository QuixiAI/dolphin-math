import ast
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.kernel_validity_generator import KernelValidityGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Check whether the candidate kernel Gram matrix K=(\[\[.*?\]\]) is PSD "
    r"using Sylvester's criterion for 2x2 matrices\."
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


def bool_text(value):
    return "true" if value else "false"


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    matrix = ast.literal_eval(match.group(1))
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][1]
    ac = a * c
    b2 = b * b
    det = ac - b2
    checks = [a >= 0, c >= 0, det >= 0]
    is_psd = all(checks)
    steps = [
        make_step("PSD_SETUP", f"K={matrix_text(matrix)}",
                  "criterion=all principal minors >= 0"),
        make_step("PRINCIPAL_MINOR", "K11", a),
        make_step("CHECK", "K11 >= 0", f"{a} >= 0",
                  bool_text(checks[0])),
        make_step("PRINCIPAL_MINOR", "K22", c),
        make_step("CHECK", "K22 >= 0", f"{c} >= 0",
                  bool_text(checks[1])),
        make_step("M", a, c, ac),
        make_step("M", b, b, b2),
        make_step("S", ac, b2, det),
        make_step("DET", "K", det),
        make_step("PRINCIPAL_MINOR", "det(K)", det),
        make_step("CHECK", "det(K) >= 0", f"{det} >= 0",
                  bool_text(checks[2])),
        make_step("KERNEL_VALIDITY", f"psd={bool_text(is_psd)}"),
    ]
    answer = f"PSD={bool_text(is_psd)}; minors=({a},{c},{det})"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestKernelValidityGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = KernelValidityGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "kernel_validity_psd_2x2")
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

    def test_emits_psd_and_non_psd_cases(self):
        seen = set()
        for _ in range(300):
            result = self.gen.generate()
            seen.add(result["final_answer"].split(";", 1)[0])
        self.assertIn("PSD=true", seen)
        self.assertIn("PSD=false", seen)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
