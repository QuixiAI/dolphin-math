import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.kernel_evaluation_generator import KernelEvaluationGenerator
from helpers import DELIM


POLY_RE = re.compile(
    r"Compute the Gram matrix for points (.+) using polynomial kernel "
    r"K\(x,z\)=\(x dot z \+ c\)\^d with c=([^ ]+) and d=([0-9]+)\."
)
RBF_RE = re.compile(
    r"Compute the Gram matrix for points (.+) using RBF kernel "
    r"K\(x,z\)=exp\(-gamma \|\|x-z\|\|\^2\) with gamma=([^ ]+)\."
)
POINT_RE = re.compile(r"([ABC])=\(([^,]+),([^)]+)\)")


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def vector_text(vector):
    return "(" + ",".join(fraction_text(value) for value in vector) + ")"


def points_text(labels, vectors):
    return ", ".join(
        f"{label}={vector_text(vector)}"
        for label, vector in zip(labels, vectors)
    )


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def exp_text(scale):
    scale = Fraction(scale)
    if scale == 0:
        return "1"
    return f"exp(-{fraction_text(scale)})"


def parse_points(raw):
    parsed = POINT_RE.findall(raw)
    labels = [label for label, _, _ in parsed]
    vectors = [(int(x), int(y)) for _, x, y in parsed]
    return labels, vectors


def expected_polynomial(problem):
    match = POLY_RE.fullmatch(problem)
    labels, vectors = parse_points(match.group(1))
    constant = int(match.group(2))
    degree = int(match.group(3))
    steps = [
        make_step("KERNEL_SETUP", "type=polynomial",
                  f"points={points_text(labels, vectors)}",
                  f"c={constant},d={degree}"),
    ]
    matrix = []
    for row, left in enumerate(vectors):
        matrix_row = []
        for col, right in enumerate(vectors):
            products = [left[i] * right[i] for i in range(2)]
            dot = products[0] + products[1]
            base = dot + constant
            value = base ** degree
            pair = f"{labels[row]},{labels[col]}"
            steps.extend([
                make_step("M", left[0], right[0], products[0]),
                make_step("M", left[1], right[1], products[1]),
                make_step("A", products[0], products[1], dot),
                make_step("DOT", pair, dot),
                make_step("A", dot, constant, base),
                make_step("KERNEL_BASE", pair, f"dot+c={dot}+{constant}",
                          base),
                make_step("E", base, degree, value),
                make_step("KERNEL_VALUE", pair, value),
            ])
            matrix_row.append(value)
        matrix.append(matrix_row)
    answer = f"K={matrix_text(matrix)}"
    return steps, answer


def expected_rbf(problem):
    match = RBF_RE.fullmatch(problem)
    labels, vectors = parse_points(match.group(1))
    gamma = Fraction(match.group(2))
    steps = [
        make_step("KERNEL_SETUP", "type=rbf",
                  f"points={points_text(labels, vectors)}",
                  f"gamma={fraction_text(gamma)}"),
    ]
    matrix = []
    for row, left in enumerate(vectors):
        matrix_row = []
        for col, right in enumerate(vectors):
            dx = left[0] - right[0]
            dy = left[1] - right[1]
            dx2 = dx ** 2
            dy2 = dy ** 2
            dist2 = dx2 + dy2
            scale = gamma * dist2
            exponent = -scale
            value = exp_text(scale)
            pair = f"{labels[row]},{labels[col]}"
            steps.extend([
                make_step("S", left[0], right[0], dx),
                make_step("E", dx, 2, dx2),
                make_step("S", left[1], right[1], dy),
                make_step("E", dy, 2, dy2),
                make_step("A", dx2, dy2, dist2),
                make_step("DIST2", pair, dist2),
                make_step("M", fraction_text(gamma), dist2,
                          fraction_text(scale)),
                make_step("KERNEL_EXPONENT", pair, fraction_text(exponent)),
                make_step("KERNEL_VALUE", pair, value),
            ])
            matrix_row.append(value)
        matrix.append(matrix_row)
    answer = f"K={matrix_text(matrix)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if POLY_RE.fullmatch(problem):
        steps, answer = expected_polynomial(problem)
    elif RBF_RE.fullmatch(problem):
        steps, answer = expected_rbf(problem)
    else:
        raise AssertionError(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestKernelEvaluationGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = KernelEvaluationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["operation"].startswith("kernel_evaluation_"))
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

    def test_variants_are_available(self):
        for variant in KernelEvaluationGenerator.VARIANTS:
            result = KernelEvaluationGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"kernel_evaluation_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            KernelEvaluationGenerator("bogus")

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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
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
