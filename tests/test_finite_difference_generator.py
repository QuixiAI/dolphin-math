import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.finite_difference_generator import FiniteDifferenceGenerator
from helpers import DELIM


TABLE_RE = re.compile(
    r"Build the forward-difference table for x=\[([^\]]+)\] "
    r"and y=\[([^\]]+)\] through second differences\."
)
FORWARD_RE = re.compile(
    r"Use the forward difference with h=(\d+), f\((-?\d+)\)=(-?\d+), "
    r"and f\((-?\d+)\)=(-?\d+) to estimate f'\((-?\d+)\)\."
)
CENTRAL_RE = re.compile(
    r"Use the central difference with h=(\d+), f\((-?\d+)\)=(-?\d+), "
    r"and f\((-?\d+)\)=(-?\d+) to estimate f'\((-?\d+)\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def list_text(values):
    return "[" + ", ".join(fraction_text(v) for v in values) + "]"


def parse_list(text):
    return [Fraction(part.strip()) for part in text.split(",")]


def parse_problem(problem):
    match = TABLE_RE.fullmatch(problem)
    if match:
        return {
            "variant": "table",
            "xs": parse_list(match.group(1)),
            "ys": parse_list(match.group(2)),
        }
    match = FORWARD_RE.fullmatch(problem)
    if match:
        h = int(match.group(1))
        x0 = int(match.group(2))
        self_x = int(match.group(6))
        assert x0 == self_x
        assert int(match.group(4)) == x0 + h
        return {
            "variant": "forward_derivative",
            "h": h,
            "x0": x0,
            "y0": Fraction(match.group(3)),
            "y1": Fraction(match.group(5)),
        }
    match = CENTRAL_RE.fullmatch(problem)
    assert match is not None, problem
    h = int(match.group(1))
    left_x = int(match.group(2))
    right_x = int(match.group(4))
    x0 = int(match.group(6))
    assert left_x == x0 - h
    assert right_x == x0 + h
    return {
        "variant": "central_derivative",
        "h": h,
        "x0": x0,
        "left_y": Fraction(match.group(3)),
        "right_y": Fraction(match.group(5)),
    }


def expected_table(parts):
    xs = parts["xs"]
    ys = parts["ys"]
    first = [ys[i + 1] - ys[i] for i in range(3)]
    second = [first[i + 1] - first[i] for i in range(2)]
    steps = [
        make_step("FINITE_DIFF_SETUP", "table", f"x={list_text(xs)}",
                  f"y={list_text(ys)}"),
    ]
    for i in range(3):
        steps.append(make_step("S", fraction_text(ys[i + 1]),
                               fraction_text(ys[i]), fraction_text(first[i])))
    steps.append(make_step("DIFF_ROW", "Delta y", list_text(first)))
    for i in range(2):
        steps.append(make_step("S", fraction_text(first[i + 1]),
                               fraction_text(first[i]),
                               fraction_text(second[i])))
    steps.append(make_step("DIFF_ROW", "Delta2 y", list_text(second)))
    answer = f"Delta y = {list_text(first)}; Delta2 y = {list_text(second)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_forward(parts):
    h = parts["h"]
    x0 = parts["x0"]
    y0 = parts["y0"]
    y1 = parts["y1"]
    numerator = y1 - y0
    derivative = Fraction(numerator, h)
    steps = [
        make_step("FINITE_DIFF_SETUP", "forward_derivative",
                  f"x0={x0},h={h}",
                  f"f0={fraction_text(y0)},f1={fraction_text(y1)}"),
        make_step("S", fraction_text(y1), fraction_text(y0),
                  fraction_text(numerator)),
        make_step("D", fraction_text(numerator), h,
                  fraction_text(derivative)),
    ]
    answer = f"forward f'({x0}) = {fraction_text(derivative)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_central(parts):
    h = parts["h"]
    x0 = parts["x0"]
    left_y = parts["left_y"]
    right_y = parts["right_y"]
    numerator = right_y - left_y
    denominator = 2 * h
    derivative = Fraction(numerator, denominator)
    steps = [
        make_step("FINITE_DIFF_SETUP", "central_derivative",
                  f"x0={x0},h={h}",
                  f"f-={fraction_text(left_y)},f+={fraction_text(right_y)}"),
        make_step("S", fraction_text(right_y), fraction_text(left_y),
                  fraction_text(numerator)),
        make_step("M", 2, h, denominator),
        make_step("D", fraction_text(numerator), denominator,
                  fraction_text(derivative)),
    ]
    answer = f"central f'({x0}) = {fraction_text(derivative)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "table":
        return expected_table(parts)
    if parts["variant"] == "forward_derivative":
        return expected_forward(parts)
    return expected_central(parts)


class TestFiniteDifferenceGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = FiniteDifferenceGenerator()

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
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in FiniteDifferenceGenerator.VARIANTS:
            result = FiniteDifferenceGenerator(variant).generate()
            self.assertEqual(result["operation"], f"finite_difference_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FiniteDifferenceGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_all_variants_seen_with_random_generator(self):
        seen = {self.gen.generate()["operation"] for _ in range(200)}
        self.assertEqual(
            seen,
            {"finite_difference_table",
             "finite_difference_forward_derivative",
             "finite_difference_central_derivative"},
        )


if __name__ == "__main__":
    unittest.main()
