import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.modular_arithmetic_generator import (
    ModularArithmeticGenerator, isbn10_check, luhn_check,
)
from helpers import DELIM


def oracle_answer(example):
    """A9 oracle: recompute the modular arithmetic answer from the prompt."""
    problem = example["problem"]
    m = re.search(r"It is (\d+) o'clock.*after (\d+) hours", problem)
    if m:
        start, add = (int(v) for v in m.groups())
        reduced = (start + add) % 12
        return f"{12 if reduced == 0 else reduced} o'clock"
    m = re.search(r"ISBN-10 check digit for prefix (\d{9})", problem)
    if m:
        return isbn10_check(m.group(1))
    prefix = re.search(r"Luhn check digit for prefix (\d+)", problem).group(1)
    return str(luhn_check(prefix)[0])


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        code = parts[0]
        if code == "MOD_TERM":
            weight, digit = (int(v) for v in parts[1].split(" * "))
            if weight * digit != int(parts[2]):
                return False
        elif code == "LUHN_DIGIT":
            digit = int(parts[1].split()[1])
            raw, adjusted = (int(v) for v in re.fullmatch(
                r"(\d+) -> (\d+)", parts[3]
            ).groups())
            expected_raw = digit * 2 if parts[2] == "double" else digit
            expected_adjusted = expected_raw - 9 if expected_raw > 9 else expected_raw
            if raw != expected_raw or adjusted != expected_adjusted:
                return False
        elif code == "A":
            if int(parts[1]) + int(parts[2]) != int(parts[3]):
                return False
        elif code == "MOD_REDUCE":
            modulus = int(parts[2].split()[1])
            if int(parts[1]) % modulus != int(parts[3]):
                return False
        elif code == "CHECK" and "multiple of" in parts[3]:
            modulus = int(parts[3].split()[-1])
            if int(parts[2]) % modulus != 0:
                return False
    return True


class TestModularArithmeticGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ModularArithmeticGenerator()

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

    def test_check_digit_shapes(self):
        isbn = ModularArithmeticGenerator("isbn10")
        luhn = ModularArithmeticGenerator("luhn")
        for _ in range(100):
            self.assertRegex(isbn.generate()["final_answer"], r"^(\d|X)$")
            self.assertRegex(luhn.generate()["final_answer"], r"^\d$")

    def test_mod_reduce_present(self):
        for variant in ModularArithmeticGenerator.VARIANTS:
            result = ModularArithmeticGenerator(variant).generate()
            self.assertTrue(any(s.startswith(f"MOD_REDUCE{DELIM}")
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
            ModularArithmeticGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
