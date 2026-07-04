import random
from base_generator import ProblemGenerator
from helpers import step, jid

class ProportionalRelationshipGenerator(ProblemGenerator):
    """Generates proportional relationship problems (a/b = c/x or a/b = x/c)."""

    def generate(self) -> dict:
        operation = "proportional_relationship" # Correct operation name
        # Generate a simple proportion a/b = c/x or a/b = x/c
        # Ensure integer results for simplicity
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        k = random.randint(2, 5) # Multiplier

        if random.choice([True, False]):
            # Case 1: a/b = c/x  => x = (b*c)/a
            c = a * k
            x_ans = b * k
            problem = f"If {a} is to {b}, what is {c} proportional to?"
            proportion_str = f"{a}/{b} = {c}/x"
            factor1, factor2 = b, c
            divisor = a
        else:
            # Case 2: a/b = x/c => x = (a*c)/b
            c = b * k
            x_ans = a * k
            problem = f"If {a} is to {b}, what is proportional to {c}?"
            proportion_str = f"{a}/{b} = x/{c}"
            factor1, factor2 = a, c
            divisor = b

        cross = factor1 * factor2
        final_answer_str = str(x_ans)

        # Same step pattern as ProportionWordProblemGenerator:
        # numeric cross-multiplication, then isolate x, then divide
        steps = [
            step("PROP_SETUP", proportion_str),
            step("M", factor1, factor2, cross),
            step("EQ_SETUP", f"x = {cross}/{divisor}"),
            step("D", cross, divisor, x_ans),
        ]
        steps.append(step("Z", final_answer_str)) # Final answer step

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer_str
        )
