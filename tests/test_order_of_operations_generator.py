import re
import unittest
import random
import sys
import os

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.order_of_operations_generator import OrderOfOperationsGenerator
from fractions import Fraction
from helpers import DELIM


class TestOrderOfOperationsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = OrderOfOperationsGenerator()

    def test_format_and_z(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(res["operation"], "order_of_operations")

    def test_precedence_handling(self):
        # Force a known form
        gen = OrderOfOperationsGenerator()
        res = gen.generate()
        # Verify first arithmetic step honors precedence
        first_op = res["steps"][0].split(DELIM)[0]
        expr = res["problem"]
        if "*" in expr or "/" in expr:
            # Should not start with A/S on outer unless parentheses dictate
            if "(" not in expr.split("*")[0] and "(" not in expr.split("/")[0]:
                self.assertIn(first_op, {"M", "D"})

    def test_rewrite_sequence_no_duplicates(self):
        """Ensure expressions are rewritten once per precedence move (no duplicate ops)."""
        random.seed(1)
        gen = OrderOfOperationsGenerator()
        res = gen.generate()
        steps = res["steps"]
        # No adjacent identical arithmetic op-codes
        op_codes = [s.split(DELIM)[0] for s in steps if not s.startswith(f"REWRITE{DELIM}")]
        for prev, curr in zip(op_codes, op_codes[1:]):
            self.assertNotEqual(prev + curr, "AA")
            self.assertNotEqual(prev + curr, "MM")
            self.assertNotEqual(prev + curr, "SS")


def eval_expr_exact(expr):
    """Evaluates a problem expression with exact Fraction arithmetic.

    Handles integers, decimals, and mixed numbers ('2 1/2').
    """
    # mixed numbers -> (F(whole*den+num, den))
    expr = re.sub(r"(\d+) (\d+)/(\d+)",
                  lambda m: f"(F({int(m.group(1)) * int(m.group(3)) + int(m.group(2))},{m.group(3)}))",
                  expr)
    # bare fractions -> F(n, d)
    expr = re.sub(r"(?<![\w)])(\d+)/(\d+)", r"(F(\1,\2))", expr)
    # decimals -> F('2.4')
    expr = re.sub(r"(\d+\.\d+)", r"(F('\1'))", expr)
    # remaining bare integers -> F(n)
    expr = re.sub(r"(?<![\w.'])(\d+)(?![\w.'])", r"(F(\1))", expr)
    return eval(expr, {"F": Fraction})


def parse_answer(ans):
    m = re.fullmatch(r"(\d+) (\d+)/(\d+)", ans)
    if m:
        return Fraction(int(m.group(1)) * int(m.group(3)) + int(m.group(2)),
                        int(m.group(3)))
    if "/" in ans:
        return Fraction(ans)
    return Fraction(ans) if "." not in ans else Fraction(ans)


class TestOrderOfOperationsOracle(unittest.TestCase):
    """A9-style oracle: independently evaluate every problem expression."""

    def _oracle_sweep(self, mode, n=400):
        random.seed(7)
        gen = OrderOfOperationsGenerator(mode)
        for _ in range(n):
            res = gen.generate()
            expr = res["problem"].replace("Compute ", "")
            self.assertEqual(eval_expr_exact(expr),
                             parse_answer(res["final_answer"]),
                             f"{expr} != {res['final_answer']}")

    def test_integers_exact(self):
        """Regression: the old division guards could floor-divide silently."""
        self._oracle_sweep("integers", 1000)

    def test_decimals_exact(self):
        self._oracle_sweep("decimals")

    def test_mixed_numbers_exact(self):
        self._oracle_sweep("mixed_numbers")

    def test_modes_and_metadata(self):
        for mode, op, diff in (
                ("integers", "order_of_operations", 3),
                ("decimals", "order_of_operations_decimals", 4),
                ("mixed_numbers", "order_of_operations_mixed_numbers", 4)):
            random.seed(3)
            res = OrderOfOperationsGenerator(mode).generate()
            self.assertEqual(res["operation"], op)
            self.assertEqual(res["difficulty"], diff)  # A3 per-instance value
        with self.assertRaises(ValueError):
            OrderOfOperationsGenerator("bogus")

    def test_mixed_numbers_procedure(self):
        random.seed(11)
        gen = OrderOfOperationsGenerator("mixed_numbers")
        for _ in range(100):
            res = gen.generate()
            codes = [s.split(DELIM)[0] for s in res["steps"]]
            self.assertIn("MIX_IMPROPER", codes)
            self.assertIn("M", codes)
            self.assertEqual(codes[-1], "Z")


if __name__ == "__main__":
    unittest.main()
