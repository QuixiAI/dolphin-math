import random
from base_generator import ProblemGenerator
from helpers import step, jid


class SimpleProbabilityGenerator(ProblemGenerator):
    """Single-event probability with uniform outcomes."""

    def generate(self) -> dict:
        total = random.randint(3, 10)
        favorable = random.randint(1, total)
        operation = "probability_simple"
        problem = f"If an event has {favorable} favorable outcomes out of {total} equally likely outcomes, what is P?"

        steps = []
        steps.append(step("PROB_SETUP", favorable, total))
        # Round division result for human-readable display
        div_result = round(favorable / total, 2)
        steps.append(step("D", favorable, total, div_result))
        steps.append(step("F", f"{favorable}/{total}", f"{div_result:.2f}"))
        steps.append(step("Z", f"{div_result:.2f}"))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=f"{favorable/total:.2f}",
        )
