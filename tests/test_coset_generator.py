import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.coset_generator import CosetGenerator
from helpers import DELIM


ZN_RE = re.compile(
    r"In Z_(\d+) under addition modulo \d+, let H=<(\d+)>\. "
    r"Enumerate the distinct left cosets a\+H\."
)
UNITS_RE = re.compile(
    r"In U\((\d+)\) under multiplication modulo \d+, let H=<(\d+)>\. "
    r"Enumerate the distinct left cosets aH\."
)
D3_RE = re.compile(
    r"In D3 with elements e, r, r2, s, rs, r2s, let H=(\{[a-z0-9, ]+\})\. "
    r"Enumerate the distinct left cosets gH\."
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


def set_text(values):
    return "{" + list_text(values) + "}"


def parse_set(raw):
    body = raw.strip("{}")
    if not body:
        return []
    return body.split(", ")


def units(n):
    return [value for value in range(1, n) if gcd(value, n) == 1]


def d3_multiply(left, right):
    i, j = D3_PAIRS[left]
    k, ell = D3_PAIRS[right]
    return D3_NAMES[((i + (-1 if j else 1) * k) % 3, (j + ell) % 2)]


def coset_summary(cosets):
    return "; ".join(f"{label}={set_text(values)}" for label, values in cosets)


def parse_problem(problem):
    match = ZN_RE.fullmatch(problem)
    if match:
        n, element = map(int, match.groups())
        return {"variant": "zn", "n": n, "element": element}
    match = UNITS_RE.fullmatch(problem)
    if match:
        n, element = map(int, match.groups())
        return {"variant": "units", "n": n, "element": element}
    match = D3_RE.fullmatch(problem)
    assert match is not None, problem
    return {"variant": "d3", "subgroup": parse_set(match.group(1))}


def append_index_steps(steps, group_size, subgroup_size, index):
    steps.append(make_step("D", group_size, subgroup_size, index))
    steps.append(make_step("INDEX", f"G size {group_size}",
                           f"H size {subgroup_size}", index))
    steps.append(make_step("CHECK", "cosets partition group", "yes"))


def expected_zn(n, element):
    group = list(range(n))
    steps = [
        make_step("GROUP_SETUP", f"Z_{n}", "addition mod n",
                  f"group size {n}"),
        make_step("SUBGROUP_START", f"H=<{element}>", "identity 0"),
    ]
    subgroup = [0]
    current = 0
    for k in range(1, n + 1):
        previous = current
        total = previous + element
        current = total % n
        steps.append(make_step("A", previous, element, total))
        steps.append(make_step("MOD_REDUCE", total, f"mod {n}", current))
        steps.append(make_step("SUBGROUP_ELEM", f"k={k}", current))
        if current == 0:
            break
        subgroup.append(current)
    steps.append(make_step("SUBGROUP", f"H={set_text(subgroup)}",
                           f"size {len(subgroup)}"))

    cosets = []
    covered = set()
    for rep in group:
        if rep in covered:
            steps.append(make_step("COSET_SKIP", rep, "already listed"))
            continue
        label = f"{rep}+H"
        steps.append(make_step("COSET_START", f"rep {rep}", label))
        values = []
        for member in subgroup:
            total = rep + member
            value = total % n
            steps.append(make_step("A", rep, member, total))
            steps.append(make_step("MOD_REDUCE", total, f"mod {n}", value))
            steps.append(make_step("COSET_ELEM", label, value))
            values.append(value)
        covered.update(values)
        cosets.append((label, values))
        steps.append(make_step("COSET", label, set_text(values)))
    append_index_steps(steps, len(group), len(subgroup), len(cosets))
    answer = f"cosets = {coset_summary(cosets)}; index = {len(cosets)}"
    return steps, answer


def expected_units(n, element):
    group = units(n)
    steps = [
        make_step("GROUP_SETUP", f"U({n})", "multiplication mod n",
                  f"group size {len(group)}"),
        make_step("SUBGROUP_START", f"H=<{element}>", "identity 1"),
    ]
    subgroup = [1]
    current = 1
    for k in range(1, len(group) + 1):
        previous = current
        product = previous * element
        current = product % n
        steps.append(make_step("M", previous, element, product))
        steps.append(make_step("MOD_REDUCE", product, f"mod {n}", current))
        steps.append(make_step("SUBGROUP_ELEM", f"k={k}", current))
        if current == 1:
            break
        subgroup.append(current)
    steps.append(make_step("SUBGROUP", f"H={set_text(subgroup)}",
                           f"size {len(subgroup)}"))

    cosets = []
    covered = set()
    for rep in group:
        if rep in covered:
            steps.append(make_step("COSET_SKIP", rep, "already listed"))
            continue
        label = f"{rep}H"
        steps.append(make_step("COSET_START", f"rep {rep}", label))
        values = []
        for member in subgroup:
            product = rep * member
            value = product % n
            steps.append(make_step("M", rep, member, product))
            steps.append(make_step("MOD_REDUCE", product, f"mod {n}", value))
            steps.append(make_step("COSET_ELEM", label, value))
            values.append(value)
        covered.update(values)
        cosets.append((label, values))
        steps.append(make_step("COSET", label, set_text(values)))
    append_index_steps(steps, len(group), len(subgroup), len(cosets))
    answer = f"cosets = {coset_summary(cosets)}; index = {len(cosets)}"
    return steps, answer


def expected_d3(subgroup):
    steps = [
        make_step("GROUP_SETUP", "D3", "symmetries of a triangle",
                  f"group size {len(D3_ELEMENTS)}"),
        make_step("SUBGROUP", f"H={set_text(subgroup)}",
                  f"size {len(subgroup)}"),
    ]
    cosets = []
    covered = set()
    for rep in D3_ELEMENTS:
        if rep in covered:
            steps.append(make_step("COSET_SKIP", rep, "already listed"))
            continue
        label = f"{rep}H"
        steps.append(make_step("COSET_START", f"rep {rep}", label))
        values = []
        for member in subgroup:
            value = d3_multiply(rep, member)
            steps.append(make_step("GROUP_MULT", rep, member, value))
            steps.append(make_step("COSET_ELEM", label, value))
            values.append(value)
        covered.update(values)
        cosets.append((label, values))
        steps.append(make_step("COSET", label, set_text(values)))
    append_index_steps(steps, len(D3_ELEMENTS), len(subgroup), len(cosets))
    answer = f"cosets = {coset_summary(cosets)}; index = {len(cosets)}"
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "zn":
        steps, answer = expected_zn(parts["n"], parts["element"])
    elif parts["variant"] == "units":
        steps, answer = expected_units(parts["n"], parts["element"])
    else:
        steps, answer = expected_d3(parts["subgroup"])
    steps.append(make_step("Z", answer))
    return steps, answer


class TestCosetGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CosetGenerator()

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
                    self.assertEqual(int(fields[1]) % int(fields[2]), 0,
                                     raw_step)
                elif fields[0] == "MOD_REDUCE":
                    mod = int(fields[2].split()[1])
                    self.assertEqual(int(fields[1]) % mod, int(fields[3]),
                                     raw_step)
                elif fields[0] == "GROUP_MULT":
                    self.assertEqual(d3_multiply(fields[1], fields[2]),
                                     fields[3], raw_step)

    def test_variants_are_available(self):
        for variant in ("zn", "units", "d3"):
            gen = CosetGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"], f"coset_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CosetGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
