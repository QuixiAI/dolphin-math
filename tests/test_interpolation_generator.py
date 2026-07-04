import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.interpolation_generator import InterpolationGenerator
from helpers import DELIM


POINT_RE = re.compile(r"\((-?\d+),(-?\d+)\)")
LAGRANGE_RE = re.compile(
    r"Use Lagrange interpolation through points (.+) to find P\((-?\d+)\)\."
)
NEWTON_RE = re.compile(
    r"Use Newton divided differences through points (.+) to find P\((-?\d+)\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def point_text(points):
    return ", ".join(f"({x},{y})" for x, y in points)


def parse_points(text):
    matches = POINT_RE.findall(text)
    assert len(matches) == 3, text
    return [(int(x), int(y)) for x, y in matches]


def parse_problem(problem):
    match = LAGRANGE_RE.fullmatch(problem)
    if match:
        return {
            "variant": "lagrange",
            "points": parse_points(match.group(1)),
            "target": int(match.group(2)),
        }
    match = NEWTON_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "newton",
        "points": parse_points(match.group(1)),
        "target": int(match.group(2)),
    }


def expected_lagrange(points, target):
    steps = [
        make_step("INTERP_SETUP", "lagrange", f"points={point_text(points)}",
                  f"x={target}"),
    ]
    terms = []
    for i, (x_i, y_i) in enumerate(points):
        basis = Fraction(1)
        for j, (x_j, _) in enumerate(points):
            if i == j:
                continue
            numerator = target - x_j
            denominator = x_i - x_j
            factor = Fraction(numerator, denominator)
            steps.extend([
                make_step("S", target, x_j, numerator),
                make_step("S", x_i, x_j, denominator),
                make_step("D", numerator, denominator, fraction_text(factor)),
                make_step("LAGRANGE_FACTOR", f"L_{i}", f"j={j}",
                          fraction_text(factor)),
                make_step("M", fraction_text(basis), fraction_text(factor),
                          fraction_text(basis * factor)),
            ])
            basis *= factor
        term = y_i * basis
        terms.append(term)
        steps.append(make_step("M", y_i, fraction_text(basis),
                               fraction_text(term)))
    total = Fraction(0)
    for term in terms:
        next_total = total + term
        steps.append(make_step("A", fraction_text(total),
                               fraction_text(term), fraction_text(next_total)))
        total = next_total
    answer = f"P({target}) = {fraction_text(total)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_newton(points, target):
    (x0, y0), (x1, y1), (x2, y2) = points
    steps = [
        make_step("INTERP_SETUP", "newton", f"points={point_text(points)}",
                  f"x={target}"),
    ]
    dy01 = y1 - y0
    dx01 = x1 - x0
    dd01 = Fraction(dy01, dx01)
    dy12 = y2 - y1
    dx12 = x2 - x1
    dd12 = Fraction(dy12, dx12)
    diff_dd = dd12 - dd01
    dx02 = x2 - x0
    dd012 = diff_dd / dx02
    steps.extend([
        make_step("S", y1, y0, dy01),
        make_step("S", x1, x0, dx01),
        make_step("D", dy01, dx01, fraction_text(dd01)),
        make_step("NEWTON_DD", "f[x0,x1]", fraction_text(dd01)),
        make_step("S", y2, y1, dy12),
        make_step("S", x2, x1, dx12),
        make_step("D", dy12, dx12, fraction_text(dd12)),
        make_step("NEWTON_DD", "f[x1,x2]", fraction_text(dd12)),
        make_step("S", fraction_text(dd12), fraction_text(dd01),
                  fraction_text(diff_dd)),
        make_step("S", x2, x0, dx02),
        make_step("D", fraction_text(diff_dd), dx02, fraction_text(dd012)),
        make_step("NEWTON_DD", "f[x0,x1,x2]", fraction_text(dd012)),
    ])
    x_minus_x0 = target - x0
    x_minus_x1 = target - x1
    linear_term = dd01 * x_minus_x0
    product = x_minus_x0 * x_minus_x1
    quad_term = dd012 * product
    partial = Fraction(y0) + linear_term
    total = partial + quad_term
    steps.extend([
        make_step("S", target, x0, x_minus_x0),
        make_step("M", fraction_text(dd01), x_minus_x0,
                  fraction_text(linear_term)),
        make_step("S", target, x1, x_minus_x1),
        make_step("M", x_minus_x0, x_minus_x1, product),
        make_step("M", fraction_text(dd012), product,
                  fraction_text(quad_term)),
        make_step("A", y0, fraction_text(linear_term),
                  fraction_text(partial)),
        make_step("A", fraction_text(partial), fraction_text(quad_term),
                  fraction_text(total)),
    ])
    answer = f"P({target}) = {fraction_text(total)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "lagrange":
        return expected_lagrange(parts["points"], parts["target"])
    return expected_newton(parts["points"], parts["target"])


class TestInterpolationGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = InterpolationGenerator()

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
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in InterpolationGenerator.VARIANTS:
            result = InterpolationGenerator(variant).generate()
            self.assertEqual(result["operation"], f"interpolation_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            InterpolationGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_all_variants_seen_with_random_generator(self):
        seen = {self.gen.generate()["operation"] for _ in range(100)}
        self.assertEqual(seen, {"interpolation_lagrange",
                                "interpolation_newton"})


if __name__ == "__main__":
    unittest.main()
