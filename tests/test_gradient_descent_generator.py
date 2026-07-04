import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.gradient_descent_generator import (
    GradientDescentGenerator,
    point_text,
)
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Starting at \(([^,]+),([^)]+)\) for f\(x,y\)=1/2\*\((\d+)x\^2\+"
    r"(\d+)y\^2\), run 3 gradient-descent steps with step size eta=([^.]*)\."
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
    x = Fraction(match.group(1))
    y = Fraction(match.group(2))
    a = int(match.group(3))
    b = int(match.group(4))
    eta = Fraction(match.group(5))
    return x, y, a, b, eta


def expected_flow(example):
    x, y, a, b, eta = parse_problem(example["problem"])
    steps = [
        make_step("GD_SETUP", f"f(x,y)=1/2*({a}x^2+{b}y^2)",
                  f"start={point_text(x, y)}", f"eta={fraction_text(eta)}"),
        make_step("GRADIENT_FORMULA", f"grad=({a}x,{b}y)"),
    ]
    for index in range(1, GradientDescentGenerator.STEPS + 1):
        grad_x = a * x
        grad_y = b * y
        update_x = eta * grad_x
        update_y = eta * grad_y
        new_x = x - update_x
        new_y = y - update_y
        steps += [
            make_step("M", a, fraction_text(x), fraction_text(grad_x)),
            make_step("M", b, fraction_text(y), fraction_text(grad_y)),
            make_step("M", fraction_text(eta), fraction_text(grad_x),
                      fraction_text(update_x)),
            make_step("S", fraction_text(x), fraction_text(update_x),
                      fraction_text(new_x)),
            make_step("M", fraction_text(eta), fraction_text(grad_y),
                      fraction_text(update_y)),
            make_step("S", fraction_text(y), fraction_text(update_y),
                      fraction_text(new_y)),
            make_step("ITERATE", f"k={index}", point_text(new_x, new_y)),
        ]
        x, y = new_x, new_y

    x_sq = x ** 2
    y_sq = y ** 2
    ax_sq = a * x_sq
    by_sq = b * y_sq
    doubled_value = ax_sq + by_sq
    value = doubled_value / 2
    steps += [
        make_step("E", fraction_text(x), 2, fraction_text(x_sq)),
        make_step("M", a, fraction_text(x_sq), fraction_text(ax_sq)),
        make_step("E", fraction_text(y), 2, fraction_text(y_sq)),
        make_step("M", b, fraction_text(y_sq), fraction_text(by_sq)),
        make_step("A", fraction_text(ax_sq), fraction_text(by_sq),
                  fraction_text(doubled_value)),
        make_step("D", fraction_text(doubled_value), 2, fraction_text(value)),
    ]
    answer = (
        f"x_3={fraction_text(x)}, y_3={fraction_text(y)}, "
        f"f(x_3,y_3)={fraction_text(value)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestGradientDescentGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = GradientDescentGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "gradient_descent_quadratic")
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

    def test_step_size_is_positive(self):
        for _ in range(300):
            *_, eta = parse_problem(self.gen.generate()["problem"])
            self.assertGreater(eta, 0)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
