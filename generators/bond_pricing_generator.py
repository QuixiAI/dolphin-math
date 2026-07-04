import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec, money
from generators.finance_generator import exact


def cents_exact(value):
    return (value * 100).denominator == 1


class BondPricingGenerator(ProblemGenerator):
    """
    Annual coupon bond pricing and current yield.

    Price is the sum of discounted coupon payments plus discounted face value.
    Current yield is annual coupon / bond price.

    Op-codes used:
    - BOND_SETUP / BOND_FORMULA / COUPON / CASHFLOW_PV / BOND_PRICE /
      CURRENT_YIELD
    - PERCENT_TO_DEC (established)
    - M / A / D / E (established/shared): exact discounting and yield
    - Z: price and current yield
    """

    def generate(self) -> dict:
        while True:
            face = random.randrange(500, 10001, 100)
            coupon_pct = random.choice([4, 5, 8, 10, 12, 20, 25])
            ytm_pct = random.choice([4, 5, 8, 10, 12, 20, 25, 50])
            years = random.randint(1, 6)
            coupon_rate = Fraction(coupon_pct, 100)
            ytm = Fraction(ytm_pct, 100)
            coupon = face * coupon_rate
            base = 1 + ytm
            coupon_pvs = [Fraction(coupon, 1) / (base ** t)
                          for t in range(1, years + 1)]
            face_pv = Fraction(face, 1) / (base ** years)
            price = sum(coupon_pvs, face_pv)
            if cents_exact(price):
                break
        current_yield = Fraction(coupon, 1) / price
        steps = [
            step("BOND_SETUP", f"face={face}",
                 f"coupon={coupon_pct}%,ytm={ytm_pct}%,years={years}"),
            step("PERCENT_TO_DEC", f"{coupon_pct}%", dec(coupon_rate)),
            step("PERCENT_TO_DEC", f"{ytm_pct}%", dec(ytm)),
            step("BOND_FORMULA", "price=sum coupon/(1+y)^t + face/(1+y)^n"),
            step("M", face, dec(coupon_rate), exact(coupon)),
            step("COUPON", exact(coupon)),
            step("A", 1, dec(ytm), exact(base)),
        ]
        running = Fraction(0)
        for t, pv in enumerate(coupon_pvs, start=1):
            new_running = running + pv
            steps.extend([
                step("E", exact(base), t, exact(base ** t)),
                step("D", exact(coupon), exact(base ** t), exact(pv)),
                step("CASHFLOW_PV", f"coupon_t{t}", exact(pv)),
                step("A", exact(running), exact(pv), exact(new_running)),
            ])
            running = new_running
        steps.extend([
            step("E", exact(base), years, exact(base ** years)),
            step("D", face, exact(base ** years), exact(face_pv)),
            step("CASHFLOW_PV", "face", exact(face_pv)),
            step("A", exact(running), exact(face_pv), exact(price)),
            step("BOND_PRICE", money(price)),
            step("D", exact(coupon), exact(price), exact(current_yield)),
            step("CURRENT_YIELD", exact(current_yield)),
        ])
        answer = f"price {money(price)}; current_yield={exact(current_yield)}"
        steps.append(step("Z", answer))
        problem = (
            f"A bond has face value ${face}, annual coupon rate {coupon_pct}%, "
            f"yield to maturity {ytm_pct}%, and {years} years to maturity "
            "with annual coupons. Compute the bond price and current yield."
        )
        return dict(
            problem_id=jid(),
            operation="bond_pricing_current_yield",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
