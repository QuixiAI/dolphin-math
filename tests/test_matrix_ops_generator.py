import ast
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.matrix_ops_generator import MatrixOpsGenerator, mat
from helpers import DELIM


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"Given A = (\[.+?\]\]) and B = (\[.+?\]\]), "
                     r"compute A ([+-]) B\.", p)
    if m:
        A, B = ast.literal_eval(m.group(1)), ast.literal_eval(m.group(2))
        s = 1 if m.group(3) == "+" else -1
        return mat([[A[i][j] + s * B[i][j] for j in range(2)]
                    for i in range(2)])
    m = re.fullmatch(r"Given A = (\[.+?\]\]), compute (-?\d+)A\.", p)
    if m:
        A, k = ast.literal_eval(m.group(1)), int(m.group(2))
        return mat([[k * v for v in row] for row in A])
    m = re.fullmatch(r"Given A = (\[.+?\]\]) and [vB] = (\[.+?\]\]), "
                     r"compute A[vB]?B?\. Show the row-by-column "
                     r"work\.", p)
    assert m, p
    A, B = ast.literal_eval(m.group(1)), ast.literal_eval(m.group(2))
    cols = len(B[0])
    return mat([[sum(A[i][t] * B[t][j] for t in range(2))
                 for j in range(cols)] for i in range(2)])


class TestMatrixOpsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = MatrixOpsGenerator()

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

    def test_multiplication_shows_row_column_work(self):
        gen = MatrixOpsGenerator("multiply")
        for _ in range(100):
            result = gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertEqual(ops.count("M"), 8)
            self.assertEqual(ops.count("A"), 4)
            self.assertEqual(ops.count("MAT_ENTRY"), 4)

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A" and len(f) == 4:
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            MatrixOpsGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
