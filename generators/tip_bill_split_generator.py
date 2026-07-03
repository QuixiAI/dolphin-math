import random
from base_generator import ProblemGenerator
from helpers import step, jid


def money(cents):
    """Formats integer cents as a dollars string with two decimals."""
    return f"{cents // 100}.{cents % 100:02d}"


class TipBillSplitGenerator(ProblemGenerator):
    """
    Generates tip and bill-splitting problems (consumer percent math).

    Variants:
    - tip_total:        bill + T% tip -> total including tip
    - tip_split:        bill + T% tip, split evenly among N people
    - find_tip_percent: bill and amount paid -> what percent was the tip?

    Bills are whole dollars and totals are constructed to split into exact
    cents, so every amount is exact. All internal math is integer cents.

    Op-codes used:
    - PERCENT_TO_DEC: Convert tip percent to decimal (percent, decimal)
    - M: Multiply bill by rate for the tip (bill, rate, tip)
    - A: Add tip to bill (bill, tip, total)
    - S: Subtract bill from paid to isolate the tip (paid, bill, tip)
    - D: Divide (total, people, per_person) or (tip, bill, rate)
    - DEC_TO_PERCENT: Convert rate back to percent (decimal, percent)
    - CHECK: Verify by an independent route (method, lhs_work, rhs_work)
    - Z: Final answer
    """

    TIP_PERCENTS = [10, 15, 18, 20, 25]
    PLACES = ["Louie's Diner", "the Harbor Grill", "Casa Verde", "the Noodle House",
              "Sunrise Cafe", "the Corner Bistro"]
    NAMES = ["Maya", "Devon", "Priya", "Marcus", "Elena", "Sam"]

    def __init__(self, problem_type=None):
        valid = ["tip_total", "tip_split", "find_tip_percent", None]
        if problem_type not in valid:
            raise ValueError(f"problem_type must be one of {valid}")
        self.problem_type = problem_type

    def generate(self) -> dict:
        ptype = self.problem_type or random.choice(
            ["tip_total", "tip_split", "find_tip_percent"])

        tip_pct = random.choice(self.TIP_PERCENTS)
        # Whole-dollar bill: tip in cents = dollars * pct, always exact.
        bill_dollars = random.randint(18, 240)
        bill = bill_dollars * 100
        tip = bill_dollars * tip_pct
        total = bill + tip
        place = random.choice(self.PLACES)

        rate = f"{tip_pct / 100:.2f}"

        if ptype == "tip_split":
            # Uniform party size first, then re-draw the bill until the total
            # splits into exact cents (avoids skewing toward 5-way splits).
            people = random.randint(2, 8)
            while total % people != 0:
                bill_dollars = random.randint(18, 240)
                bill = bill_dollars * 100
                tip = bill_dollars * tip_pct
                total = bill + tip
            per_person = total // people
            problem = (f"The dinner bill at {place} comes to ${money(bill)} for "
                       f"{people} friends. They add a {tip_pct}% tip and split the "
                       f"total evenly. How much does each person pay?")
            steps = [
                step("PERCENT_TO_DEC", f"{tip_pct}%", rate),
                step("M", money(bill), rate, money(tip)),
                step("A", money(bill), money(tip), money(total)),
                step("D", money(total), people, money(per_person)),
                step("CHECK", "split",
                     f"{money(per_person)}×{people}={money(total)}",
                     f"{money(bill)}+{money(tip)}={money(total)}"),
                step("Z", f"${money(per_person)}"),
            ]
            answer = f"${money(per_person)}"

        elif ptype == "tip_total":
            problem = (f"A meal at {place} costs ${money(bill)}. "
                       f"{random.choice(self.NAMES)} adds a {tip_pct}% tip. "
                       f"What is the total including tip?")
            steps = [
                step("PERCENT_TO_DEC", f"{tip_pct}%", rate),
                step("M", money(bill), rate, money(tip)),
                step("A", money(bill), money(tip), money(total)),
                step("CHECK", "tip_two_ways",
                     f"{money(total)}-{money(bill)}={money(tip)}",
                     f"{money(bill)}×{rate}={money(tip)}"),
                step("Z", f"${money(total)}"),
            ]
            answer = f"${money(total)}"

        else:  # find_tip_percent
            name = random.choice(self.NAMES)
            problem = (f"The bill at {place} was ${money(bill)}, and {name} paid "
                       f"${money(total)} including tip. What percent tip did "
                       f"{name} leave?")
            steps = [
                step("S", money(total), money(bill), money(tip)),
                step("D", money(tip), money(bill), rate),
                step("DEC_TO_PERCENT", rate, f"{tip_pct}%"),
                step("CHECK", "tip_two_ways",
                     f"{money(bill)}×{rate}={money(tip)}",
                     f"{money(total)}-{money(bill)}={money(tip)}"),
                step("Z", f"{tip_pct}%"),
            ]
            answer = f"{tip_pct}%"

        return dict(
            problem_id=jid(),
            operation=ptype,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
