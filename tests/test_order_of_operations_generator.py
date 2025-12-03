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


if __name__ == "__main__":
    unittest.main()
