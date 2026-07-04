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

from generators.stars_and_bars_generator import StarsAndBarsGenerator
from helpers import DELIM


def oracle_parts(example):
    problem = example["problem"]
    match = re.fullmatch(
        r"How many nonnegative integer solutions are there to "
        r"x1 \+ \.\.\. \+ x(\d+) = (\d+)\?",
        problem,
    )
    if match:
        k, n = map(int, match.groups())
        value = math.comb(n + k - 1, k - 1)
        return {
            "variant": "nonnegative",
            "k": k,
            "n": n,
            "top": n + k - 1,
            "bottom": k - 1,
            "answer": f"solutions = {value}",
        }
    match = re.fullmatch(
        r"How many positive integer solutions are there to "
        r"x1 \+ \.\.\. \+ x(\d+) = (\d+)\?",
        problem,
    )
    if match:
        k, n = map(int, match.groups())
        value = math.comb(n - 1, k - 1)
        return {
            "variant": "positive",
            "k": k,
            "n": n,
            "remaining": n - k,
            "top": n - 1,
            "bottom": k - 1,
            "answer": f"solutions = {value}",
        }
    match = re.fullmatch(
        r"How many distinct strings can be made from (.+)\?",
        problem,
    )
    assert match is not None, problem
    counts = [int(value) for value in re.findall(r"(\d+) [A-D](?:'s)?",
                                                  match.group(1))]
    total = sum(counts)
    denom = 1
    for count in counts:
        denom *= math.factorial(count)
    value = math.factorial(total) // denom
    return {
        "variant": "multinomial",
        "counts": counts,
        "total": total,
        "denom": denom,
        "answer": f"multinomial = {value}",
    }


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "SB_SETUP":
            bound = "xi >= 0" if parts["variant"] == "nonnegative" else "xi >= 1"
            if fields[1:] != [f"x1+...+x{parts['k']} = {parts['n']}",
                              bound]:
                return False
        elif op == "SHIFT":
            if fields[1:] != ["yi = xi - 1",
                              f"y1+...+y{parts['k']} = {parts['remaining']}"]:
                return False
        elif op == "COMB_SETUP":
            if fields[1] != f"C({parts['top']}, {parts['bottom']})":
                return False
        elif op == "A":
            if int(fields[1]) + int(fields[2]) != int(fields[3]):
                return False
        elif op == "S":
            if int(fields[1]) - int(fields[2]) != int(fields[3]):
                return False
        elif op == "M":
            if int(fields[1]) * int(fields[2]) != int(fields[3]):
                return False
        elif op == "D":
            if Fraction(int(fields[1]), int(fields[2])) != int(fields[3]):
                return False
        elif op == "FACT_VALUE":
            label = fields[1]
            n = int(label.rstrip("!"))
            if int(fields[2]) != math.factorial(n):
                return False
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    return True


class TestStarsAndBarsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = StarsAndBarsGenerator()

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
        for variant in ("nonnegative", "positive", "multinomial"):
            gen = StarsAndBarsGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"stars_and_bars_{variant}")
                self.assertEqual(oracle_parts(result)["variant"], variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            StarsAndBarsGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
