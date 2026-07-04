import ast
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.pca_generator import PCAGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For points (\[[^\]]+\]), use population covariance \(divide by n\) "
    r"to compute 2D PCA and project each centered point onto the principal "
    r"component\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def point_text(point):
    return f"({fraction_text(point[0])},{fraction_text(point[1])})"


def points_text(points):
    return "[" + ", ".join(point_text(point) for point in points) + "]"


def vector_text(values):
    return "(" + ",".join(fraction_text(value) for value in values) + ")"


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(fraction_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def parse_points(problem):
    match = PROBLEM_RE.fullmatch(problem)
    if not match:
        raise AssertionError(problem)
    return [(Fraction(x), Fraction(y)) for x, y in ast.literal_eval(match.group(1))]


def add_running_steps(steps, values):
    running = Fraction(0)
    for value in values:
        new_running = running + value
        steps.append(make_step("A", fraction_text(running),
                               fraction_text(value),
                               fraction_text(new_running)))
        running = new_running
    return running


def expected_flow(example):
    points = parse_points(example["problem"])
    n = len(points)
    steps = [
        make_step("PCA_SETUP", f"points={points_text(points)}",
                  "population covariance"),
    ]
    sum_x = add_running_steps(steps, [point[0] for point in points])
    mean_x = sum_x / n
    steps.append(make_step("D", fraction_text(sum_x), n, fraction_text(mean_x)))
    sum_y = add_running_steps(steps, [point[1] for point in points])
    mean_y = sum_y / n
    steps.append(make_step("D", fraction_text(sum_y), n, fraction_text(mean_y)))

    centered = []
    for index, point in enumerate(points, start=1):
        cx = point[0] - mean_x
        cy = point[1] - mean_y
        centered.append((cx, cy))
        steps.extend([
            make_step("S", fraction_text(point[0]), fraction_text(mean_x),
                      fraction_text(cx)),
            make_step("S", fraction_text(point[1]), fraction_text(mean_y),
                      fraction_text(cy)),
            make_step("CENTER", f"P{index}", point_text((cx, cy))),
        ])

    cov_entries = []
    for name in ("xx", "xy", "yy"):
        products = []
        for cx, cy in centered:
            if name == "xx":
                value = cx ** 2
                steps.append(make_step("E", fraction_text(cx), 2,
                                       fraction_text(value)))
            elif name == "yy":
                value = cy ** 2
                steps.append(make_step("E", fraction_text(cy), 2,
                                       fraction_text(value)))
            else:
                value = cx * cy
                steps.append(make_step("M", fraction_text(cx),
                                       fraction_text(cy),
                                       fraction_text(value)))
            products.append(value)
        total = add_running_steps(steps, products)
        entry = total / n
        steps.append(make_step("D", fraction_text(total), n,
                               fraction_text(entry)))
        steps.append(make_step("COV_ENTRY", name, fraction_text(entry)))
        cov_entries.append(entry)

    cov_xx, cov_xy, cov_yy = cov_entries
    covariance = [[cov_xx, cov_xy], [cov_xy, cov_yy]]
    if cov_xx >= cov_yy:
        pc = (Fraction(1), Fraction(0))
        pc_name = "e1"
        relation = ">="
    else:
        pc = (Fraction(0), Fraction(1))
        pc_name = "e2"
        relation = "<"
    steps.extend([
        make_step("EIGENVALUES", "diagonal covariance",
                  f"lambda_x={fraction_text(cov_xx)}, "
                  f"lambda_y={fraction_text(cov_yy)}"),
        make_step("CHECK", "lambda_x vs lambda_y",
                  f"{fraction_text(cov_xx)} {relation} {fraction_text(cov_yy)}",
                  f"pc={pc_name}"),
        make_step("PC_VECTOR", pc_name, vector_text(pc)),
    ])

    scores = []
    for index, (cx, cy) in enumerate(centered, start=1):
        term_x = cx * pc[0]
        term_y = cy * pc[1]
        score_value = term_x + term_y
        steps.extend([
            make_step("M", fraction_text(cx), fraction_text(pc[0]),
                      fraction_text(term_x)),
            make_step("M", fraction_text(cy), fraction_text(pc[1]),
                      fraction_text(term_y)),
            make_step("A", fraction_text(term_x), fraction_text(term_y),
                      fraction_text(score_value)),
            make_step("PROJECT", f"P{index}", fraction_text(score_value)),
        ])
        scores.append(score_value)

    answer = (
        f"cov={matrix_text(covariance)}; pc={vector_text(pc)}; "
        f"scores={','.join(fraction_text(score) for score in scores)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestPCAGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = PCAGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "pca_2d_projection")
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

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
