import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

# A4: several natural-language phrasings per scenario. Keyed by the
# arithmetic type so the solving steps stay identical while the
# surface form varies (this also grows the dedup space). Placeholders
# are named so operand order in the sentence never affects the math.
PHRASINGS = {
    "increase": [
        "What is the new value after a {pct}% increase on {base}?",
        "A quantity of {base} grows by {pct}%. What is the result?",
        "Increase {base} by {pct}%. What do you get?",
    ],
    "decrease": [
        "What is the new value after a {pct}% decrease on {base}?",
        "A quantity of {base} shrinks by {pct}%. What is the result?",
        "Decrease {base} by {pct}%. What do you get?",
    ],
    "markup": [
        "A store marks up an item by {pct}% on a base price of ${base}. "
        "What is the new price?",
        "A wholesaler buys an item for ${base} and marks it up {pct}%. "
        "What is the retail price?",
    ],
    "discount": [
        "A {pct}% discount is applied to ${base}. What is the sale price?",
        "An item priced at ${base} is {pct}% off. What is the sale price?",
    ],
    "tax": [
        "An item costs ${base} and a sales tax of {pct}% is applied. "
        "What is the total cost?",
        "A ${base} purchase is charged {pct}% sales tax. What is the "
        "total?",
    ],
}

ADDITIVE = ("increase", "markup", "tax")

# A6: irrelevant facts to plant. Each number plays no role in the
# computation.
DISTRACTORS = [
    "The store has been open for {} years.",
    "There are {} other items on the shelf.",
    "The receipt is {} inches long.",
    "The cashier has worked there for {} months.",
    "The store closes at {} PM.",
]


class PercentWordProblemGenerator(ProblemGenerator):
    """
    Percent increase/decrease, markup, discount, and tax word problems
    with explicit arithmetic. Supports multiple phrasings per scenario
    (A4) and an optional distractor quantity the scratchpad must first
    filter out (A6).

    With distractor=True the problem carries one irrelevant number and
    the first step (SELECT_RELEVANT) names the numbers that matter and
    the one to ignore — the way a human crosses out unused data.

    Op-codes used:
    - SELECT_RELEVANT: relevant data vs. the distractor to ignore
    - PERCENT_TO_DEC / M / A / S (established)
    - Z: the resulting value
    """

    def __init__(self, distractor: bool = False):
        self.distractor = distractor
        if distractor:
            self.op_symbol = "distractor"

    def generate(self) -> dict:
        op_type = random.choice(list(PHRASINGS))
        prompt = random.choice(PHRASINGS[op_type])
        pct = random.choice([5, 8, 10, 12, 15, 20, 25, 30])
        base = random.randint(20, 200)
        problem = prompt.format(pct=pct, base=base)

        steps = []
        if self.distractor:
            d_sentence = random.choice(DISTRACTORS)
            d_val = random.randint(2, 40)
            problem = f"{problem} {d_sentence.format(d_val)}"
            steps.append(step("SELECT_RELEVANT",
                              f"base = {base}, rate = {pct}%",
                              f"ignore {d_val} (irrelevant)"))

        pct_dec = Fraction(pct, 100)
        change = Fraction(base) * pct_dec
        steps.append(step("PERCENT_TO_DEC", f"{pct}%", dec(pct_dec)))
        steps.append(step("M", base, dec(pct_dec), dec(change)))
        if op_type in ADDITIVE:
            new_total = base + change
            steps.append(step("A", base, dec(change), dec(new_total)))
        else:
            new_total = base - change
            steps.append(step("S", base, dec(change), dec(new_total)))

        final_answer = (str(new_total.numerator)
                        if new_total.denominator == 1
                        else dec(new_total))
        steps.append(step("Z", final_answer))

        operation = ("percent_word_problem_distractor"
                     if self.distractor else "percent_word_problem")
        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
