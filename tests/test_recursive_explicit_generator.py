import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.recursive_explicit_generator import (
    RecursiveExplicitGenerator,
)
from helpers import DELIM


def unroll_recursive(text, count=6):
    """'a_1 = 5; a_n = a_(n-1) + 3' or 'a_1 = 6; a_n = 3·a_(n-1)'."""
    m = re.fullmatch(
        r"a_1 = (-?\d+); a_n = (?:a_\(n-1\) ([+-]) (\d+)"
        r"|(-?\d+)·a_\(n-1\))", text)
    assert m, text
    a1 = int(m.group(1))
    seq = [a1]
    for _ in range(count - 1):
        if m.group(4):
            seq.append(int(m.group(4)) * seq[-1])
        else:
            d = int(m.group(3)) * (1 if m.group(2) == "+" else -1)
            seq.append(seq[-1] + d)
    return seq


def unroll_explicit(text, count=6):
    """'a_n = 3n + 2' or 'a_n = 5·(-2)^(n-1)'."""
    m = re.fullmatch(r"a_n = (-?\d+)·\(?(-?\d+)\)?\^\(n-1\)", text)
    if m:
        a, r = int(m.group(1)), int(m.group(2))
        return [a * r ** (n - 1) for n in range(1, count + 1)]
    m = re.fullmatch(r"a_n = (-?\d*)n(?: ([+-]) (\d+))?", text)
    assert m, text
    a = int(m.group(1) + "1") if m.group(1) in ("", "-") else int(m.group(1))
    b = int(m.group(3) or 0) * (1 if (m.group(2) or "+") == "+" else -1)
    return [a * n + b for n in range(1, count + 1)]


def oracle_check(example):
    """Both representations must generate the same first six terms."""
    p = example["problem"]
    m = re.fullmatch(
        r"The sequence is defined by a_1 = (-?\d+) and (.+) for n > 1\. "
        r"Write an explicit formula for a_n\.", p)
    if m:
        given = unroll_recursive(f"a_1 = {m.group(1)}; {m.group(2)}")
        converted = unroll_explicit(example["final_answer"])
        return given == converted
    m = re.fullmatch(r"The sequence is defined by (a_n = .+)\. "
                     r"Write a recursive definition\.", p)
    assert m, p
    given = unroll_explicit(m.group(1))
    converted = unroll_recursive(example["final_answer"])
    return given == converted


class TestRecursiveExplicitGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RecursiveExplicitGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_conversions_agree(self):
        """A9 oracle: unroll both forms six terms; they must match."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1].strip("()")) ** int(f[2]),
                                     int(f[3]), s)

    def test_rec_to_exp_unrolls_and_checks(self):
        for v in ("rec_to_exp_arith", "rec_to_exp_geo"):
            gen = RecursiveExplicitGenerator(v)
            for _ in range(150):
                result = gen.generate()
                unroll = next(s for s in result["steps"]
                              if s.startswith(f"UNROLL{DELIM}"))
                terms = [int(x) for x in unroll.split(DELIM)[1].split(", ")]
                self.assertEqual(len(terms), 4)
                chk = next(s for s in result["steps"]
                           if s.startswith(f"CHECK{DELIM}"))
                self.assertEqual(int(chk.split(DELIM)[3]), terms[3], chk)

    def test_exp_to_rec_evaluates_two_terms(self):
        for v in ("exp_to_rec_arith", "exp_to_rec_geo"):
            gen = RecursiveExplicitGenerator(v)
            for _ in range(150):
                result = gen.generate()
                evals = [s for s in result["steps"]
                         if s.startswith(f"EVAL{DELIM}")]
                self.assertEqual([e.split(DELIM)[1] for e in evals],
                                 ["a_1", "a_2"])

    def test_all_variants_reachable(self):
        ops = {}
        for _ in range(200):
            r = self.gen.generate()
            key = (r["operation"], "geo" if "·" in r["final_answer"]
                   or "^" in r["final_answer"] else "arith")
            ops[key] = ops.get(key, 0) + 1
        self.assertEqual(len(ops), 4, ops)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RecursiveExplicitGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
