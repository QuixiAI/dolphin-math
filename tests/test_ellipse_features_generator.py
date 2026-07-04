import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.ellipse_features_generator import EllipseFeaturesGenerator
from tests.test_parabola_features_generator import parse_shift
from helpers import DELIM


def oracle_answer(example):
    """Recomputes center/vertices/foci from the equation alone."""
    m = re.fullmatch(
        r"Find the center, vertices, and foci of the ellipse "
        r"(.+)\^2/(\d+) \+ (.+)\^2/(\d+) = 1\.", example["problem"])
    assert m, example["problem"]
    h = parse_shift(m.group(1), "x")
    k = parse_shift(m.group(3), "y")
    d1, d2 = int(m.group(2)), int(m.group(4))
    assert d1 != d2
    a2, b2 = max(d1, d2), min(d1, d2)
    a = math.isqrt(a2)
    assert a * a == a2
    c2 = a2 - b2
    c = math.isqrt(c2)
    horizontal = d1 > d2
    if c * c == c2:
        if horizontal:
            foci = [f"({h - c}, {k})", f"({h + c}, {k})"]
        else:
            foci = [f"({h}, {k - c})", f"({h}, {k + c})"]
    else:
        ct = f"√{c2}"
        if horizontal:
            foci = [f"({h} - {ct}, {k})", f"({h} + {ct}, {k})"]
        else:
            foci = [f"({h}, {k} - {ct})", f"({h}, {k} + {ct})"]
    if horizontal:
        verts = [(h - a, k), (h + a, k)]
    else:
        verts = [(h, k - a), (h, k + a)]
    return (f"center ({h}, {k}); vertices ({verts[0][0]}, {verts[0][1]}) "
            f"and ({verts[1][0]}, {verts[1][1]}); "
            f"foci {foci[0]} and {foci[1]}")


class TestEllipseFeaturesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = EllipseFeaturesGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute all features from the equation."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_c_squared_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            evals = {s.split(DELIM)[1]: s.split(DELIM)[2]
                     for s in result["steps"]
                     if s.startswith(f"EVAL{DELIM}")}
            a, b = int(evals["a"]), int(evals["b"])
            self.assertGreater(a, b)
            self.assertEqual(int(evals["c^2"]), a * a - b * b)
            c_txt = evals["c"]
            if c_txt.startswith("√"):
                c2 = int(c_txt[1:])
                self.assertEqual(c2, a * a - b * b)
                r = math.isqrt(c2)
                self.assertNotEqual(r * r, c2, c_txt)
            else:
                self.assertEqual(int(c_txt) ** 2, a * a - b * b)

    def test_integer_and_radical_foci_occur(self):
        kinds = set()
        for _ in range(200):
            kinds.add("√" in self.gen.generate()["final_answer"])
        self.assertEqual(kinds, {True, False})

    def test_two_vertices_and_two_foci(self):
        for _ in range(200):
            result = self.gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertEqual(ops.count("VERTEX"), 2)
            self.assertEqual(ops.count("FOCUS"), 2)
            self.assertEqual(ops.count("CENTER"), 1)


if __name__ == "__main__":
    unittest.main()
