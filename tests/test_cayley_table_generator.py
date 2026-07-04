import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.cayley_table_generator import CayleyTableGenerator
from helpers import DELIM


ZN_RE = re.compile(
    r"Build the Cayley table for Z_(\d+) under addition modulo \d+ and "
    r"find the order of element (\d+)\."
)
UNITS_RE = re.compile(
    r"Build the Cayley table for U\((\d+)\) under multiplication modulo "
    r"\d+ and find the order of element (\d+)\."
)
D3_RE = re.compile(
    r"Build the Cayley table for D3 with elements e, r, r2, s, rs, r2s "
    r"and find the order of element (e|r|r2|s|rs|r2s)\."
)

D3_ELEMENTS = ["e", "r", "r2", "s", "rs", "r2s"]
D3_PAIRS = {
    "e": (0, 0),
    "r": (1, 0),
    "r2": (2, 0),
    "s": (0, 1),
    "rs": (1, 1),
    "r2s": (2, 1),
}
D3_NAMES = {value: key for key, value in D3_PAIRS.items()}


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def list_text(values):
    return ", ".join(str(value) for value in values)


def units(n):
    return [value for value in range(1, n) if gcd(value, n) == 1]


def d3_multiply(left, right):
    i, j = D3_PAIRS[left]
    k, ell = D3_PAIRS[right]
    return D3_NAMES[((i + (-1 if j else 1) * k) % 3, (j + ell) % 2)]


def parse_problem(problem):
    match = ZN_RE.fullmatch(problem)
    if match:
        n, target = map(int, match.groups())
        return {"variant": "zn", "n": n, "target": target}
    match = UNITS_RE.fullmatch(problem)
    if match:
        n, target = map(int, match.groups())
        return {"variant": "units", "n": n, "target": target}
    match = D3_RE.fullmatch(problem)
    assert match is not None, problem
    return {"variant": "d3", "target": match.group(1)}


def expected_zn(n, target):
    elements = list(range(n))
    steps = [
        make_step("GROUP_SETUP", f"Z_{n}", "addition mod n"),
        make_step("CAYLEY_HEADER", list_text(elements)),
    ]
    for row in elements:
        values = [(row + col) % n for col in elements]
        steps.append(make_step("CAYLEY_ROW", f"row {row}",
                               list_text(values)))
    current = 0
    steps.append(make_step("ORDER_START", target, "identity 0"))
    for k in range(1, n + 1):
        previous = current
        total = previous + target
        current = total % n
        steps.append(make_step("A", previous, target, total))
        steps.append(make_step("MOD_REDUCE", total, f"mod {n}", current))
        steps.append(make_step("ORDER_STEP", f"k={k}", current))
        if current == 0:
            order = k
            break
    steps.append(make_step("ELEMENT_ORDER", target, order))
    answer = f"order({target}) = {order}"
    return steps, answer


def expected_units(n, target):
    elements = units(n)
    steps = [
        make_step("GROUP_SETUP", f"U({n})", "multiplication mod n"),
        make_step("CAYLEY_HEADER", list_text(elements)),
    ]
    for row in elements:
        values = [(row * col) % n for col in elements]
        steps.append(make_step("CAYLEY_ROW", f"row {row}",
                               list_text(values)))
    current = 1
    steps.append(make_step("ORDER_START", target, "identity 1"))
    for k in range(1, len(elements) + 1):
        previous = current
        product = previous * target
        current = product % n
        steps.append(make_step("M", previous, target, product))
        steps.append(make_step("MOD_REDUCE", product, f"mod {n}", current))
        steps.append(make_step("ORDER_STEP", f"k={k}", current))
        if current == 1:
            order = k
            break
    steps.append(make_step("ELEMENT_ORDER", target, order))
    answer = f"order({target}) = {order}"
    return steps, answer


def expected_d3(target):
    steps = [
        make_step("GROUP_SETUP", "D3", "symmetries of a triangle"),
        make_step("CAYLEY_HEADER", list_text(D3_ELEMENTS)),
    ]
    for row in D3_ELEMENTS:
        values = [d3_multiply(row, col) for col in D3_ELEMENTS]
        steps.append(make_step("CAYLEY_ROW", f"row {row}",
                               list_text(values)))
    current = "e"
    steps.append(make_step("ORDER_START", target, "identity e"))
    for k in range(1, 7):
        current = d3_multiply(current, target)
        steps.append(make_step("ORDER_STEP", f"k={k}", current))
        if current == "e":
            order = k
            break
    steps.append(make_step("ELEMENT_ORDER", target, order))
    answer = f"order({target}) = {order}"
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "zn":
        steps, answer = expected_zn(parts["n"], parts["target"])
    elif parts["variant"] == "units":
        steps, answer = expected_units(parts["n"], parts["target"])
    else:
        steps, answer = expected_d3(parts["target"])
    steps.append(make_step("Z", answer))
    return steps, answer


class TestCayleyTableGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CayleyTableGenerator()

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
                elif fields[0] == "MOD_REDUCE":
                    mod = int(fields[2].split()[1])
                    self.assertEqual(int(fields[1]) % mod, int(fields[3]),
                                     raw_step)

    def test_variants_are_available(self):
        for variant in ("zn", "units", "d3"):
            gen = CayleyTableGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"cayley_table_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CayleyTableGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
