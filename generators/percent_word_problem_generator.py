import random
from base_generator import ProblemGenerator
from helpers import step, jid


class PercentWordProblemGenerator(ProblemGenerator):
    """
    Generates percent change, markup/discount, and tax problems with explicit arithmetic steps.
    """

    def generate(self) -> dict:
        scenarios = [
            ("increase", "percent increase", "What is the new value after a {}% increase on {}?"),
            ("decrease", "percent decrease", "What is the new value after a {}% decrease on {}?"),
            ("markup", "markup", "A store marks up an item by {}% on a base price of {}. What is the new price?"),
            ("discount", "discount", "A {}% discount is applied to {}. What is the sale price?"),
            ("tax", "sales tax", "An item costs {} and a sales tax of {}% is applied. What is the total cost?"),
        ]

        scenario = random.choice(scenarios)
        pct = random.choice([5, 8, 10, 12, 15, 20, 25, 30])
        base = random.randint(20, 200) * 1  # dollars

        op_type, op_name, prompt = scenario
        problem = prompt.format(pct, base)

        steps = []
        pct_dec = pct / 100
        steps.append(step("PERCENT_TO_DEC", f"{pct}%", pct_dec))
        change = base * pct_dec
        if op_type in ("increase", "markup", "tax"):
            steps.append(step("M", base, pct_dec, change))
            new_total = base + change
            steps.append(step("A", base, change, new_total))
        else:  # decrease or discount
            steps.append(step("M", base, pct_dec, change))
            new_total = base - change
            steps.append(step("S", base, change, new_total))

        rounded = round(new_total, 2)
        if rounded.is_integer():
            final_answer = f"{int(rounded)}"
        else:
            final_answer = f"{rounded}"
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="percent_word_problem",
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
