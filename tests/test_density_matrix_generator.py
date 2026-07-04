import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.density_matrix_generator import DensityMatrixGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"An ensemble has probability ([^ ]+) of ket0 and the remaining "
    r"probability of ket1\. For observable A=diag\((-?\d+),(-?\d+)\), "
    r"build rho, compute Tr\(rho A\), and compute Tr\(rho\^2\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return {"p": Fraction(match.group(1)), "a": int(match.group(2)),
            "b": int(match.group(3))}


def expected_flow(example):
    parts = parse_problem(example["problem"])
    p = parts["p"]
    q = 1 - p
    left = p * parts["a"]
    right = q * parts["b"]
    expectation = left + right
    p_sq = p ** 2
    q_sq = q ** 2
    purity = p_sq + q_sq
    rho = f"[[{fraction_text(p)},0],[0,{fraction_text(q)}]]"
    observable = f"diag({parts['a']},{parts['b']})"
    answer = (
        f"rho = {rho}; expectation = {fraction_text(expectation)}; "
        f"purity = {fraction_text(purity)}"
    )
    steps = [
        make_step("DENSITY_SETUP", f"p0={fraction_text(p)}", "p1=1-p0",
                  f"A={observable}"),
        make_step("S", 1, fraction_text(p), fraction_text(q)),
        make_step("DENSITY_MATRIX", f"rho={rho}"),
        make_step("TRACE_EXPECT", "Tr(rho A)=p0*a+p1*b"),
        make_step("M", fraction_text(p), parts["a"], fraction_text(left)),
        make_step("M", fraction_text(q), parts["b"], fraction_text(right)),
        make_step("A", fraction_text(left), fraction_text(right),
                  fraction_text(expectation)),
        make_step("E", fraction_text(p), 2, fraction_text(p_sq)),
        make_step("E", fraction_text(q), 2, fraction_text(q_sq)),
        make_step("A", fraction_text(p_sq), fraction_text(q_sq),
                  fraction_text(purity)),
        make_step("PURITY", f"Tr(rho^2)={fraction_text(purity)}"),
        make_step("Z", answer),
    ]
    return steps, answer


class TestDensityMatrixGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DensityMatrixGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "density_matrix_diagonal")
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
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
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
