import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class ORFormulaGenerator(ProblemGenerator):
    """
    Operations-research formula chains for EOQ and M/M/1 queues.

    Variants:
    - eoq: economic order quantity and relevant annual costs
    - mm1: utilization, L, W, Lq, and Wq

    Op-codes used:
    - OR_SETUP: model inputs
    - FORMULA: formula being applied
    - ROOT: exact square root for EOQ
    - A / S / M / D / E (established/shared): exact arithmetic
    - CHECK: unit or stability check
    - Z: requested metrics
    """

    VARIANTS = ["eoq", "mm1"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "eoq":
            problem, steps, answer = self._generate_eoq()
        else:
            problem, steps, answer = self._generate_mm1()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"or_formula_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_eoq(self):
        q = 2 * random.randint(3, 30)
        holding = random.randint(1, 20)
        demand = q * holding
        order_cost = q // 2
        two_demand = 2 * demand
        numerator = two_demand * order_cost
        radicand = numerator // holding
        orders_per_year = Fraction(demand, q)
        annual_order_cost = orders_per_year * order_cost
        average_inventory = Fraction(q, 2)
        annual_holding_cost = average_inventory * holding
        total_cost = annual_order_cost + annual_holding_cost
        steps = [
            step("OR_SETUP", "EOQ", f"D={demand}", f"S={order_cost}, H={holding}"),
            step("FORMULA", "Q=sqrt(2DS/H)"),
            step("M", 2, demand, two_demand),
            step("M", two_demand, order_cost, numerator),
            step("D", numerator, holding, radicand),
            step("ROOT", radicand, q),
            step("FORMULA", "annual ordering cost=(D/Q)S"),
            step("D", demand, q, fraction_text(orders_per_year)),
            step("M", fraction_text(orders_per_year), order_cost,
                 fraction_text(annual_order_cost)),
            step("FORMULA", "annual holding cost=(Q/2)H"),
            step("D", q, 2, fraction_text(average_inventory)),
            step("M", fraction_text(average_inventory), holding,
                 fraction_text(annual_holding_cost)),
            step("A", fraction_text(annual_order_cost),
                 fraction_text(annual_holding_cost), fraction_text(total_cost)),
            step("CHECK", "ordering cost equals holding cost",
                 fraction_text(annual_order_cost)),
        ]
        answer = (
            f"EOQ={q}; ordering cost={fraction_text(annual_order_cost)}; "
            f"holding cost={fraction_text(annual_holding_cost)}; "
            f"total cost={fraction_text(total_cost)}"
        )
        problem = (
            f"For EOQ with annual demand D={demand}, order cost S={order_cost}, "
            f"and holding cost H={holding}, compute EOQ and annual relevant "
            "costs."
        )
        return problem, steps, answer

    def _generate_mm1(self):
        arrival = random.randint(1, 18)
        service = random.randint(arrival + 1, arrival + 20)
        gap = service - arrival
        rho = Fraction(arrival, service)
        L = Fraction(arrival, gap)
        W = Fraction(1, gap)
        arrival_sq = arrival ** 2
        queue_den = service * gap
        Lq = Fraction(arrival_sq, queue_den)
        Wq = Fraction(arrival, queue_den)
        steps = [
            step("OR_SETUP", "M/M/1", f"lambda={arrival}", f"mu={service}"),
            step("CHECK", f"lambda={arrival} < mu={service}", "stable"),
            step("S", service, arrival, gap),
            step("FORMULA", "rho=lambda/mu"),
            step("D", arrival, service, fraction_text(rho)),
            step("FORMULA", "L=lambda/(mu-lambda)"),
            step("D", arrival, gap, fraction_text(L)),
            step("FORMULA", "W=1/(mu-lambda)"),
            step("D", 1, gap, fraction_text(W)),
            step("FORMULA", "Lq=lambda^2/(mu*(mu-lambda))"),
            step("E", arrival, 2, arrival_sq),
            step("M", service, gap, queue_den),
            step("D", arrival_sq, queue_den, fraction_text(Lq)),
            step("FORMULA", "Wq=lambda/(mu*(mu-lambda))"),
            step("D", arrival, queue_den, fraction_text(Wq)),
        ]
        answer = (
            f"rho={fraction_text(rho)}; L={fraction_text(L)}; "
            f"W={fraction_text(W)}; Lq={fraction_text(Lq)}; "
            f"Wq={fraction_text(Wq)}"
        )
        problem = (
            f"For an M/M/1 queue with arrival rate lambda={arrival} and "
            f"service rate mu={service}, compute rho, L, W, Lq, and Wq."
        )
        return problem, steps, answer
