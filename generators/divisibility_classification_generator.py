import random
from math import isqrt
from base_generator import ProblemGenerator
from helpers import step, jid


class DivisibilityClassificationGenerator(ProblemGenerator):
    """Checks divisibility by small primes and classifies as prime/composite."""

    def generate(self) -> dict:
        n = random.randint(10, 150)
        steps = []
        divisors = [2, 3, 5, 7, 11, 13]
        factors_found = []
        for d in divisors:
            if d > n:
                continue
            rem = n % d
            steps.append(step("DIV_CHECK", n, d, rem))
            if rem == 0:
                factors_found.append(d)
        if n > 1 and not factors_found:
            steps.append(step("PRIME", n))
            final_answer = "prime"
        else:
            # confirm composite via smallest found factor
            if factors_found:
                steps.append(step("COMPOSITE_FACTOR", factors_found[0], n // factors_found[0]))
            final_answer = "composite"
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="divisibility_classify",
            problem=f"Classify {n} as prime or composite",
            steps=steps,
            final_answer=final_answer,
        )
