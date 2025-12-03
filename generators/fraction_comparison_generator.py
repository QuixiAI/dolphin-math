import random
import math
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


class FractionComparisonGenerator(ProblemGenerator):
    """Compares two fractions using common denominator (human LCD method)."""

    def generate(self) -> dict:
        n1, d1 = random.randint(1, 9), random.randint(2, 12)
        n2, d2 = random.randint(1, 9), random.randint(2, 12)
        f1, f2 = Fraction(n1, d1), Fraction(n2, d2)

        # Ensure not equal too often; if equal, tweak
        if f1 == f2:
            n2 += 1
            f2 = Fraction(n2, d2)

        steps = []
        # LCD using simplified denominators
        lcd = math.lcm(f1.denominator, f2.denominator)
        if f1.denominator != f2.denominator:
            steps.append(step("L", f1.denominator, f2.denominator, lcd))

        n1c = f1.numerator * (lcd // f1.denominator)
        n2c = f2.numerator * (lcd // f2.denominator)
        if f1.denominator != lcd:
            steps.append(step("C", str(f1), lcd, f"{n1c}/{lcd}"))
        if f2.denominator != lcd:
            steps.append(step("C", str(f2), lcd, f"{n2c}/{lcd}"))

        # Compare converted numerators
        if n1c > n2c:
            relation = ">"
        elif n1c < n2c:
            relation = "<"
        else:
            relation = "="
        steps.append(step("CMP", f"{n1c}/{lcd}", f"{n2c}/{lcd}", relation))

        final_answer = f"{f1} {relation} {f2}"
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="fraction_compare",
            problem=f"Compare: {f1} ? {f2}",
            steps=steps,
            final_answer=final_answer,
        )
