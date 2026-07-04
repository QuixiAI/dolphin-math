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

from generators.log_conversion_generator import LogConversionGenerator
from helpers import DELIM


def oracle_answer(example):
    """Recomputes each conversion/evaluation from the text alone."""
    p = example["problem"]
    m = re.fullmatch(r"Write (\d+)\^(\d+) = (\d+) in logarithmic form\.", p)
    if m:
        b, y, x = (int(v) for v in m.groups())
        assert b ** y == x
        return f"log_{b}({x}) = {y}"
    m = re.fullmatch(r"Write log_(\d+)\((\d+)\) = (\d+) in exponential "
                     r"form\.", p)
    if m:
        b, x, y = (int(v) for v in m.groups())
        assert b ** y == x
        return f"{b}^{y} = {x}"
    m = re.fullmatch(r"Evaluate log_(\d+)\((1/)?(\d+)\)\.", p)
    if m:
        b, recip, x = int(m.group(1)), m.group(2), int(m.group(3))
        y = round(math.log(x, b))
        assert b ** y == x
        return str(-y if recip else y)
    m = re.fullmatch(r"Use the change of base formula to evaluate "
                     r"log_(\d+)\((\d+)\)\.", p)
    if m:
        base2, big = int(m.group(1)), int(m.group(2))
        # exact: find the shared base c with integer exponents m, n
        for c in (2, 3, 5):
            lm = math.log(big, c)
            ln_ = math.log(base2, c)
            if abs(lm - round(lm)) < 1e-9 and abs(ln_ - round(ln_)) < 1e-9:
                return str(Fraction(round(lm), round(ln_)))
        raise AssertionError(p)
    m = re.fullmatch(r"Evaluate ln\(e\^(\d+)\)\.", p)
    if m:
        return m.group(1)
    if p == "Evaluate ln(1).":
        return "0"
    if p == "Evaluate ln(e).":
        return "1"
    m = re.fullmatch(r"Evaluate e\^\(ln (\d+)\)\.", p)
    assert m, p
    return m.group(1)


class TestLogConversionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LogConversionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute every form independently."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_evaluate_sweep_is_honest(self):
        gen = LogConversionGenerator("evaluate")
        for _ in range(300):
            result = gen.generate()
            b = int(re.search(r"log_(\d+)", result["problem"]).group(1))
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "TRY":
                    bb, k = f[1].split("^")
                    self.assertEqual(int(bb) ** int(k), int(f[2]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)
            accepts = [s for s in result["steps"]
                       if s.startswith(f"ACCEPT{DELIM}")]
            self.assertEqual(len(accepts), 1)

    def test_change_of_base_fraction_reduced(self):
        gen = LogConversionGenerator("change_of_base")
        for _ in range(200):
            result = gen.generate()
            a = result["final_answer"]
            if "/" in a:
                n, d = (int(v) for v in a.split("/"))
                self.assertEqual(str(Fraction(n, d)), a)

    def test_reciprocal_arguments_give_negatives(self):
        gen = LogConversionGenerator("evaluate")
        found = False
        for _ in range(200):
            result = gen.generate()
            if "1/" in result["problem"]:
                found = True
                self.assertTrue(result["final_answer"].startswith("-"))
        self.assertTrue(found)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(300):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"log_exp_to_log", "log_log_to_exp",
                               "log_evaluate", "log_change_of_base",
                               "log_ln_identity"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            LogConversionGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
