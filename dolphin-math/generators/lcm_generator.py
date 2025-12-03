import random
from base_generator import ProblemGenerator
from helpers import step, jid


class LCMGenerator(ProblemGenerator):
    """Computes least common multiple using Euclidean algorithm + formula."""

    def generate(self) -> dict:
        a = random.randint(10, 140)
        b = random.randint(10, 140)
        steps = []

        # Euclidean algorithm to find gcd with steps
        x, y = a, b
        steps.append(step("GCD_START", x, y))
        while y != 0:
            rem = x % y
            steps.append(step("GCD_STEP", x, y, rem))
            x, y = y, rem
        gcd = x
        steps.append(step("GCD_RESULT", gcd))

        lcm_val = abs(a * b) // gcd if gcd else 0
        steps.append(step("LCM_FROM_GCD", f"{a}*{b}", gcd, lcm_val))
        steps.append(step("Z", str(lcm_val)))

        return dict(
            problem_id=jid(),
            operation="lcm",
            problem=f"Find LCM of {a} and {b}",
            steps=steps,
            final_answer=str(lcm_val),
        )
