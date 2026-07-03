import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.radical_rationalize_generator import RadicalRationalizeGenerator
from generators.radical_multiply_generator import rad, split_square
from helpers import DELIM


def oracle_answer(example):
    """Independently rationalizes from the problem text alone."""
    expr = example["problem"].split(": ", 1)[1]

    m = re.fullmatch(r"(\d+)/√(\d+)", expr)
    if m:  # simple
        a, root = int(m.group(1)), int(m.group(2))
        g = gcd(a, root)
        num, den = a // g, root // g
        if den == 1:
            return rad(num, root)
        return f"{rad(num, root)}/{den}"

    m = re.fullmatch(r"√(\d+)/√(\d+)", expr)
    if m:  # quotient
        big, n = int(m.group(1)), int(m.group(2))
        assert big % n == 0
        k = big // n
        s, f = split_square(k)
        return rad(s, f)

    m = re.fullmatch(r"(\d+)/\((\d+) \+ √(\d+)\)", expr)
    assert m, expr
    a, b, root = (int(v) for v in m.groups())
    d = b * b - root
    g = gcd(gcd(a * b, a), d)
    n1, n2, dr = a * b // g, a // g, d // g
    if dr == 1:
        return f"{n1} - {rad(n2, root)}"
    return f"({n1} - {rad(n2, root)})/{dr}"


class TestRadicalRationalizeGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RadicalRationalizeGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "radical_rationalize")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: rationalize independently; no radical may remain in
        any denominator, and fractions must be fully reduced."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])
            ans = result["final_answer"]
            if "/" in ans:
                den = ans.rsplit("/", 1)[1]
                self.assertNotIn("√", den, ans)

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "D" and f[1].isdigit():
                    self.assertEqual(int(f[1]) // int(f[2]), int(f[3]), s)
                    self.assertEqual(int(f[1]) % int(f[2]), 0, s)
                elif f[0] == "SQUARE_FACTOR":
                    mm = re.fullmatch(r"(\d+) × (\d+)", f[2])
                    self.assertEqual(int(mm.group(1)) * int(mm.group(2)),
                                     int(f[1]), s)

    def test_conjugate_denominator_positive(self):
        gen = RadicalRationalizeGenerator("conjugate")
        for _ in range(100):
            result = gen.generate()
            e_step = next(s for s in result["steps"]
                          if s.startswith(f"E{DELIM}"))
            s_step = next(s for s in result["steps"]
                          if s.startswith(f"S{DELIM}"))
            self.assertGreater(int(s_step.split(DELIM)[3]), 0, s_step)

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(150):
            p = self.gen.generate()["problem"]
            expr = p.split(": ", 1)[1]
            if expr.startswith("√"):
                kinds.add("quotient")
            elif "(" in expr:
                kinds.add("conjugate")
            else:
                kinds.add("simple")
        self.assertEqual(kinds, {"quotient", "conjugate", "simple"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RadicalRationalizeGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
