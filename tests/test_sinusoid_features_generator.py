import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.sinusoid_features_generator import (
    SinusoidFeaturesGenerator,
)
from generators.arc_sector_generator import pi_txt
from helpers import DELIM


def oracle_answer(example):
    m = re.fullmatch(r"State the amplitude, period, phase shift, and "
                     r"midline of (.+)\.", example["problem"])
    eq = m.group(1)
    mm = re.fullmatch(
        r"y = (-?\d*)(?:sin|cos)\((\d+)\(x ([+-]) ([^)]+)\)\)"
        r"(?: ([+-]) (\d+))?", eq)
    if mm:  # factored (degree or radian)
        A = int(mm.group(1) + "1") if mm.group(1) in ("", "-") \
            else int(mm.group(1))
        B = int(mm.group(2))
        direction = "right" if mm.group(3) == "-" else "left"
        C = mm.group(4)
        D = int(mm.group(6) or 0) * (1 if (mm.group(5) or "+") == "+"
                                     else -1)
        if "π" in C:
            period = pi_txt(Fraction(2, B))
        else:
            period = f"{360 // B}°"
        return (f"amplitude {abs(A)}; period {period}; phase shift "
                f"{C} {direction}; midline y = {D}")
    mm = re.fullmatch(
        r"y = (-?\d*)(?:sin|cos)\((\d+)x ([+-]) (\d+)°\)"
        r"(?: ([+-]) (\d+))?", eq)
    assert mm, eq
    A = int(mm.group(1) + "1") if mm.group(1) in ("", "-") \
        else int(mm.group(1))
    B = int(mm.group(2))
    direction = "right" if mm.group(3) == "-" else "left"
    phi = int(mm.group(4))
    D = int(mm.group(6) or 0) * (1 if (mm.group(5) or "+") == "+"
                                 else -1)
    assert phi % B == 0
    return (f"amplitude {abs(A)}; period {360 // B}°; phase shift "
            f"{phi // B}° {direction}; midline y = {D}")


class TestSinusoidFeaturesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SinusoidFeaturesGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_unfactored_shows_factoring(self):
        gen = SinusoidFeaturesGenerator("unfactored")
        for _ in range(200):
            result = gen.generate()
            self.assertTrue(any(s.startswith(f"REWRITE{DELIM}")
                                for s in result["steps"]),
                            result["steps"])

    def test_amplitude_never_negative(self):
        for _ in range(300):
            result = self.gen.generate()
            m = re.search(r"amplitude (-?\d+)", result["final_answer"])
            self.assertGreater(int(m.group(1)), 0)

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "D" and f[1].isdigit():
                    self.assertEqual(int(f[1]), int(f[2]) * int(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            SinusoidFeaturesGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
