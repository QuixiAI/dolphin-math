import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.similar_triangles_generator import SimilarTrianglesGenerator
from helpers import DELIM


def oracle_answer(example):
    """Re-solves the proportion from the problem text alone."""
    p = example["problem"]
    m = re.fullmatch(r"Triangle ABC is similar to triangle DEF, with "
                     r"DE = (\d+), AB = (\d+), EF = (\d+)\. Find BC\.", p)
    if m:
        A, a, B = (int(v) for v in m.groups())
        v = Fraction(a * B, A)
        assert v.denominator == 1
        return f"BC = {v.numerator}"
    m = re.fullmatch(r"Triangle ABC is similar to triangle DEF, with "
                     r"AB = (\d+), DE = (\d+), BC = (\d+)\. Find EF\.", p)
    assert m, p
    a, A, b = (int(v) for v in m.groups())
    v = Fraction(A * b, a)
    assert v.denominator == 1
    return f"EF = {v.numerator}"


class TestSimilarTrianglesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SimilarTrianglesGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: re-solve the proportion."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "D":
                    self.assertEqual(int(f[1]), int(f[2]) * int(f[3]), s)

    def test_scale_check_is_consistent(self):
        for _ in range(300):
            result = self.gen.generate()
            chk = next(s for s in result["steps"]
                       if s.startswith(f"CHECK{DELIM}"))
            f = chk.split(DELIM)
            k = Fraction(f[3])
            for part in f[2].split(", "):
                ratio = part.split(" = ")[0]
                num, den = ratio.split("/")
                self.assertEqual(Fraction(int(num), int(den)), k, chk)

    def test_both_directions_occur(self):
        goals = set()
        for _ in range(100):
            goals.add(self.gen.generate()["final_answer"].split(" = ")[0])
        self.assertEqual(goals, {"BC", "EF"})


if __name__ == "__main__":
    unittest.main()
