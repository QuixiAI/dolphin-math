import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.vector_ops_generator import VectorOpsGenerator
from generators.geometric_mean_generator import sqrt_txt
from helpers import DELIM


def parse_vec(txt):
    return [Fraction(v) for v in txt.strip("⟨⟩").split(", ")]


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"Given u = (⟨.+?⟩) and v = (⟨.+?⟩), compute "
                     r"(\d)u ([+-]) (\d)v\.", p)
    if m:
        u, v = parse_vec(m.group(1)), parse_vec(m.group(2))
        a, b = int(m.group(3)), int(m.group(5))
        sign = 1 if m.group(4) == "+" else -1
        res = [a * u[i] + sign * b * v[i] for i in range(2)]
        return "⟨" + ", ".join(str(c) for c in res) + "⟩"
    m = re.fullmatch(r"Find the magnitude of v = (⟨.+?⟩)\. Give an "
                     r"exact answer\.", p)
    if m:
        comps = parse_vec(m.group(1))
        return sqrt_txt(int(sum(c * c for c in comps)))
    m = re.fullmatch(r"Find the unit vector in the direction of "
                     r"v = (⟨.+?⟩)\.", p)
    assert m, p
    comps = parse_vec(m.group(1))
    total = int(sum(c * c for c in comps))
    mag = math.isqrt(total)
    assert mag * mag == total
    return "⟨" + ", ".join(str(Fraction(int(c), mag)) for c in comps) + "⟩"


class TestVectorOpsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = VectorOpsGenerator()

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

    def test_unit_vectors_have_magnitude_one(self):
        gen = VectorOpsGenerator("unit_vector")
        for _ in range(200):
            result = gen.generate()
            comps = parse_vec(result["final_answer"])
            self.assertEqual(sum(c * c for c in comps), 1)

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] in ("M", "A", "S", "D") and len(f) == 4:
                    x, y, z = (Fraction(v.strip("()")) for v in f[1:])
                    got = {"M": lambda: x * y, "A": lambda: x + y,
                           "S": lambda: x - y, "D": lambda: x / y}[f[0]]()
                    self.assertEqual(got, z, s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1].strip("()")) ** int(f[2]),
                                     int(f[3]), s)

    def test_3d_magnitudes_occur(self):
        gen = VectorOpsGenerator("magnitude")
        found = False
        for _ in range(100):
            result = gen.generate()
            if result["problem"].count(",") == 2:
                found = True
        self.assertTrue(found)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            VectorOpsGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
