import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.set_operations_generator import SetOperationsGenerator
from helpers import DELIM


LETTERS = ["a", "b", "c", "d", "e", "f"]
DIGITS = ["1", "2", "3", "4"]


def fmt_set(values):
    return "{" + ", ".join(values) + "}" if values else "{}"


def ordered(values, universe):
    return [value for value in universe if value in values]


def parse_set(text):
    if text == "{}":
        return []
    assert text.startswith("{") and text.endswith("}"), text
    return [item.strip() for item in text[1:-1].split(",")]


def subsets(values):
    out = [[]]
    for value in values:
        out += [subset + [value] for subset in out]
    return sorted(out, key=lambda subset: (len(subset), [values.index(v) for v in subset]))


def fmt_power_set(values):
    return "{" + ", ".join(fmt_set(subset) for subset in subsets(values)) + "}"


def fmt_pairs(A, B):
    pairs = [f"({a}, {b})" for a in A for b in B]
    return "{" + ", ".join(pairs) + "}" if pairs else "{}"


def oracle_parts(example):
    problem = example["problem"]
    match = re.fullmatch(
        r"Given A = (\{.*\}) and B = (\{.*\}), find A "
        r"(union|intersect|minus) B\.",
        problem,
    )
    if match:
        A = parse_set(match.group(1))
        B = parse_set(match.group(2))
        op = match.group(3)
        if op == "union":
            result = ordered(set(A) | set(B), LETTERS)
        elif op == "intersect":
            result = ordered(set(A) & set(B), LETTERS)
        else:
            result = ordered(set(A) - set(B), LETTERS)
        return {
            "variant": "algebra",
            "A": A,
            "B": B,
            "op": op,
            "result": result,
            "answer": fmt_set(result),
        }

    match = re.fullmatch(r"Find the power set P\(S\) for S = (\{.*\})\.",
                         problem)
    if match:
        S = parse_set(match.group(1))
        return {
            "variant": "power_set",
            "S": S,
            "answer": f"P(S) = {fmt_power_set(S)}",
        }

    match = re.fullmatch(
        r"Find A x B for A = (\{.*\}) and B = (\{.*\})\.",
        problem,
    )
    assert match is not None, problem
    A = parse_set(match.group(1))
    B = parse_set(match.group(2))
    return {
        "variant": "cartesian_product",
        "A": A,
        "B": B,
        "answer": f"A x B = {fmt_pairs(A, B)}",
    }


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    pair_count = 0
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "SET_SETUP":
            if parts["variant"] == "algebra":
                expected = [f"A = {fmt_set(parts['A'])}",
                            f"B = {fmt_set(parts['B'])}", parts["op"]]
            elif parts["variant"] == "power_set":
                expected = [f"S = {fmt_set(parts['S'])}", "power set"]
            else:
                expected = [f"A = {fmt_set(parts['A'])}",
                            f"B = {fmt_set(parts['B'])}",
                            "cartesian product"]
            if fields[1:] != expected:
                return False
        elif op == "ELEMENT_SCAN":
            element = fields[1]
            in_a = element in parts["A"]
            in_b = element in parts["B"]
            keep = element in parts["result"]
            expected = [element, f"in A={in_a}, in B={in_b}",
                        "keep" if keep else "skip"]
            if fields[1:] != expected:
                return False
        elif op == "COUNT":
            if fields[1:] != ["result size", str(len(parts["result"]))]:
                return False
        elif op == "E":
            if int(fields[1]) ** int(fields[2]) != int(fields[3]):
                return False
        elif op == "SUBSET_SIZE":
            size = int(fields[1])
            group = [fmt_set(subset) for subset in subsets(parts["S"])
                     if len(subset) == size]
            if fields[2] != ", ".join(group):
                return False
        elif op == "M":
            if int(fields[1]) * int(fields[2]) != int(fields[3]):
                return False
        elif op == "CART_PAIR":
            a, b = fields[1], fields[2]
            if fields[3] != f"({a}, {b})":
                return False
            pair_count += 1
        elif op == "POWER_SET_RESULT":
            if fields[1:] != [fmt_power_set(parts["S"])]:
                return False
        elif op == "CARTESIAN_RESULT":
            if fields[1:] != [fmt_pairs(parts["A"], parts["B"])]:
                return False
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    if parts["variant"] == "cartesian_product":
        return pair_count == len(parts["A"]) * len(parts["B"])
    return True


class TestSetOperationsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SetOperationsGenerator()

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
        for variant in ("algebra", "power_set", "cartesian_product"):
            gen = SetOperationsGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"set_operations_{variant}")
                self.assertEqual(oracle_parts(result)["variant"], variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SetOperationsGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
