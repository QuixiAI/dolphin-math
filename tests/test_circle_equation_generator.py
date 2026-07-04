import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.circle_equation_generator import CircleEquationGenerator
from generators.parabola_features_generator import shift
from helpers import DELIM


def eq_of(h, k, r2):
    return f"{shift('x', h)}^2 + {shift('y', k)}^2 = {r2}"


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"Write the equation of the circle with center "
                     r"\((-?\d+), (-?\d+)\) and radius (\d+)\.", p)
    if m:
        h, k, r = (int(v) for v in m.groups())
        return eq_of(h, k, r * r)
    m = re.fullmatch(r"Write the equation of the circle with center "
                     r"\((-?\d+), (-?\d+)\) that passes through "
                     r"\((-?\d+), (-?\d+)\)\.", p)
    if m:
        h, k, px, py = (int(v) for v in m.groups())
        return eq_of(h, k, (px - h) ** 2 + (py - k) ** 2)
    m = re.fullmatch(r"Write the equation of the circle whose diameter "
                     r"has endpoints \((-?\d+), (-?\d+)\) and "
                     r"\((-?\d+), (-?\d+)\)\.", p)
    assert m, p
    x1, y1, x2, y2 = (int(v) for v in m.groups())
    h, k = (x1 + x2) // 2, (y1 + y2) // 2
    return eq_of(h, k, (x2 - h) ** 2 + (y2 - k) ** 2)


class TestCircleEquationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CircleEquationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1].strip("()")) ** int(f[2]),
                                     int(f[3]), s)
                elif f[0] == "D":
                    self.assertEqual(int(f[1]), int(f[2]) * int(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)


if __name__ == "__main__":
    unittest.main()
