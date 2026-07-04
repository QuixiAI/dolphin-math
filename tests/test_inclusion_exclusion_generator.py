import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.inclusion_exclusion_generator import InclusionExclusionGenerator
from helpers import DELIM


def oracle_parts(example):
    problem = example["problem"]
    match = re.fullmatch(
        r"In a survey, n\(A\) = (\d+), n\(B\) = (\d+), and "
        r"n\(A intersect B\) = (\d+)\. How many are in A union B\?",
        problem,
    )
    if match:
        A, B, AB = map(int, match.groups())
        union = A + B - AB
        return {
            "variant": "two_sets",
            "A": A,
            "B": B,
            "AB": AB,
            "union": union,
            "answer": f"n(A union B) = {union}",
        }
    match = re.fullmatch(
        r"In a survey, n\(A\) = (\d+), n\(B\) = (\d+), n\(C\) = "
        r"(\d+), n\(A intersect B\) = (\d+), n\(A intersect C\) = "
        r"(\d+), n\(B intersect C\) = (\d+), and n\(A intersect B "
        r"intersect C\) = (\d+)\. How many are in A union B union C\?",
        problem,
    )
    assert match is not None, problem
    A, B, C, AB, AC, BC, ABC = map(int, match.groups())
    union = A + B + C - AB - AC - BC + ABC
    return {
        "variant": "three_sets",
        "A": A,
        "B": B,
        "C": C,
        "AB": AB,
        "AC": AC,
        "BC": BC,
        "ABC": ABC,
        "union": union,
        "answer": f"n(A union B union C) = {union}",
    }


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "IE_SETUP":
            if parts["variant"] == "two_sets":
                expected = [
                    f"n(A)={parts['A']}, n(B)={parts['B']}",
                    f"n(A intersect B)={parts['AB']}",
                ]
            else:
                expected = [
                    f"n(A)={parts['A']}, n(B)={parts['B']}, "
                    f"n(C)={parts['C']}",
                    f"n(AB)={parts['AB']}, n(AC)={parts['AC']}, "
                    f"n(BC)={parts['BC']}, n(ABC)={parts['ABC']}",
                ]
            if fields[1:] != expected:
                return False
        elif op == "A":
            if int(fields[1]) + int(fields[2]) != int(fields[3]):
                return False
        elif op == "S":
            if int(fields[1]) - int(fields[2]) != int(fields[3]):
                return False
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    return True


class TestInclusionExclusionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = InclusionExclusionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_variants_are_available(self):
        for variant in ("two_sets", "three_sets"):
            gen = InclusionExclusionGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"inclusion_exclusion_{variant}")
                self.assertEqual(oracle_parts(result)["variant"], variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            InclusionExclusionGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
