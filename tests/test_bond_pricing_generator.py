import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.bond_pricing_generator import BondPricingGenerator
from generators.exponential_model_generator import dec, money
from generators.finance_generator import exact
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"A bond has face value \$(\d+), annual coupon rate (\d+)%, yield "
    r"to maturity (\d+)%, and (\d+) years to maturity with annual coupons\. "
    r"Compute the bond price and current yield\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    face = int(match.group(1))
    coupon_pct = int(match.group(2))
    ytm_pct = int(match.group(3))
    years = int(match.group(4))
    coupon_rate = Fraction(coupon_pct, 100)
    ytm = Fraction(ytm_pct, 100)
    coupon = face * coupon_rate
    base = 1 + ytm
    coupon_pvs = [Fraction(coupon, 1) / (base ** t)
                  for t in range(1, years + 1)]
    face_pv = Fraction(face, 1) / (base ** years)
    price = sum(coupon_pvs, face_pv)
    current_yield = Fraction(coupon, 1) / price
    steps = [
        make_step("BOND_SETUP", f"face={face}",
                  f"coupon={coupon_pct}%,ytm={ytm_pct}%,years={years}"),
        make_step("PERCENT_TO_DEC", f"{coupon_pct}%", dec(coupon_rate)),
        make_step("PERCENT_TO_DEC", f"{ytm_pct}%", dec(ytm)),
        make_step("BOND_FORMULA", "price=sum coupon/(1+y)^t + face/(1+y)^n"),
        make_step("M", face, dec(coupon_rate), exact(coupon)),
        make_step("COUPON", exact(coupon)),
        make_step("A", 1, dec(ytm), exact(base)),
    ]
    running = Fraction(0)
    for t, pv in enumerate(coupon_pvs, start=1):
        new_running = running + pv
        steps.extend([
            make_step("E", exact(base), t, exact(base ** t)),
            make_step("D", exact(coupon), exact(base ** t), exact(pv)),
            make_step("CASHFLOW_PV", f"coupon_t{t}", exact(pv)),
            make_step("A", exact(running), exact(pv), exact(new_running)),
        ])
        running = new_running
    steps.extend([
        make_step("E", exact(base), years, exact(base ** years)),
        make_step("D", face, exact(base ** years), exact(face_pv)),
        make_step("CASHFLOW_PV", "face", exact(face_pv)),
        make_step("A", exact(running), exact(face_pv), exact(price)),
        make_step("BOND_PRICE", money(price)),
        make_step("D", exact(coupon), exact(price), exact(current_yield)),
        make_step("CURRENT_YIELD", exact(current_yield)),
    ])
    answer = f"price {money(price)}; current_yield={exact(current_yield)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestBondPricingGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = BondPricingGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "bond_pricing_current_yield")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
