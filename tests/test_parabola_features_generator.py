import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.parabola_features_generator import ParabolaFeaturesGenerator
from helpers import DELIM


def parse_shift(txt, var):
    """'(x - 3)' -> 3, '(y + 2)' -> -2, 'x' -> 0."""
    if txt == var:
        return 0
    m = re.fullmatch(rf"\({var} ([+-]) (\d+)\)", txt)
    assert m, txt
    return int(m.group(2)) * (-1 if m.group(1) == "+" else 1)


def oracle_answer(example):
    """Recomputes vertex/focus/directrix from the equation alone."""
    m = re.fullmatch(r"Find the vertex, focus, and directrix of "
                     r"(.+)\^2 = (-?\d+)(.+)\.", example["problem"])
    assert m, example["problem"]
    sq, C, other = m.group(1), int(m.group(2)), m.group(3)
    assert C % 4 == 0
    p = C // 4
    if sq.lstrip("(").startswith("x"):
        h = parse_shift(sq, "x")
        k = parse_shift(other if other != "y" else "y", "y")
        focus = (h, k + p)
        directrix = f"y = {k - p}"
    else:
        k = parse_shift(sq, "y")
        h = parse_shift(other if other != "x" else "x", "x")
        focus = (h + p, k)
        directrix = f"x = {h - p}"
    return (f"vertex ({h}, {k}); focus ({focus[0]}, {focus[1]}); "
            f"directrix {directrix}")


class TestParabolaFeaturesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ParabolaFeaturesGenerator()

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

    def test_focus_on_axis_and_directrix_opposite(self):
        """Focus and directrix are equidistant from the vertex."""
        for _ in range(300):
            result = self.gen.generate()
            m = re.fullmatch(r"vertex \((-?\d+), (-?\d+)\); focus "
                             r"\((-?\d+), (-?\d+)\); directrix "
                             r"([xy]) = (-?\d+)", result["final_answer"])
            h, k, fx, fy = (int(m.group(i)) for i in range(1, 5))
            axis, dval = m.group(5), int(m.group(6))
            if axis == "y":  # vertical parabola
                self.assertEqual(fx, h)
                self.assertEqual(fy - k, -(dval - k))
                self.assertNotEqual(fy, k)
            else:
                self.assertEqual(fy, k)
                self.assertEqual(fx - h, -(dval - h))

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "D":
                    self.assertEqual(int(f[1]), int(f[2]) * int(f[3]), s)

    def test_orientation_identified(self):
        for _ in range(200):
            result = self.gen.generate()
            fi = next(s for s in result["steps"]
                      if s.startswith(f"FORM_IDENTIFY{DELIM}"))
            starts_x = result["problem"].split("of ")[1].lstrip("(") \
                .startswith("x")
            self.assertEqual("vertical" in fi, starts_x, fi)

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(200):
            result = self.gen.generate()
            eq = result["problem"].split("of ")[1]
            if "(" not in eq.split(" = ")[0] and \
                    "(" not in eq.split(" = ")[1]:
                kinds.add("origin")
            elif eq.lstrip("(").startswith("x"):
                kinds.add("vertical")
            else:
                kinds.add("horizontal")
        self.assertEqual(kinds, {"origin", "vertical", "horizontal"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ParabolaFeaturesGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
