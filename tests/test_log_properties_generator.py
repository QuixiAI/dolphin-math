import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.log_properties_generator import LogPropertiesGenerator
from helpers import DELIM

VALS = {"x": 2.3, "y": 1.7, "z": 3.1}


def eval_log_arg(arg):
    """'8x^3/y' -> numeric value of the argument."""
    if "/" in arg:
        num, den = arg.split("/")
        return eval_log_arg(num) / eval_log_arg(den)
    m = re.fullmatch(r"(\d*)((?:[xyz](?:\^\d+)?)*)", arg)
    assert m, arg
    val = float(m.group(1)) if m.group(1) else 1.0
    for vm in re.finditer(r"([xyz])(?:\^(\d+))?", m.group(2)):
        val *= VALS[vm.group(1)] ** int(vm.group(2) or 1)
    return val


def eval_expr(text):
    """Evaluates a sum of terms: ints and [c]log_b(arg)."""
    total = 0.0
    for sign, term in re.findall(r"(^|[+-]) ?([^+-]+)", " " + text):
        term = term.strip()
        s = -1.0 if sign == "-" else 1.0
        m = re.fullmatch(r"(\d*)log_(\d+)\((.+)\)", term)
        if m:
            c = int(m.group(1) or 1)
            b = int(m.group(2))
            total += s * c * math.log(eval_log_arg(m.group(3)), b)
        else:
            total += s * float(term)
    return total


def oracle_check(example):
    """The problem expression and the answer evaluate identically."""
    p = example["problem"]
    m = re.fullmatch(r"Expand: (.+)\.", p) or \
        re.fullmatch(r"Write as a single logarithm: (.+)\.", p)
    assert m, p
    lhs = eval_expr(m.group(1))
    rhs = eval_expr(example["final_answer"])
    return abs(lhs - rhs) < 1e-9


class TestLogPropertiesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LogPropertiesGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_equivalence(self):
        """A9 oracle: both sides evaluate identically at fixed points."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_every_rule_step_preserves_value(self):
        """Each LOG_* rule application is itself an identity."""
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] in ("LOG_PRODUCT", "LOG_QUOTIENT", "LOG_POWER"):
                    self.assertLess(
                        abs(eval_expr(f[1]) - eval_expr(f[2])), 1e-9, s)

    def test_expand_answers_have_no_parenthesized_products(self):
        gen = LogPropertiesGenerator("expand")
        for _ in range(200):
            result = gen.generate()
            # expanded form: only single-variable or numeric log terms
            for m in re.finditer(r"log_\d+\(([^)]+)\)",
                                 result["final_answer"]):
                self.assertRegex(m.group(1), r"^[xyz]$|^\d+$",
                                 result["final_answer"])

    def test_condense_answer_is_single_log(self):
        gen = LogPropertiesGenerator("condense")
        for _ in range(200):
            result = gen.generate()
            self.assertEqual(result["final_answer"].count("log"), 1)
            self.assertNotIn(" + ", result["final_answer"])
            self.assertNotIn(" - ", result["final_answer"])

    def test_numeric_factor_evaluated_with_power_shown(self):
        gen = LogPropertiesGenerator("expand")
        for _ in range(300):
            result = gen.generate()
            evs = [s for s in result["steps"]
                   if s.startswith(f"EVAL{DELIM}")]
            for ev in evs:
                f = ev.split(DELIM)
                m = re.fullmatch(r"log_(\d+)\((\d+)\)", f[1])
                self.assertEqual(int(m.group(1)) ** int(f[2]),
                                 int(m.group(2)), ev)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"log_expand", "log_condense"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            LogPropertiesGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
