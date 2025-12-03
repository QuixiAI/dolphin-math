import random
import math
from base_generator import ProblemGenerator
from helpers import step, jid


class RepeatingDecimalGenerator(ProblemGenerator):
    """
    Determines whether a fraction converts to a terminating or repeating decimal and shows the decimal expansion.
    """

    def generate(self) -> dict:
        terminating_denoms = [2, 4, 5, 8, 10, 16, 20, 25, 40]
        repeating_denoms = [3, 6, 7, 9, 11, 12, 13]
        denom = random.choice(terminating_denoms + repeating_denoms)
        num = random.randint(1, denom - 1)

        # Simplify fraction
        g = math.gcd(num, denom)
        simp_num, simp_den = num // g, denom // g

        steps = []
        steps.append(step("F", f"{num}/{denom}", f"{simp_num}/{simp_den}"))

        # Factor denominator
        factors = []
        d = simp_den
        for p in [2, 5]:
            while d % p == 0:
                factors.append(p)
                steps.append(step("PF_STEP", d, p, d // p))
                d //= p
        while d > 1:
            # Treat remaining d as prime for our limited set
            factors.append(d)
            steps.append(step("PF_PRIME", d))
            break

        kind = "terminating" if all(f in (2, 5) for f in factors) else "repeating"
        steps.append(step("DEC_TYPE", f"{simp_num}/{simp_den}", kind))

        decimal_value = round(simp_num / simp_den, 6)
        decimal_str = f"{decimal_value:.6f}" if kind == "repeating" else str(decimal_value).rstrip("0").rstrip(".")
        steps.append(step("DEC_VALUE", f"{simp_num}/{simp_den}", decimal_str))

        final_answer = f"{decimal_str} ({kind})"
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="repeating_decimal",
            problem=f"Determine if {simp_num}/{simp_den} is terminating or repeating, and give the decimal.",
            steps=steps,
            final_answer=final_answer,
        )
