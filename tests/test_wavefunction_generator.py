import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.wavefunction_generator import WavefunctionGenerator
from helpers import DELIM


POWER_RE = re.compile(
    r"On 0<=x<=(\d+), let psi\(x\)=N\*\(x/L\)\^(\d+)\. Normalize it and "
    r"compute <x> and <x\^2>\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def sqrt_text(value):
    value = Fraction(value)
    if value == 1:
        return "1"
    return f"sqrt({fraction_text(value)})"


def expected_flow(example):
    length_raw, power_raw = POWER_RE.fullmatch(example["problem"]).groups()
    length = int(length_raw)
    power = int(power_raw)
    two_k = 2 * power
    norm_num = two_k + 1
    norm_sq = Fraction(norm_num, length)
    norm = sqrt_text(norm_sq)
    x_den = two_k + 2
    x_num = norm_num * length
    x_expect = Fraction(x_num, x_den)
    x2_den = two_k + 3
    length_sq = length ** 2
    x2_num = norm_num * length_sq
    x2_expect = Fraction(x2_num, x2_den)
    steps = [
        make_step("WAVE_SETUP", "power_interval", f"psi=N*(x/L)^{power}",
                  f"0<=x<={length}"),
        make_step("WAVE_FORMULA",
                  "1=N^2*integral_0^L (x/L)^(2k) dx"),
        make_step("M", 2, power, two_k),
        make_step("A", two_k, 1, norm_num),
        make_step("POWER_INTEGRAL", f"n={two_k}", f"L/{norm_num}"),
        make_step("D", norm_num, length, fraction_text(norm_sq)),
        make_step("WAVE_FORMULA", f"N^2={fraction_text(norm_sq)}"),
        make_step("WAVE_FORMULA",
                  "<x>=N^2*integral_0^L x*(x/L)^(2k) dx"),
        make_step("A", two_k, 2, x_den),
        make_step("POWER_INTEGRAL", f"n={two_k + 1}", f"L^2/{x_den}"),
        make_step("M", norm_num, length, x_num),
        make_step("D", x_num, x_den, fraction_text(x_expect)),
        make_step("WAVE_FORMULA",
                  "<x^2>=N^2*integral_0^L x^2*(x/L)^(2k) dx"),
        make_step("A", two_k, 3, x2_den),
        make_step("POWER_INTEGRAL", f"n={two_k + 2}", f"L^3/{x2_den}"),
        make_step("E", length, 2, length_sq),
        make_step("M", norm_num, length_sq, x2_num),
        make_step("D", x2_num, x2_den, fraction_text(x2_expect)),
    ]
    answer = (
        f"N={norm}; <x>={fraction_text(x_expect)}; "
        f"<x^2>={fraction_text(x2_expect)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestWavefunctionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = WavefunctionGenerator()

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
            match = POWER_RE.fullmatch(result["problem"])
            self.assertIsNotNone(match, result["problem"])
            power = int(match.group(2))
            two_k = 2 * power
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "POWER_INTEGRAL":
                    exponent = int(fields[1].removeprefix("n="))
                    if exponent == two_k:
                        expected = f"L/{exponent + 1}"
                    elif exponent == two_k + 1:
                        expected = f"L^2/{exponent + 1}"
                    else:
                        self.assertEqual(exponent, two_k + 2, raw_step)
                        expected = f"L^3/{exponent + 1}"
                    self.assertEqual(fields[2], expected, raw_step)

    def test_variants_are_available(self):
        for variant in WavefunctionGenerator.VARIANTS:
            result = WavefunctionGenerator(variant).generate()
            self.assertEqual(result["operation"], f"wavefunction_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            WavefunctionGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
