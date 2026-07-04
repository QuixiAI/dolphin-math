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

from generators.hyperbola_features_generator import (
    HyperbolaFeaturesGenerator,
    slope_txt,
)
from generators.parabola_features_generator import shift
from tests.test_parabola_features_generator import parse_shift
from helpers import DELIM


def oracle_answer(example):
    """Recomputes all hyperbola features from the equation alone."""
    m = re.fullmatch(
        r"Find the center, vertices, foci, and asymptotes of the "
        r"hyperbola (.+)\^2/(\d+) - (.+)\^2/(\d+) = 1\.",
        example["problem"])
    assert m, example["problem"]
    first, a2, second, b2 = (m.group(1), int(m.group(2)),
                             m.group(3), int(m.group(4)))
    horizontal = first.lstrip("(").startswith("x")
    if horizontal:
        h = parse_shift(first, "x")
        k = parse_shift(second, "y")
    else:
        k = parse_shift(first, "y")
        h = parse_shift(second, "x")
    a = math.isqrt(a2)
    b = math.isqrt(b2)
    assert a * a == a2 and b * b == b2
    c2 = a2 + b2
    c = math.isqrt(c2)
    c_txt = str(c) if c * c == c2 else f"√{c2}"
    slope = Fraction(b, a) if horizontal else Fraction(a, b)

    if horizontal:
        verts = [(h - a, k), (h + a, k)]
        if c * c == c2:
            foci = [f"({h - c}, {k})", f"({h + c}, {k})"]
        else:
            foci = [f"({h} - {c_txt}, {k})", f"({h} + {c_txt}, {k})"]
    else:
        verts = [(h, k - a), (h, k + a)]
        if c * c == c2:
            foci = [f"({h}, {k - c})", f"({h}, {k + c})"]
        else:
            foci = [f"({h}, {k} - {c_txt})", f"({h}, {k} + {c_txt})"]

    st = slope_txt(slope)
    x_part = f"{st}{shift('x', h)}" if h else f"{st}x"
    asym = f"y = ±{x_part}" if k == 0 else f"y = {k} ± {x_part}"
    return (f"center ({h}, {k}); vertices ({verts[0][0]}, {verts[0][1]}) "
            f"and ({verts[1][0]}, {verts[1][1]}); "
            f"foci {foci[0]} and {foci[1]}; asymptotes {asym}")


class TestHyperbolaFeaturesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = HyperbolaFeaturesGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute everything from the equation."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_c_squared_uses_plus(self):
        """The hyperbola relation c^2 = a^2 + b^2, not minus."""
        for _ in range(300):
            result = self.gen.generate()
            evals = {s.split(DELIM)[1]: s.split(DELIM)[2]
                     for s in result["steps"]
                     if s.startswith(f"EVAL{DELIM}")}
            a, b = int(evals["a"]), int(evals["b"])
            self.assertEqual(int(evals["c^2"]), a * a + b * b)

    def test_asymptote_slope_reduced(self):
        for _ in range(300):
            result = self.gen.generate()
            m = re.search(r"± \((\d+)/(\d+)\)", result["final_answer"])
            if m:
                n, d = int(m.group(1)), int(m.group(2))
                self.assertEqual(math.gcd(n, d), 1, result["final_answer"])

    def test_counts(self):
        for _ in range(200):
            result = self.gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertEqual(ops.count("VERTEX"), 2)
            self.assertEqual(ops.count("FOCUS"), 2)
            self.assertEqual(ops.count("ASYMPTOTE"), 1)

    def test_both_orientations_and_radical_foci_occur(self):
        kinds = set()
        for _ in range(200):
            result = self.gen.generate()
            eq = result["problem"].split("hyperbola ")[1]
            kinds.add(("y" if eq.lstrip("(").startswith("y") else "x",
                       "√" in result["final_answer"]))
        self.assertEqual(len(kinds), 4, kinds)


if __name__ == "__main__":
    unittest.main()
