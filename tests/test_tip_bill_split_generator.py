import os
import random
import re
import sys
import unittest
from decimal import Decimal

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.tip_bill_split_generator import TipBillSplitGenerator
from helpers import DELIM


def cents(s):
    """'85.00' or '$85.00' -> integer cents."""
    return int((Decimal(s.lstrip("$")) * 100).to_integral_value())


def oracle_answer(example):
    """Independently recomputes the answer from the problem text alone."""
    problem = example["problem"]
    op = example["operation"]
    dollars = [cents(m) for m in re.findall(r"\$(\d+\.\d{2})", problem)]
    if op == "find_tip_percent":
        bill, paid = dollars
        tip = paid - bill
        pct = tip * 100 // bill
        assert bill * pct == tip * 100, "tip percent not exact"
        return f"{pct}%"
    pct = int(re.search(r"(\d+)% tip", problem).group(1))
    bill = dollars[0]
    assert bill * pct % 100 == 0, "tip not exact cents"
    total = bill + bill * pct // 100
    if op == "tip_total":
        return f"${total // 100}.{total % 100:02d}"
    people = int(re.search(r"for (\d+) friends", problem).group(1))
    assert total % people == 0, "split not exact"
    per = total // people
    return f"${per // 100}.{per % 100:02d}"


class TestTipBillSplitGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TipBillSplitGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertIn(result["operation"],
                      ("tip_total", "tip_split", "find_tip_percent"))
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_all_variants_reachable(self):
        seen = {self.gen.generate()["operation"] for _ in range(60)}
        self.assertEqual(seen, {"tip_total", "tip_split", "find_tip_percent"})

    def test_fixed_variant_constructor(self):
        for ptype in ("tip_total", "tip_split", "find_tip_percent"):
            gen = TipBillSplitGenerator(ptype)
            for _ in range(10):
                self.assertEqual(gen.generate()["operation"], ptype)
        with self.assertRaises(ValueError):
            TipBillSplitGenerator("bogus")

    def test_oracle_answer_from_problem_text(self):
        """A9-style oracle: recompute the answer from the problem text alone."""
        for _ in range(300):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_all_step_arithmetic_verified(self):
        """Every A, S, M, D, and CHECK step must be independently true."""
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "A":
                    self.assertEqual(Decimal(f[1]) + Decimal(f[2]), Decimal(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(Decimal(f[1]) - Decimal(f[2]), Decimal(f[3]), s)
                elif f[0] in ("M", "D"):
                    x, y, z = Decimal(f[1]), Decimal(f[2]), Decimal(f[3])
                    if f[0] == "M":
                        self.assertEqual(x * y, z, s)
                    else:
                        self.assertEqual(x / y, z, s)
                elif f[0] == "CHECK":
                    self.assertIn(f[1], ("split", "tip_two_ways"), s)
                    vals = []
                    for work in f[2:4]:
                        m = re.fullmatch(
                            r"([\d.]+)([×+\-])([\d.]+)=([\d.]+)", work)
                        self.assertIsNotNone(m, s)
                        a, op_sym, b, r = (Decimal(m.group(1)), m.group(2),
                                           Decimal(m.group(3)), Decimal(m.group(4)))
                        got = a * b if op_sym == "×" else (
                            a + b if op_sym == "+" else a - b)
                        self.assertEqual(got, r, s)
                        vals.append(r)
                    self.assertEqual(vals[0], vals[1], f"CHECK routes differ: {s}")
                elif f[0] == "PERCENT_TO_DEC":
                    pct = Decimal(f[1].rstrip("%"))
                    self.assertEqual(pct / 100, Decimal(f[2]), s)
                elif f[0] == "DEC_TO_PERCENT":
                    self.assertEqual(Decimal(f[1]) * 100,
                                     Decimal(f[2].rstrip("%")), s)

    def test_answer_formats(self):
        for _ in range(100):
            result = self.gen.generate()
            if result["operation"] == "find_tip_percent":
                self.assertRegex(result["final_answer"], r"^\d+%$")
            else:
                self.assertRegex(result["final_answer"], r"^\$\d+\.\d{2}$")


if __name__ == "__main__":
    unittest.main()
