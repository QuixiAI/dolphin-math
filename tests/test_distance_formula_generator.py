import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.distance_formula_generator import DistanceFormulaGenerator
from generators.geometric_mean_generator import sqrt_txt
from helpers import DELIM


def oracle_answer(example):
    m = re.fullmatch(r"Find the distance between \((-?\d+), (-?\d+)\) "
                     r"and \((-?\d+), (-?\d+)\)\.", example["problem"])
    assert m, example["problem"]
    x1, y1, x2, y2 = (int(v) for v in m.groups())
    return f"d = {sqrt_txt((x2 - x1) ** 2 + (y2 - y1) ** 2)}"


class TestDistanceFormulaGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DistanceFormulaGenerator()

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
                if f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1].strip("()")) ** int(f[2]),
                                     int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)

    def test_radicals_simplified_and_integers_occur(self):
        kinds = set()
        for _ in range(300):
            result = self.gen.generate()
            a = result["final_answer"]
            kinds.add("√" in a)
            m = re.search(r"√(\d+)", a)
            if m:
                inside = int(m.group(1))
                for f in range(2, int(math.isqrt(inside)) + 1):
                    self.assertNotEqual(inside % (f * f), 0, a)
        self.assertEqual(kinds, {True, False})


if __name__ == "__main__":
    unittest.main()
