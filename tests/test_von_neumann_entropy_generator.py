import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.von_neumann_entropy_generator import VonNeumannEntropyGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Compute the von Neumann entropy in bits for a density matrix "
    r"with eigenvalues \[([^]]+)\]\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def list_text(values):
    return "[" + ",".join(fraction_text(v) for v in values) + "]"


def bit_unit(value):
    return "bit" if Fraction(value) == 1 else "bits"


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return [Fraction(piece) for piece in match.group(1).split(",")]


def expected_flow(example):
    eigenvalues = parse_problem(example["problem"])
    steps = [
        make_step("ENTROPY_SETUP", f"eigenvalues={list_text(eigenvalues)}",
                  "S=-sum lambda log2(lambda)"),
    ]
    running = Fraction(0)
    for value in eigenvalues:
        exponent = value.denominator.bit_length() - 1
        term = value * exponent
        steps.append(make_step("LOG2", fraction_text(value), -exponent))
        steps.append(make_step("M", fraction_text(value), exponent,
                               fraction_text(term)))
        new_running = running + term
        steps.append(make_step("A", fraction_text(running),
                               fraction_text(term),
                               fraction_text(new_running)))
        running = new_running
    answer = f"S = {fraction_text(running)} {bit_unit(running)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestVonNeumannEntropyGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = VonNeumannEntropyGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "von_neumann_entropy_dyadic")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(200):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
