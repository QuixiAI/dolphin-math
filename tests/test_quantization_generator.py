import math
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.quantization_generator import QuantizationGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Quantize tensor x=(\([^)]+\)) with int8 scale=([-0-9/]+) and "
    r"zero_point=([-0-9]+) using q=round\(x/scale\)\+zero_point, then "
    r"dequantize and compute sum absolute round-trip error\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_vector(raw):
    return [Fraction(part) for part in raw.strip("()").split(",")]


def vector_text(values):
    return "(" + ",".join(str(value) for value in values) + ")"


def fraction_vector_text(values):
    return "(" + ",".join(fraction_text(value) for value in values) + ")"


def round_half_up(value):
    return math.floor(value + Fraction(1, 2))


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    raw_values = parse_vector(match.group(1))
    scale = Fraction(match.group(2))
    zero_point = int(match.group(3))
    q_values = []
    dequantized = []
    abs_errors = []
    steps = [
        make_step("QUANT_SETUP", f"x={fraction_vector_text(raw_values)}",
                  f"scale={fraction_text(scale)}",
                  f"zero_point={zero_point}"),
    ]
    for index, value in enumerate(raw_values, start=1):
        scaled = value / scale
        shifted = scaled + zero_point
        q_value = round_half_up(shifted)
        q_minus_zp = q_value - zero_point
        deq = q_minus_zp * scale
        error = value - deq
        abs_error = abs(error)
        steps.extend([
            make_step("D", fraction_text(value), fraction_text(scale),
                      fraction_text(scaled)),
            make_step("A", fraction_text(scaled), zero_point,
                      fraction_text(shifted)),
            make_step("ROUND", fraction_text(shifted), q_value),
            make_step("QUANT_VALUE", index, q_value),
            make_step("S", q_value, zero_point, q_minus_zp),
            make_step("M", q_minus_zp, fraction_text(scale),
                      fraction_text(deq)),
            make_step("DEQUANT_VALUE", index, fraction_text(deq)),
            make_step("S", fraction_text(value), fraction_text(deq),
                      fraction_text(error)),
            make_step("ABS_ERROR", index, fraction_text(abs_error)),
        ])
        q_values.append(q_value)
        dequantized.append(deq)
        abs_errors.append(abs_error)
    running = Fraction(0)
    for abs_error in abs_errors:
        new_running = running + abs_error
        steps.append(make_step("A", fraction_text(running),
                               fraction_text(abs_error),
                               fraction_text(new_running)))
        running = new_running
    steps.append(make_step("ROUNDTRIP_ERROR", "sum_abs",
                           fraction_text(running)))
    answer = (
        f"q={vector_text(q_values)}; dequant={fraction_vector_text(dequantized)}; "
        f"sum_abs_error={fraction_text(running)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestQuantizationGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = QuantizationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "quantization_int8_affine")
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
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
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
