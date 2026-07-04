import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.dft_generator import DFTGenerator, complex_text, dft_values, seq_text
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Compute the length-(2|4) DFT of x=\[([-0-9,]+)\]\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_values(raw):
    return [int(part) for part in raw.split(",")]


def expected_flow(example):
    length_raw, values_raw = PROBLEM_RE.fullmatch(example["problem"]).groups()
    length = int(length_raw)
    values = parse_values(values_raw)
    if length == 2:
        x0, x1 = values
        x0_plus_x1 = x0 + x1
        x0_minus_x1 = x0 - x1
        steps = [
            make_step("DFT_SETUP", "N=2", f"x={seq_text(values)}"),
            make_step("TWIDDLE", "W2=-1"),
            make_step("DFT_BIN", "X0=x0+x1"),
            make_step("A", x0, x1, x0_plus_x1),
            make_step("DFT_BIN", "X1=x0-x1"),
            make_step("S", x0, x1, x0_minus_x1),
        ]
    else:
        x0, x1, x2, x3 = values
        x0_x1 = x0 + x1
        x0_x1_x2 = x0_x1 + x2
        X0 = x0_x1_x2 + x3
        real13 = x0 - x2
        imag1 = x3 - x1
        x0_minus_x1 = x0 - x1
        x0_minus_x1_plus_x2 = x0_minus_x1 + x2
        X2 = x0_minus_x1_plus_x2 - x3
        imag3 = x1 - x3
        steps = [
            make_step("DFT_SETUP", "N=4", f"x={seq_text(values)}"),
            make_step("TWIDDLE", "W4=-i", "W4^2=-1", "W4^3=i"),
            make_step("DFT_BIN", "X0=x0+x1+x2+x3"),
            make_step("A", x0, x1, x0_x1),
            make_step("A", x0_x1, x2, x0_x1_x2),
            make_step("A", x0_x1_x2, x3, X0),
            make_step("DFT_BIN", "X1=(x0-x2)+(x3-x1)i"),
            make_step("S", x0, x2, real13),
            make_step("S", x3, x1, imag1),
            make_step("DFT_BIN", f"X1={complex_text(real13, imag1)}"),
            make_step("DFT_BIN", "X2=x0-x1+x2-x3"),
            make_step("S", x0, x1, x0_minus_x1),
            make_step("A", x0_minus_x1, x2, x0_minus_x1_plus_x2),
            make_step("S", x0_minus_x1_plus_x2, x3, X2),
            make_step("DFT_BIN", "X3=(x0-x2)+(x1-x3)i"),
            make_step("S", x0, x2, real13),
            make_step("S", x1, x3, imag3),
            make_step("DFT_BIN", f"X3={complex_text(real13, imag3)}"),
        ]
    answer = f"X={seq_text(dft_values(values))}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestDFTGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = DFTGenerator()

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

    def test_lengths_are_available(self):
        for length in DFTGenerator.LENGTHS:
            result = DFTGenerator(length).generate()
            self.assertEqual(result["operation"], f"dft_length_{length}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_length_rejected(self):
        with self.assertRaises(ValueError):
            DFTGenerator(3)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
