import ast
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.determinant_generator import DeterminantGenerator
from helpers import DELIM


def det(m):
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    total = 0
    for j in range(3):
        cols = [c for c in range(3) if c != j]
        minor = [[m[1][cols[0]], m[1][cols[1]]],
                 [m[2][cols[0]], m[2][cols[1]]]]
        total += (-1) ** j * m[0][j] * det(minor)
    return total


def oracle_answer(example):
    m = re.search(r"A = (\[\[.+\]\])", example["problem"])
    A = ast.literal_eval(m.group(1))
    return str(det(A))


class TestDeterminantGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DeterminantGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: independent recursive determinant."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_three_by_three_has_three_cofactors(self):
        gen = DeterminantGenerator("three")
        for _ in range(100):
            result = gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertEqual(ops.count("COFACTOR"), 3)
            signs = [s.split(DELIM)[1][-1] for s in result["steps"]
                     if s.startswith(f"COFACTOR{DELIM}")]
            self.assertEqual(signs, ["+", "-", "+"])

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "A" and len(f) == 4:
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)

    def test_both_sizes_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"determinant_two", "determinant_three"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            DeterminantGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
