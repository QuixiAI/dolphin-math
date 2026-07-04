import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.lie_exponential_generator import LieExponentialGenerator
from helpers import DELIM


SO2_RE = re.compile(
    r"Exponentiate the so\(2\) element theta=(-?\d+) deg with J=(\[\[.*\]\])\."
)
SO3_RE = re.compile(
    r"Exponentiate the so\(3\) element theta=(-?\d+) deg about the "
    r"([xyz])-axis with K=(\[\[.*\]\])\."
)

TRIG = {
    0: ("1", "0"),
    30: ("sqrt3/2", "1/2"),
    45: ("sqrt2/2", "sqrt2/2"),
    60: ("1/2", "sqrt3/2"),
    90: ("0", "1"),
    120: ("-1/2", "sqrt3/2"),
    135: ("-sqrt2/2", "sqrt2/2"),
    150: ("-sqrt3/2", "1/2"),
    180: ("-1", "0"),
    210: ("-sqrt3/2", "-1/2"),
    225: ("-sqrt2/2", "-sqrt2/2"),
    240: ("-1/2", "-sqrt3/2"),
    270: ("0", "-1"),
    300: ("1/2", "-sqrt3/2"),
    315: ("sqrt2/2", "-sqrt2/2"),
    330: ("sqrt3/2", "-1/2"),
}

SO3_GENERATORS = {
    "x": [[0, 0, 0], [0, 0, -1], [0, 1, 0]],
    "y": [[0, 0, 1], [0, 0, 0], [-1, 0, 0]],
    "z": [[0, -1, 0], [1, 0, 0], [0, 0, 0]],
}

SO3_SQUARES = {
    "x": [[0, 0, 0], [0, -1, 0], [0, 0, -1]],
    "y": [[-1, 0, 0], [0, 0, 0], [0, 0, -1]],
    "z": [[-1, 0, 0], [0, -1, 0], [0, 0, 0]],
}


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def mat(matrix):
    return "[" + ", ".join(
        "[" + ", ".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def neg_text(value):
    if value == "0":
        return "0"
    if value.startswith("-"):
        return value[1:]
    return f"-{value}"


def so2_matrix(cos_text, sin_text):
    return [[cos_text, neg_text(sin_text)], [sin_text, cos_text]]


def so3_matrix(axis, cos_text, sin_text):
    if axis == "x":
        return [
            ["1", "0", "0"],
            ["0", cos_text, neg_text(sin_text)],
            ["0", sin_text, cos_text],
        ]
    if axis == "y":
        return [
            [cos_text, "0", sin_text],
            ["0", "1", "0"],
            [neg_text(sin_text), "0", cos_text],
        ]
    return [
        [cos_text, neg_text(sin_text), "0"],
        [sin_text, cos_text, "0"],
        ["0", "0", "1"],
    ]


def so3_expr_matrix(axis):
    if axis == "x":
        return [
            ["1", "0", "0"],
            ["0", "cos(theta)", "-sin(theta)"],
            ["0", "sin(theta)", "cos(theta)"],
        ]
    if axis == "y":
        return [
            ["cos(theta)", "0", "sin(theta)"],
            ["0", "1", "0"],
            ["-sin(theta)", "0", "cos(theta)"],
        ]
    return [
        ["cos(theta)", "-sin(theta)", "0"],
        ["sin(theta)", "cos(theta)", "0"],
        ["0", "0", "1"],
    ]


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ", ".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def parse_problem(problem):
    match = SO2_RE.fullmatch(problem)
    if match:
        theta = int(match.group(1))
        return {"variant": "so2", "theta": theta}
    match = SO3_RE.fullmatch(problem)
    assert match is not None, problem
    theta = int(match.group(1))
    axis = match.group(2)
    return {"variant": "so3", "theta": theta, "axis": axis}


def expected_so2(theta):
    angle = theta % 360
    cos_text, sin_text = TRIG[angle]
    J = [[0, -1], [1, 0]]
    result = so2_matrix(cos_text, sin_text)
    expr = [["cos(theta)", "-sin(theta)"],
            ["sin(theta)", "cos(theta)"]]
    steps = [
        make_step("LIE_EXP_SETUP", "SO2", f"theta={theta} deg",
                  f"J={mat(J)}", "goal=e^(theta J)"),
        make_step("MOD_REDUCE", theta, "mod 360", angle),
        make_step("MATRIX_POWER", "J^2", "-I"),
        make_step("SERIES_GROUP", "even powers", "cos(theta)I"),
        make_step("SERIES_GROUP", "odd powers", "sin(theta)J"),
        make_step("LIE_EXP_FORM", "e^(theta J)",
                  "cos(theta)I + sin(theta)J"),
        make_step("TABLE_LOOKUP", f"cos {angle} deg", cos_text),
        make_step("TABLE_LOOKUP", f"sin {angle} deg", sin_text),
    ]
    for i in range(2):
        for j in range(2):
            steps.append(make_step("MAT_ENTRY", f"({i + 1},{j + 1})",
                                   expr[i][j], result[i][j]))
    steps.extend([
        make_step("CHECK", "R^T R", "I", "orthogonal"),
        make_step("CHECK", "det R", "1", "proper rotation"),
    ])
    answer = f"e^(theta J)={matrix_text(result)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_so3(theta, axis):
    angle = theta % 360
    cos_text, sin_text = TRIG[angle]
    K = SO3_GENERATORS[axis]
    K2 = SO3_SQUARES[axis]
    result = so3_matrix(axis, cos_text, sin_text)
    expr = so3_expr_matrix(axis)
    steps = [
        make_step("LIE_EXP_SETUP", "SO3", f"axis={axis}",
                  f"theta={theta} deg", f"K={mat(K)}"),
        make_step("MOD_REDUCE", theta, "mod 360", angle),
        make_step("MATRIX_POWER", "K^2", mat(K2)),
        make_step("RODRIGUES_FORM", "e^(theta K)",
                  "I + sin(theta)K + (1-cos(theta))K^2"),
        make_step("TABLE_LOOKUP", f"cos {angle} deg", cos_text),
        make_step("TABLE_LOOKUP", f"sin {angle} deg", sin_text),
    ]
    for i in range(3):
        for j in range(3):
            steps.append(make_step("MAT_ENTRY", f"({i + 1},{j + 1})",
                                   expr[i][j], result[i][j]))
    steps.extend([
        make_step("CHECK", "R^T R", "I", "orthogonal"),
        make_step("CHECK", "det R", "1", "proper rotation"),
    ])
    answer = f"e^(theta K_{axis})={matrix_text(result)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "so2":
        return expected_so2(parts["theta"])
    return expected_so3(parts["theta"], parts["axis"])


class TestLieExponentialGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LieExponentialGenerator()

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

    def test_matrix_power_steps(self):
        for axis, K in SO3_GENERATORS.items():
            K2 = [
                [sum(K[i][k] * K[k][j] for k in range(3))
                 for j in range(3)]
                for i in range(3)
            ]
            self.assertEqual(K2, SO3_SQUARES[axis])

    def test_variants_are_available(self):
        for variant in ("so2", "so3"):
            result = LieExponentialGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"lie_exponential_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_so3_axes_are_reachable(self):
        random.seed(7)
        gen = LieExponentialGenerator("so3")
        axes = {parse_problem(gen.generate()["problem"])["axis"]
                for _ in range(100)}
        self.assertEqual(axes, {"x", "y", "z"})

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            LieExponentialGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
