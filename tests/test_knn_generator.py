import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.knn_generator import KNNGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Classify query q=\(([^,]+),([^)]+)\) by 3-NN using squared Euclidean "
    r"distance\. Training points: (.+)\."
)
POINT_RE = re.compile(r"P(\d+)=\((-?\d+),(-?\d+),([AB])\)")
LABELS = ["A", "B"]
K = 3


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def point_text(point):
    return f"({point[0]},{point[1]})"


def training_text(points):
    return ", ".join(
        f"P{index}=({point[0]},{point[1]},{label})"
        for index, (point, label) in enumerate(points, start=1)
    )


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    if not match:
        raise AssertionError(problem)
    query = (int(match.group(1)), int(match.group(2)))
    points = [
        ((int(x), int(y)), label)
        for _, x, y, label in POINT_RE.findall(match.group(3))
    ]
    return query, points


def neighbor_text(rows):
    return ",".join(
        f"P{index}:{distance}:{label}" for distance, index, label in rows
    )


def expected_flow(example):
    query, points = parse_problem(example["problem"])
    steps = [
        make_step("KNN_SETUP", f"q={point_text(query)}", f"k={K}",
                  f"training={training_text(points)}"),
    ]
    rows = []
    for index, (point, label) in enumerate(points, start=1):
        dx = query[0] - point[0]
        dy = query[1] - point[1]
        dx2 = dx ** 2
        dy2 = dy ** 2
        dist2 = dx2 + dy2
        steps.extend([
            make_step("S", query[0], point[0], dx),
            make_step("E", dx, 2, dx2),
            make_step("S", query[1], point[1], dy),
            make_step("E", dy, 2, dy2),
            make_step("A", dx2, dy2, dist2),
            make_step("KNN_DISTANCE", f"P{index}", f"label={label}",
                      f"d2={dist2}"),
        ])
        rows.append((dist2, index, label))

    rows.sort(key=lambda item: (item[0], item[1]))
    neighbors = rows[:K]
    counts = {
        label: sum(1 for _, _, neighbor_label in neighbors
                   if neighbor_label == label)
        for label in LABELS
    }
    prediction = "A" if counts["A"] > counts["B"] else "B"
    relation = ">" if prediction == "A" else "<"
    steps.extend([
        make_step("KNN_SORT", neighbor_text(rows)),
        make_step("KNN_NEIGHBORS", neighbor_text(neighbors)),
        make_step("LABEL_COUNT", "A", counts["A"]),
        make_step("LABEL_COUNT", "B", counts["B"]),
        make_step("CHECK", "A vs B",
                  f"{counts['A']} {relation} {counts['B']}",
                  f"predict={prediction}"),
    ])
    neighbor_labels = ",".join(
        f"P{index}:{label}" for _, index, label in neighbors
    )
    answer = f"class={prediction}; neighbors={neighbor_labels}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestKNNGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = KNNGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "knn_classification")
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
