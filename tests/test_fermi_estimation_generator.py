import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.fermi_estimation_generator import FermiEstimationGenerator, sig2
from helpers import DELIM


def oracle_answer(example):
    """A9 oracle: recompute the rounded estimate from prompt factors."""
    problem = example["problem"]
    m = re.search(
        r"town with (\d+) people using about (\d+) gallons",
        problem,
    )
    if m:
        people, gallons = (int(v) for v in m.groups())
        return f"{sig2(people * gallons)} gallons/day"
    m = re.search(
        r"stadium with (\d+) sections, (\d+) rows per section, and "
        r"(\d+) seats per row",
        problem,
    )
    if m:
        sections, rows, seats = (int(v) for v in m.groups())
        return f"{sig2(sections * rows * seats)} seats"
    m = re.search(
        r"school with (\d+) students eating (\d+) slices per week for "
        r"(\d+) weeks",
        problem,
    )
    students, slices, weeks = (int(v) for v in m.groups())
    return f"{sig2(students * slices * weeks)} slices/year"


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        code = parts[0]
        if code == "M":
            if int(parts[1]) * int(parts[2]) != int(parts[3]):
                return False
        elif code == "SIGFIG_ROUND":
            if sig2(int(parts[1])) != parts[3]:
                return False
        elif code == "ESTIMATE_CHECK":
            if sig2(int(parts[2])) != parts[1]:
                return False
    return True


class TestFermiEstimationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FermiEstimationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_rounding_shape(self):
        for _ in range(200):
            answer = self.gen.generate()["final_answer"]
            self.assertRegex(answer, r"^\d(?:\.\d)? × 10\^\d+ .+")

    def test_estimate_check_present(self):
        for variant in FermiEstimationGenerator.VARIANTS:
            result = FermiEstimationGenerator(variant).generate()
            self.assertTrue(any(s.startswith(f"ESTIMATE_CHECK{DELIM}")
                                for s in result["steps"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            FermiEstimationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
