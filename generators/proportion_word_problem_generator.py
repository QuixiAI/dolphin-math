import random
from base_generator import ProblemGenerator
from helpers import step, jid


class ProportionWordProblemGenerator(ProblemGenerator):
    """
    Generates proportion word problems with units (rates like mi/hr, $/lb, etc.) and solves via cross-multiplication.
    """

    def generate(self) -> dict:
        scenarios = [
            ("speed", "If a car travels {} miles in {} hours, how far will it travel in {} hours?", "mi", "hr", "distance"),
            ("cost", "If {} pounds of apples cost ${}, how much do {} pounds cost?", "lb", "$", "money"),
            ("recipe", "A recipe uses {} cups of flour for {} servings. How many cups are needed for {} servings?", "cups", "servings", "amount"),
            ("ratio_table", "Complete the ratio: {} {} corresponds to {} {}. What corresponds to {} {}?", None, None, "generic"),
        ]
        kind, prompt, unit1, unit2, answer_type = random.choice(scenarios)

        base1 = random.randint(1, 10)
        base2 = random.randint(1, 5)
        target = random.randint(2, 12)

        # Build known ratio a/b = x/target (solve for x)
        a = base1 * base2  # keep numbers reasonable
        b = base2
        if kind == "ratio_table":
            problem = f"Complete the ratio: {a} corresponds to {b}. What corresponds to {target}?"
        else:
            problem = prompt.format(a, b, target)

        steps = []
        steps.append(step("PROP_SETUP", f"{a}/{b} = x/{target}"))
        cross_mult = a * target
        steps.append(step("M", a, target, cross_mult))
        steps.append(step("EQ_SETUP", f"x = {cross_mult}/{b}"))
        result = cross_mult / b
        steps.append(step("D", cross_mult, b, result))
        if answer_type == "money":
            final_answer = f"${result:.2f}"
        elif answer_type in ("distance", "amount"):
            final_answer = f"{result} {unit1}"
        else:
            final_answer = f"{result}"
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="proportion_word_problem",
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
