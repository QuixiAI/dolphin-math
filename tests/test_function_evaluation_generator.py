import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.function_evaluation_generator import (
    FunctionEvaluationGenerator,
)
from helpers import DELIM


def oracle_answer(example):
    """Independently evaluates from the problem text alone."""
    p = example["problem"]

    if example["operation"] == "function_evaluation_table":
        m = re.search(
            r"([a-z]+): ([-\d, ]+); [a-z]\(\1\): ([-\d, ]+)\. "
            r"Find [a-z]\((-?\d+)\)", p)
        xs = [int(v) for v in m.group(2).split(", ")]
        ys = [int(v) for v in m.group(3).split(", ")]
        k = int(m.group(4))
        return str(ys[xs.index(k)])

    m = re.fullmatch(
        r"Given [a-z]\(([a-z])\) = (-?\d+)\1(?:\^2)?"
        r"(?: ([+-]) (\d+)\1)?(?: ([+-]) (\d+))?, find [a-z]\((-?\d+)\)\.", p)
    assert m, p
    a = int(m.group(2))
    quadratic = "^2" in p.split(", find")[0]
    k = int(m.group(7))
    if quadratic:
        b = int(m.group(4) or 0) * (1 if (m.group(3) or "+") == "+" else -1)
        c = int(m.group(6) or 0) * (1 if (m.group(5) or "+") == "+" else -1)
        return str(a * k * k + b * k + c)
    # linear: the b-term is captured by group 5/6 (no var suffix group match)
    b = int(m.group(6) or 0) * (1 if (m.group(5) or "+") == "+" else -1)
    return str(a * k + b)


class TestFunctionEvaluationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FunctionEvaluationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: evaluate independently from the text."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "E":
                    base = int(f[1].strip("()"))
                    self.assertEqual(base ** int(f[2]), int(f[3]), s)
                elif f[0] == "M" and f[1].lstrip("-").isdigit():
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)

    def test_table_lookup_matches_table(self):
        gen = FunctionEvaluationGenerator("table")
        for _ in range(100):
            result = gen.generate()
            lookup = next(s for s in result["steps"]
                          if s.startswith(f"TABLE_LOOKUP{DELIM}"))
            self.assertEqual(lookup.split(DELIM)[2], result["final_answer"])

    def test_all_variants_reachable(self):
        ops = set()
        quads = 0
        for _ in range(150):
            result = self.gen.generate()
            ops.add(result["operation"])
            if "^2" in result["problem"]:
                quads += 1
        self.assertEqual(ops, {"function_evaluation_rule",
                               "function_evaluation_table"})
        self.assertGreater(quads, 20)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            FunctionEvaluationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
