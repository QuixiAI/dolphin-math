import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.fractal_iteration_generator import FractalIterationGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Trace the (mandelbrot|julia) iteration z <- z\^2 \+ c for "
    r"(\d+) iterations from "
    r"z0=(\([^)]*\)) with c=(\([^)]*\))\. Report the first step "
    r"with \|z\| > 2, if any\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def frac_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def parse_point(text):
    real, imag = text.strip("()").split(",")
    return Fraction(real), Fraction(imag)


def point_text(z):
    return f"({frac_text(z[0])},{frac_text(z[1])})"


def trace_iteration(steps, n, z, c):
    x, y = z
    x2 = x * x
    y2 = y * y
    real_square = x2 - y2
    two_x = 2 * x
    imag_square = two_x * y
    real = real_square + c[0]
    imag = imag_square + c[1]
    steps.extend([
        make_step("E", frac_text(x), 2, frac_text(x2)),
        make_step("E", frac_text(y), 2, frac_text(y2)),
        make_step("S", frac_text(x2), frac_text(y2),
                  frac_text(real_square)),
        make_step("M", 2, frac_text(x), frac_text(two_x)),
        make_step("M", frac_text(two_x), frac_text(y),
                  frac_text(imag_square)),
        make_step("A", frac_text(real_square), frac_text(c[0]),
                  frac_text(real)),
        make_step("A", frac_text(imag_square), frac_text(c[1]),
                  frac_text(imag)),
        make_step("ITERATE", f"n={n}", f"z={point_text((real, imag))}"),
    ])
    return real, imag


def trace_norm(steps, n, z):
    x, y = z
    x2 = x * x
    y2 = y * y
    total = x2 + y2
    steps.extend([
        make_step("E", frac_text(x), 2, frac_text(x2)),
        make_step("E", frac_text(y), 2, frac_text(y2)),
        make_step("A", frac_text(x2), frac_text(y2), frac_text(total)),
    ])
    return total


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    variant = match.group(1)
    iterations = int(match.group(2))
    z0 = parse_point(match.group(3))
    c = parse_point(match.group(4))
    return {"variant": variant, "iterations": iterations, "z0": z0, "c": c}


def expected_flow(example):
    parts = parse_problem(example["problem"])
    steps = [
        make_step("FRACTAL_SETUP", parts["variant"],
                  f"z0={point_text(parts['z0'])}",
                  f"c={point_text(parts['c'])}",
                  f"N={parts['iterations']}"),
    ]
    z = parts["z0"]
    escaped_at = None
    for n in range(1, parts["iterations"] + 1):
        z = trace_iteration(steps, n, z, parts["c"])
        norm2 = trace_norm(steps, n, z)
        verdict = "escaped" if norm2 > 4 else "bounded"
        steps.append(make_step("ESCAPE_CHECK", f"n={n}",
                               f"norm2={frac_text(norm2)}", verdict))
        if escaped_at is None and norm2 > 4:
            escaped_at = n
            break
    if escaped_at is None:
        answer = f"not escaped after {parts['iterations']} steps"
    else:
        answer = f"escaped at step {escaped_at}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestFractalIterationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FractalIterationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(400):
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
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("mandelbrot", "julia"):
            gen = FractalIterationGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"fractal_iteration_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FractalIterationGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
