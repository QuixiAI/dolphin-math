import random
from math import isqrt
from base_generator import ProblemGenerator
from helpers import step, jid


class FactorsGenerator(ProblemGenerator):
    """Lists all factors of a number using trial division up to sqrt(n)."""

    def generate(self) -> dict:
        n = random.randint(12, 144)
        steps = []
        factors = set()

        for d in range(1, isqrt(n) + 1):
            rem = n % d
            steps.append(step("FACT_CHECK", n, d, rem))
            if rem == 0:
                pair = n // d
                factors.add(d)
                factors.add(pair)
                steps.append(step("FACT_PAIR", d, pair))

        factors_list = sorted(factors)
        final_answer = ", ".join(str(f) for f in factors_list)
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="factors_list",
            problem=f"List factors of {n}",
            steps=steps,
            final_answer=final_answer,
        )
