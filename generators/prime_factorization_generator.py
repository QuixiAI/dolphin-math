import random
from base_generator import ProblemGenerator
from helpers import step, jid


class PrimeFactorizationGenerator(ProblemGenerator):
    """Generates prime factorization using repeated division (factor tree style)."""

    def generate(self) -> dict:
        n = random.randint(24, 180)
        original = n
        steps = []
        factors = []
        divisor = 2

        while n > 1:
            if divisor * divisor > n:
                # Remaining n is prime
                steps.append(step("PF_PRIME", n))
                factors.append(n)
                break
            if n % divisor == 0:
                n_next = n // divisor
                steps.append(step("PF_STEP", n, divisor, n_next))
                factors.append(divisor)
                n = n_next
            else:
                divisor += 1

        final_answer = " × ".join(str(f) for f in factors)
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="prime_factorization",
            problem=f"Prime factorize {original}",
            steps=steps,
            final_answer=final_answer,
        )
