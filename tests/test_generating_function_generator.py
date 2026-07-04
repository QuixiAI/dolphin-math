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

from generators.generating_function_generator import GeneratingFunctionGenerator
from helpers import DELIM


BINOMIAL_RE = re.compile(
    r"Find the coefficient of x\^(\d+) in "
    r"\(1 \+ x\)\^(\d+)\(1 \+ x\)\^(\d+)\."
)
GEOMETRIC_RE = re.compile(
    r"Find the coefficient of x\^(\d+) in "
    r"1/\(\(1 - x\^(\d+)\)\(1 - x\^(\d+)\)\)\."
)


def convolve(poly, factor, max_degree):
    result = [0] * (max_degree + 1)
    for i, left in enumerate(poly):
        if left == 0:
            continue
        for j, right in enumerate(factor):
            if right == 0 or i + j > max_degree:
                continue
            result[i + j] += left * right
    return result


def parse_problem(problem):
    match = BINOMIAL_RE.fullmatch(problem)
    if match:
        target, a, b = map(int, match.groups())
        return {"variant": "binomial_product", "target": target,
                "a": a, "b": b}
    match = GEOMETRIC_RE.fullmatch(problem)
    assert match is not None, problem
    target, a, b = map(int, match.groups())
    return {"variant": "geometric_product", "target": target,
            "a": a, "b": b}


def coefficient_from_polynomial(parts):
    target = parts["target"]
    poly = [1] + [0] * target
    if parts["variant"] == "binomial_product":
        factor = [1, 1]
        for _ in range(parts["a"]):
            poly = convolve(poly, factor, target)
        for _ in range(parts["b"]):
            poly = convolve(poly, factor, target)
        return poly[target]

    factor_a = [0] * (target + 1)
    factor_b = [0] * (target + 1)
    for exponent in range(0, target + 1, parts["a"]):
        factor_a[exponent] = 1
    for exponent in range(0, target + 1, parts["b"]):
        factor_b[exponent] = 1
    return convolve(factor_a, factor_b, target)[target]


def oracle_answer(example):
    return f"coefficient = {coefficient_from_polynomial(parse_problem(example['problem']))}"


def check_step_arithmetic(example):
    parts = parse_problem(example["problem"])
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "GF_SETUP":
            if fields[1] != f"[x^{parts['target']}]":
                return False
        elif op == "NCR":
            match = re.fullmatch(r"C\((\d+), (\d+)\)", fields[1])
            if match is None:
                return False
            n, r = map(int, match.groups())
            if math.comb(n, r) != int(fields[2]):
                return False
        elif op == "COEFF_PAIR":
            match = re.fullmatch(r"i=(\d+), j=(\d+)", fields[1])
            if match is None:
                return False
            i, j = map(int, match.groups())
            if parts["variant"] == "binomial_product":
                if i + j != parts["target"]:
                    return False
                expected = math.comb(parts["a"], i) * math.comb(parts["b"], j)
                if int(fields[3]) != expected:
                    return False
            else:
                if parts["a"] * i + parts["b"] * j != parts["target"]:
                    return False
                if fields[3] != "accepted":
                    return False
        elif op == "GF_DIV_CHECK":
            match = re.fullmatch(r"(\d+) / (\d+)", fields[1])
            if match is None:
                return False
            rem, divisor = map(int, match.groups())
            if rem % divisor == 0 or fields[2:] != ["not integer", "reject"]:
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
        elif op == "Z":
            if fields[1:] != [oracle_answer(example)]:
                return False
    return True


class TestGeneratingFunctionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GeneratingFunctionGenerator()

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
        for variant in ("binomial_product", "geometric_product"):
            gen = GeneratingFunctionGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"generating_function_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_geometric_variant_has_accepts_and_rejects(self):
        gen = GeneratingFunctionGenerator("geometric_product")
        saw_accept = False
        saw_reject = False
        for _ in range(100):
            result = gen.generate()
            saw_accept |= any("accepted" in raw for raw in result["steps"])
            saw_reject |= any("reject" in raw for raw in result["steps"])
        self.assertTrue(saw_accept)
        self.assertTrue(saw_reject)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GeneratingFunctionGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
