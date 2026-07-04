import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.complex_locus_generator import ComplexLocusGenerator
from helpers import DELIM


CIRCLE_RE = re.compile(
    r"Identify the locus \|z - (\(-?\d+,-?\d+\))\| = (\d+), "
    r"where z=x\+iy\. Give the Cartesian equation and type\."
)
BISECTOR_RE = re.compile(
    r"Identify the locus \|z - (\(-?\d+,-?\d+\))\| = "
    r"\|z - (\(-?\d+,-?\d+\))\|, where z=x\+iy\. Give the "
    r"Cartesian equation and type\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_point(text):
    x, y = text.strip("()").split(",")
    return int(x), int(y)


def point_text(point):
    return f"({point[0]},{point[1]})"


def square_binomial(var, value):
    if value == 0:
        return f"{var}^2"
    if value > 0:
        return f"({var} - {value})^2"
    return f"({var} + {-value})^2"


def line_text(a, b, c):
    parts = []
    for coef, var in ((a, "x"), (b, "y")):
        if coef == 0:
            continue
        abs_coef = abs(coef)
        term = var if abs_coef == 1 else f"{abs_coef}{var}"
        if not parts:
            parts.append(term if coef > 0 else f"-{term}")
        else:
            parts.append(f"+ {term}" if coef > 0 else f"- {term}")
    if c != 0:
        if not parts:
            parts.append(str(c))
        else:
            parts.append(f"+ {c}" if c > 0 else f"- {-c}")
    return " ".join(parts) + " = 0"


def parse_problem(problem):
    match = CIRCLE_RE.fullmatch(problem)
    if match:
        return {
            "variant": "circle",
            "center": parse_point(match.group(1)),
            "radius": int(match.group(2)),
        }
    match = BISECTOR_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "bisector",
        "p": parse_point(match.group(1)),
        "q": parse_point(match.group(2)),
    }


def expected_circle(center, radius):
    r2 = radius * radius
    equation = (
        f"{square_binomial('x', center[0])} + "
        f"{square_binomial('y', center[1])} = {r2}"
    )
    steps = [
        make_step("LOCUS_SETUP", "z=x+iy", f"center={point_text(center)}",
                  f"radius={radius}"),
        make_step("DIST_FORMULA",
                  f"sqrt({square_binomial('x', center[0])}+"
                  f"{square_binomial('y', center[1])})={radius}"),
        make_step("E", radius, 2, r2),
        make_step("CIRCLE_EQ", equation),
    ]
    answer = (
        f"{equation}; type = circle; center = {point_text(center)}; "
        f"radius = {radius}"
    )
    return steps, answer


def expected_bisector(p, q):
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    a = 2 * dx
    b = 2 * dy
    p_norm = p[0] * p[0] + p[1] * p[1]
    q_norm = q[0] * q[0] + q[1] * q[1]
    c = p_norm - q_norm
    equation = line_text(a, b, c)
    steps = [
        make_step("LOCUS_SETUP", "z=x+iy", f"p={point_text(p)}",
                  f"q={point_text(q)}"),
        make_step("DIST_FORMULA",
                  f"{square_binomial('x', p[0])}+"
                  f"{square_binomial('y', p[1])} = "
                  f"{square_binomial('x', q[0])}+"
                  f"{square_binomial('y', q[1])}"),
        make_step("EXPAND", "cancel x^2 and y^2"),
        make_step("S", q[0], p[0], dx),
        make_step("M", 2, dx, a),
        make_step("S", q[1], p[1], dy),
        make_step("M", 2, dy, b),
        make_step("E", p[0], 2, p[0] * p[0]),
        make_step("E", p[1], 2, p[1] * p[1]),
        make_step("A", p[0] * p[0], p[1] * p[1], p_norm),
        make_step("E", q[0], 2, q[0] * q[0]),
        make_step("E", q[1], 2, q[1] * q[1]),
        make_step("A", q[0] * q[0], q[1] * q[1], q_norm),
        make_step("S", p_norm, q_norm, c),
        make_step("LINE_EQ", equation),
    ]
    return steps, f"{equation}; type = line"


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "circle":
        steps, answer = expected_circle(parts["center"], parts["radius"])
    else:
        steps, answer = expected_bisector(parts["p"], parts["q"])
    steps.append(make_step("Z", answer))
    return steps, answer


class TestComplexLocusGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ComplexLocusGenerator()

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
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("circle", "bisector"):
            gen = ComplexLocusGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"complex_locus_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ComplexLocusGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
