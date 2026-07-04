import ast
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.matrix_inverse_generator import MatrixInverseGenerator
from helpers import DELIM


def parse_frac_mat(txt):
    rows = re.findall(r"\[([^\[\]]+)\]", txt)
    return [[Fraction(v) for v in row.split(", ")] for row in rows]


def oracle_check(example):
    """A·A⁻¹ must equal the identity, exactly."""
    m = re.search(r"A = (\[\[.+?\]\]),", example["problem"])
    A = ast.literal_eval(m.group(1))
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    if det == 0:
        return example["final_answer"] == "No inverse (det = 0)"
    inv = parse_frac_mat(example["final_answer"])
    prod = [[sum(Fraction(A[i][t]) * inv[t][j] for t in range(2))
             for j in range(2)] for i in range(2)]
    return prod == [[1, 0], [0, 1]]


class TestMatrixInverseGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = MatrixInverseGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_product_is_identity(self):
        """A9 oracle: A times the claimed inverse is exactly I."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_singular_detected(self):
        gen = MatrixInverseGenerator("singular")
        for _ in range(100):
            result = gen.generate()
            self.assertEqual(result["final_answer"],
                             "No inverse (det = 0)")
            self.assertTrue(any("not invertible" in s
                                for s in result["steps"]))

    def test_unimodular_gives_integer_inverse(self):
        gen = MatrixInverseGenerator("unimodular")
        for _ in range(100):
            result = gen.generate()
            self.assertNotIn("/", result["final_answer"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "D":
                    self.assertEqual(Fraction(int(f[1]), int(f[2])),
                                     Fraction(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            MatrixInverseGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
