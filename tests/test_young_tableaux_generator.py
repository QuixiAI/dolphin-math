import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.young_tableaux_generator import YoungTableauxGenerator
from helpers import DELIM


HOOK_RE = re.compile(
    r"Use the hook-length formula to find the S_(\d+) representation "
    r"dimension for partition (\[[\d,]+\])\."
)
SU3_RE = re.compile(
    r"Use SU\(3\) Young-tableau rules to decompose "
    r"(\w+) x (\w+) and check dimensions\."
)
SU3_DECOMPS = {
    ("3", "3bar"): ([("8", 8), ("1", 1)],
                     "box plus antibox gives adjoint plus singlet"),
    ("3", "3"): ([("6", 6), ("3bar", 3)],
                   "two boxes split into symmetric plus antisymmetric"),
    ("3bar", "3bar"): ([("6bar", 6), ("3", 3)],
                         "two antiboxes split into symmetric plus antisymmetric"),
    ("8", "3"): ([("15", 15), ("6bar", 6), ("3", 3)],
                   "attach one box to the adjoint tableau"),
    ("8", "3bar"): ([("15bar", 15), ("6", 6), ("3bar", 3)],
                      "attach one antibox to the adjoint tableau"),
}
REP_DIMS = {
    "1": 1,
    "3": 3,
    "3bar": 3,
    "6": 6,
    "6bar": 6,
    "8": 8,
    "15": 15,
    "15bar": 15,
}


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def partition_text(partition):
    return "[" + ",".join(str(value) for value in partition) + "]"


def parse_partition(text):
    return [int(value) for value in text.strip("[]").split(",")]


def hook_length(partition, row, col):
    right = partition[row - 1] - col
    below = sum(1 for size in partition[row:] if size >= col)
    return right, below, right + below + 1


def component_text(components):
    return " + ".join(label for label, _ in components)


def parse_problem(problem):
    match = HOOK_RE.fullmatch(problem)
    if match:
        n = int(match.group(1))
        partition = parse_partition(match.group(2))
        return {"variant": "hook_length", "n": n, "partition": partition}
    match = SU3_RE.fullmatch(problem)
    assert match is not None, problem
    return {"variant": "su3_decomposition", "left": match.group(1),
            "right": match.group(2)}


def expected_hook(n, partition):
    hooks = []
    steps = [
        make_step("YOUNG_SETUP", f"partition={partition_text(partition)}",
                  f"n={n}", f"group=S_{n}"),
    ]
    for row, row_len in enumerate(partition, start=1):
        for col in range(1, row_len + 1):
            right, below, hook = hook_length(partition, row, col)
            hooks.append(hook)
            steps.append(make_step("HOOK", f"({row},{col})",
                                   f"right={right}", f"below={below}",
                                   f"hook={hook}"))
    hook_product = 1
    for hook in hooks:
        new_product = hook_product * hook
        steps.append(make_step("M", hook_product, hook, new_product))
        hook_product = new_product
    factorial = math.factorial(n)
    dimension = factorial // hook_product
    steps.extend([
        make_step("FACT", n, factorial),
        make_step("D", factorial, hook_product, dimension),
        make_step("CHECK", "n! divisible by hook product", "yes",
                  "integer dimension"),
    ])
    answer = f"dim S_{n}{partition_text(partition)} = {dimension}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_su3(left, right):
    components, rule = SU3_DECOMPS[(left, right)]
    product_dim = REP_DIMS[left] * REP_DIMS[right]
    steps = [
        make_step("SU3_SETUP", f"left={left}", f"right={right}"),
        make_step("TABLEAU_RULE", f"{left} x {right}", rule,
                  component_text(components)),
        make_step("M", REP_DIMS[left], REP_DIMS[right], product_dim),
    ]
    running = 0
    for label, dim in components:
        steps.append(make_step("REP_DIM", label, dim))
        new_running = running + dim
        steps.append(make_step("A", running, dim, new_running))
        running = new_running
    steps.append(make_step("CHECK", "dimension balance",
                           f"{product_dim}={running}", "ok"))
    answer = f"{left} x {right} = {component_text(components)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "hook_length":
        return expected_hook(parts["n"], parts["partition"])
    return expected_su3(parts["left"], parts["right"])


class TestYoungTableauxGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = YoungTableauxGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in YoungTableauxGenerator.VARIANTS:
            result = YoungTableauxGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"young_tableaux_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            YoungTableauxGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
