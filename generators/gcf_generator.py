import random
from base_generator import ProblemGenerator
from helpers import step, jid


class GCFGenerator(ProblemGenerator):
    """Computes greatest common factor using Euclidean algorithm."""

    def generate(self) -> dict:
        a = random.randint(20, 180)
        b = random.randint(12, 160)
        steps = []
        steps.append(step("GCD_START", a, b))

        x, y = a, b
        while y != 0:
            rem = x % y
            steps.append(step("GCD_STEP", x, y, rem))
            x, y = y, rem

        gcd = x
        steps.append(step("Z", str(gcd)))

        return dict(
            problem_id=jid(),
            operation="gcf",
            problem=f"Find GCF of {a} and {b}",
            steps=steps,
            final_answer=str(gcd),
        )
