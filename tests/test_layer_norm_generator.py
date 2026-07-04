import math
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.layer_norm_generator import LayerNormGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Apply LayerNorm to x=(\([^)]+\)) with gamma=(\([^)]+\)) and "
    r"beta=(\([^)]+\))\. Use population variance and epsilon=0\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_vector(raw):
    return tuple(Fraction(part) for part in raw.strip("()").split(","))


def vector_text(values):
    return "(" + ",".join(fraction_text(value) for value in values) + ")"


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    x = parse_vector(match.group(1))
    gamma = parse_vector(match.group(2))
    beta = parse_vector(match.group(3))
    total = x[0] + x[1]
    mean = total / 2
    devs = [value - mean for value in x]
    squares = [dev * dev for dev in devs]
    square_sum = squares[0] + squares[1]
    variance = square_sum / 2
    std = math.isqrt(variance.numerator // variance.denominator)
    normalized = [dev / std for dev in devs]
    scaled = [gamma[i] * normalized[i] for i in range(2)]
    output = [scaled[i] + beta[i] for i in range(2)]
    steps = [
        make_step("LAYERNORM_SETUP", f"x={vector_text(x)}",
                  f"gamma={vector_text(gamma)}", f"beta={vector_text(beta)}"),
        make_step("A", fraction_text(x[0]), fraction_text(x[1]),
                  fraction_text(total)),
        make_step("D", fraction_text(total), 2, fraction_text(mean)),
        make_step("MEAN", fraction_text(mean)),
    ]
    for index, value in enumerate(x):
        steps.extend([
            make_step("S", fraction_text(value), fraction_text(mean),
                      fraction_text(devs[index])),
            make_step("E", fraction_text(devs[index]), 2,
                      fraction_text(squares[index])),
        ])
    steps.extend([
        make_step("A", fraction_text(squares[0]), fraction_text(squares[1]),
                  fraction_text(square_sum)),
        make_step("D", fraction_text(square_sum), 2, fraction_text(variance)),
        make_step("VARIANCE", fraction_text(variance)),
        make_step("ROOT", f"sqrt({fraction_text(variance)})", std),
        make_step("STD", std),
    ])
    for index in range(2):
        steps.extend([
            make_step("D", fraction_text(devs[index]), std,
                      fraction_text(normalized[index])),
            make_step("NORMALIZE", index + 1,
                      fraction_text(normalized[index])),
            make_step("M", fraction_text(gamma[index]),
                      fraction_text(normalized[index]),
                      fraction_text(scaled[index])),
            make_step("A", fraction_text(scaled[index]),
                      fraction_text(beta[index]),
                      fraction_text(output[index])),
            make_step("SCALE_SHIFT", index + 1,
                      fraction_text(output[index])),
        ])
    answer = (
        f"mean={fraction_text(mean)}; variance={fraction_text(variance)}; "
        f"normalized={vector_text(normalized)}; y={vector_text(output)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestLayerNormGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = LayerNormGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "layer_norm_exact_2d")
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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    radicand = Fraction(fields[1][5:-1])
                    self.assertEqual(math.isqrt(radicand.numerator),
                                     int(fields[2]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
