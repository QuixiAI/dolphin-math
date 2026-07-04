import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.fourier_series_generator import (
    FourierSeriesGenerator,
    over_pi_text,
)
from helpers import DELIM


SQUARE_RE = re.compile(
    r"For the 2pi-periodic square wave f\(x\)=(\d+) on \(0,pi\) and "
    r"-(\d+) on \(-pi,0\), compute b_(\d+) by integration\."
)
SAW_RE = re.compile(
    r"For the 2pi-periodic sawtooth f\(x\)=(\d+)\*x on \(-pi,pi\), "
    r"compute b_(\d+) by integration\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_square(problem):
    match = SQUARE_RE.fullmatch(problem)
    amplitude = int(match.group(1))
    assert amplitude == int(match.group(2))
    n = int(match.group(3))
    parity = -1 if n % 2 else 1
    factor = 1 - parity
    two_a = 2 * amplitude
    numerator = two_a * factor
    rational_part = Fraction(numerator, n)
    coefficient = over_pi_text(rational_part)
    steps = [
        make_step("FOURIER_SETUP", "square", f"A={amplitude}", f"n={n}"),
        make_step("SYMMETRY", "odd function", "a0=0, a_n=0"),
        make_step("INTEGRAL", "b_n=(2/pi)*int_0^pi A sin(nx) dx"),
        make_step("ANTIDERIVATIVE", "-A*cos(nx)/n"),
        make_step("PARITY", f"(-1)^n={parity}"),
        make_step("S", 1, parity, factor),
        make_step("M", 2, amplitude, two_a),
        make_step("M", two_a, factor, numerator),
        make_step("D", numerator, n, fraction_text(rational_part)),
        make_step("FOURIER_COEF", f"b_{n}={coefficient}"),
    ]
    answer = f"a0=0, a_n=0, b_{n}={coefficient}"
    return steps, answer


def expected_sawtooth(problem):
    match = SAW_RE.fullmatch(problem)
    amplitude = int(match.group(1))
    n = int(match.group(2))
    parity = 1 if n % 2 else -1
    two_a = 2 * amplitude
    signed_num = two_a * parity
    coefficient = Fraction(signed_num, n)
    steps = [
        make_step("FOURIER_SETUP", "sawtooth", f"A={amplitude}", f"n={n}"),
        make_step("SYMMETRY", "odd function", "a0=0, a_n=0"),
        make_step("INTEGRAL", "b_n=(1/pi)*int_-pi^pi A*x*sin(nx) dx"),
        make_step("INTEGRATION_BY_PARTS", "u=x", "dv=sin(nx)dx"),
        make_step("PARITY", f"(-1)^(n+1)={parity}"),
        make_step("M", 2, amplitude, two_a),
        make_step("M", two_a, parity, signed_num),
        make_step("D", signed_num, n, fraction_text(coefficient)),
        make_step("FOURIER_COEF", f"b_{n}={fraction_text(coefficient)}"),
    ]
    answer = f"a0=0, a_n=0, b_{n}={fraction_text(coefficient)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if SQUARE_RE.fullmatch(problem):
        steps, answer = expected_square(problem)
    else:
        steps, answer = expected_sawtooth(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestFourierSeriesGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = FourierSeriesGenerator()

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
                if fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in FourierSeriesGenerator.VARIANTS:
            result = FourierSeriesGenerator(variant).generate()
            self.assertEqual(result["operation"], f"fourier_series_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FourierSeriesGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
