import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.conditional_probability_generator import (
    ConditionalProbabilityGenerator, exact,
)
from helpers import DELIM


TABLE_RE = re.compile(
    r"club=yes and commute=bike: (\d+); "
    r"club=no and commute=bike: (\d+); "
    r"club=yes and commute=bus: (\d+); "
    r"club=no and commute=bus: (\d+)"
)
BAYES_RE = re.compile(
    r"used for (\d+) people\. Disease=yes count is (\d+) and "
    r"disease=no count is (\d+)\. Sensitivity P\(test positive given "
    r"disease=yes\) = (\d+/\d+)\. Specificity P\(test negative given "
    r"disease=no\) = (\d+/\d+)\. Find P\(disease=(yes|no) given "
    r"test (positive|negative)\)"
)


def parse_table(problem):
    yes_bike, no_bike, yes_bus, no_bus = (
        int(v) for v in TABLE_RE.search(problem).groups()
    )
    return {
        ("yes", "bike"): yes_bike,
        ("no", "bike"): no_bike,
        ("yes", "bus"): yes_bus,
        ("no", "bus"): no_bus,
    }


def oracle_answer(example):
    """A9 oracle: recompute the answer from the problem text alone."""
    problem = example["problem"]
    if "two-way table" in problem:
        cells = parse_table(problem)
        target, given = re.search(
            r"Find P\((club=(?:yes|no)|commute=(?:bike|bus)) given "
            r"(club=(?:yes|no)|commute=(?:bike|bus))\)",
            problem,
        ).groups()
        target_var, target_val = target.split("=")
        given_var, given_val = given.split("=")

        numerator = 0
        denominator = 0
        for club_val in ("yes", "no"):
            for commute_val in ("bike", "bus"):
                count = cells[(club_val, commute_val)]
                row = {"club": club_val, "commute": commute_val}
                if row[given_var] == given_val:
                    denominator += count
                    if row[target_var] == target_val:
                        numerator += count
        return exact(Fraction(numerator, denominator))

    _, disease, no_disease, sensitivity, specificity, target, test = (
        BAYES_RE.search(problem).groups()
    )
    disease = int(disease)
    no_disease = int(no_disease)
    sensitivity = Fraction(sensitivity)
    specificity = Fraction(specificity)
    true_positive = disease * sensitivity
    false_negative = disease - true_positive
    true_negative = no_disease * specificity
    false_positive = no_disease - true_negative
    if target == "yes" and test == "positive":
        return exact(true_positive / (true_positive + false_positive))
    return exact(true_negative / (true_negative + false_negative))


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        code = parts[0]
        if code == "COND_TOTAL":
            a, b, total = (int(v) for v in re.search(
                r"(\d+) \+ (\d+) = (\d+)", parts[2]
            ).groups())
            if a + b != total:
                return False
        elif code == "BAYES_CELL":
            expr, result = parts[2], int(parts[3])
            if "*" in expr:
                left, right = expr.split(" * ")
                value = int(left) * Fraction(right)
            else:
                left, right = expr.split(" - ")
                value = int(left) - int(right)
            if value != result:
                return False
        elif code == "A":
            if Fraction(parts[1]) + Fraction(parts[2]) != Fraction(parts[3]):
                return False
        elif code == "FRAC_BUILD":
            if exact(Fraction(parts[1])) != parts[2]:
                return False
    return True


class TestConditionalProbabilityGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ConditionalProbabilityGenerator()

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

    def test_probabilities_valid(self):
        for _ in range(300):
            result = self.gen.generate()
            val = float(Fraction(result["final_answer"]))
            self.assertGreaterEqual(val, 0)
            self.assertLessEqual(val, 1)

    def test_formula_present(self):
        for variant in ConditionalProbabilityGenerator.VARIANTS:
            gen = ConditionalProbabilityGenerator(variant)
            result = gen.generate()
            formula_codes = {s.split(DELIM)[0] for s in result["steps"]}
            self.assertTrue({"COND_FORMULA", "BAYES_FORMULA"} & formula_codes)

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
            ConditionalProbabilityGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
