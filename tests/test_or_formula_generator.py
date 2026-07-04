import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.or_formula_generator import ORFormulaGenerator
from helpers import DELIM


EOQ_RE = re.compile(
    r"For EOQ with annual demand D=(\d+), order cost S=(\d+), and holding "
    r"cost H=(\d+), compute EOQ and annual relevant costs\."
)
MM1_RE = re.compile(
    r"For an M/M/1 queue with arrival rate lambda=(\d+) and service rate "
    r"mu=(\d+), compute rho, L, W, Lq, and Wq\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_eoq(problem):
    demand, order_cost, holding = (
        int(value) for value in EOQ_RE.fullmatch(problem).groups()
    )
    two_demand = 2 * demand
    numerator = two_demand * order_cost
    radicand = Fraction(numerator, holding)
    q = int(radicand ** Fraction(1, 2))
    assert q * q == radicand
    orders_per_year = Fraction(demand, q)
    annual_order_cost = orders_per_year * order_cost
    average_inventory = Fraction(q, 2)
    annual_holding_cost = average_inventory * holding
    total_cost = annual_order_cost + annual_holding_cost
    steps = [
        make_step("OR_SETUP", "EOQ", f"D={demand}",
                  f"S={order_cost}, H={holding}"),
        make_step("FORMULA", "Q=sqrt(2DS/H)"),
        make_step("M", 2, demand, two_demand),
        make_step("M", two_demand, order_cost, numerator),
        make_step("D", numerator, holding, radicand),
        make_step("ROOT", radicand, q),
        make_step("FORMULA", "annual ordering cost=(D/Q)S"),
        make_step("D", demand, q, fraction_text(orders_per_year)),
        make_step("M", fraction_text(orders_per_year), order_cost,
                  fraction_text(annual_order_cost)),
        make_step("FORMULA", "annual holding cost=(Q/2)H"),
        make_step("D", q, 2, fraction_text(average_inventory)),
        make_step("M", fraction_text(average_inventory), holding,
                  fraction_text(annual_holding_cost)),
        make_step("A", fraction_text(annual_order_cost),
                  fraction_text(annual_holding_cost),
                  fraction_text(total_cost)),
        make_step("CHECK", "ordering cost equals holding cost",
                  fraction_text(annual_order_cost)),
    ]
    answer = (
        f"EOQ={q}; ordering cost={fraction_text(annual_order_cost)}; "
        f"holding cost={fraction_text(annual_holding_cost)}; "
        f"total cost={fraction_text(total_cost)}"
    )
    return steps, answer


def expected_mm1(problem):
    arrival, service = (int(value) for value in MM1_RE.fullmatch(problem).groups())
    gap = service - arrival
    rho = Fraction(arrival, service)
    L = Fraction(arrival, gap)
    W = Fraction(1, gap)
    arrival_sq = arrival ** 2
    queue_den = service * gap
    Lq = Fraction(arrival_sq, queue_den)
    Wq = Fraction(arrival, queue_den)
    steps = [
        make_step("OR_SETUP", "M/M/1", f"lambda={arrival}",
                  f"mu={service}"),
        make_step("CHECK", f"lambda={arrival} < mu={service}", "stable"),
        make_step("S", service, arrival, gap),
        make_step("FORMULA", "rho=lambda/mu"),
        make_step("D", arrival, service, fraction_text(rho)),
        make_step("FORMULA", "L=lambda/(mu-lambda)"),
        make_step("D", arrival, gap, fraction_text(L)),
        make_step("FORMULA", "W=1/(mu-lambda)"),
        make_step("D", 1, gap, fraction_text(W)),
        make_step("FORMULA", "Lq=lambda^2/(mu*(mu-lambda))"),
        make_step("E", arrival, 2, arrival_sq),
        make_step("M", service, gap, queue_den),
        make_step("D", arrival_sq, queue_den, fraction_text(Lq)),
        make_step("FORMULA", "Wq=lambda/(mu*(mu-lambda))"),
        make_step("D", arrival, queue_den, fraction_text(Wq)),
    ]
    answer = (
        f"rho={fraction_text(rho)}; L={fraction_text(L)}; "
        f"W={fraction_text(W)}; Lq={fraction_text(Lq)}; "
        f"Wq={fraction_text(Wq)}"
    )
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if EOQ_RE.fullmatch(problem):
        steps, answer = expected_eoq(problem)
    else:
        steps, answer = expected_mm1(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestORFormulaGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ORFormulaGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
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
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    self.assertEqual(int(fields[2]) ** 2, int(fields[1]),
                                     raw_step)

    def test_variants_are_available(self):
        for variant in ORFormulaGenerator.VARIANTS:
            result = ORFormulaGenerator(variant).generate()
            self.assertEqual(result["operation"], f"or_formula_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ORFormulaGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
