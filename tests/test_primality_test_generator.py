import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.primality_test_generator import PrimalityTestGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Use the Miller-Rabin test on n=(\d+) with witnesses ([\d, ]+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def list_text(values):
    return ", ".join(str(value) for value in values)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    n = int(match.group(1))
    witnesses = [int(value) for value in match.group(2).split(", ")]
    return n, witnesses


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def decompose(n):
    value = n - 1
    s = 0
    d = value
    divisions = []
    while d % 2 == 0:
        next_d = d // 2
        divisions.append((d, next_d))
        s += 1
        d = next_d
    return s, d, divisions


def expected_flow(n, witnesses):
    s, d, divisions = decompose(n)
    steps = [
        make_step("MR_SETUP", f"n={n}", f"witnesses {list_text(witnesses)}"),
    ]
    for value, next_value in divisions:
        steps.append(make_step("D", value, 2, next_value))
    steps.append(make_step("MR_DECOMPOSE", n - 1, f"2^{s} * {d}"))

    composite_witness = None
    for witness in witnesses:
        steps.append(make_step("MR_WITNESS", witness))
        x = pow(witness, d, n)
        steps.append(make_step("MOD_POWER", f"{witness}^{d}", f"mod {n}", x))
        if x in (1, n - 1):
            steps.append(make_step("MR_WITNESS_RESULT", witness,
                                   "passes initial"))
            continue

        passed = False
        for r in range(1, s):
            previous = x
            squared = previous * previous
            x = squared % n
            steps.append(make_step("M", previous, previous, squared))
            steps.append(make_step("MOD_REDUCE", squared, f"mod {n}", x))
            steps.append(make_step("MR_SQUARE", f"r={r}", x))
            if x == n - 1:
                steps.append(make_step("MR_WITNESS_RESULT", witness,
                                       f"passes at r={r}"))
                passed = True
                break
        if not passed:
            steps.append(make_step("MR_WITNESS_RESULT", witness, "composite"))
            composite_witness = witness
            break

    if composite_witness is None:
        answer = f"probably prime for witnesses = {list_text(witnesses)}"
    else:
        answer = f"composite; witness = {composite_witness}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestPrimalityTestGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PrimalityTestGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "primality_test_miller_rabin")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            n, witnesses = parse_problem(result["problem"])
            expected_steps, answer = expected_flow(n, witnesses)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_witness_outcome_and_arithmetic(self):
        saw = set()
        for _ in range(500):
            result = self.gen.generate()
            n, witnesses = parse_problem(result["problem"])
            saw.add("composite" if result["final_answer"].startswith("composite")
                    else "probably")
            if is_prime(n):
                self.assertTrue(result["final_answer"].startswith("probably"))
            else:
                self.assertTrue(any(gcd(w, n) == 1 for w in witnesses))

            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]),
                                     int(fields[3]), raw_step)
                    self.assertEqual(int(fields[1]) % int(fields[2]), 0)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "MOD_REDUCE":
                    mod = int(fields[2].split()[1])
                    self.assertEqual(int(fields[1]) % mod, int(fields[3]),
                                     raw_step)
                elif fields[0] == "MOD_POWER":
                    base, exponent = map(int, fields[1].split("^"))
                    mod = int(fields[2].split()[1])
                    self.assertEqual(pow(base, exponent, mod),
                                     int(fields[3]), raw_step)
        self.assertEqual(saw, {"composite", "probably"})

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
