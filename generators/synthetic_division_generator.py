import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.polynomial_long_division_generator import poly_txt


class SyntheticDivisionGenerator(ProblemGenerator):
    """
    Synthetic division by (x - r): write the coefficient row (with a 0
    placeholder for any missing term), bring down the lead, then the
    multiply-add rhythm across the columns. The bottom row is read back
    as the quotient and remainder.

    The synthetic value r is stated explicitly from the divisor - the
    sign flip for a divisor like x + 2 is the classic trap.

    Variants:
    - cubic:        all four dividend coefficients nonzero
    - missing_term: one interior coefficient is zero; the COEFFS step
      records the inserted 0 placeholder
    - quartic:      one extra multiply-add column

    Op-codes used:
    - SYNDIV_SETUP: dividend and the synthetic value (dividend, r = ...)
    - COEFFS: the coefficient row (row, optional placeholder note)
    - SYN_DROP: bring down the leading coefficient (value)
    - M / A: the multiply-by-r / add-column rhythm (established)
    - SYN_ROW: the completed bottom row (row)
    - R: the remainder (established)
    - Z: quotient, plus remainder/(divisor) when nonzero
    """

    VARIANTS = ["cubic", "missing_term", "quartic"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choices(
            self.VARIANTS, weights=[55, 25, 20])[0]
        var = "x"
        r = random.choice([v for v in range(-5, 6) if v != 0])

        while True:
            if variant == "quartic":
                q = [random.randint(1, 2)] + \
                    [random.choice([v for v in range(-4, 5) if v != 0])
                     for _ in range(3)]
            else:
                q = [random.randint(1, 3)] + \
                    [random.choice([v for v in range(-5, 6) if v != 0])
                     for _ in range(2)]
            rem = random.choice([0, 0] + list(range(-9, 10)))
            # dividend coefficients from q and rem
            coefs = [q[0]]
            for i in range(1, len(q)):
                coefs.append(q[i] - r * q[i - 1])
            coefs.append(rem - r * q[-1])
            interior = coefs[1:-1]
            if variant == "missing_term":
                if interior.count(0) == 1 and coefs[-1] != 0 != coefs[0]:
                    break
            else:
                if 0 not in coefs:
                    break

        dividend = poly_txt(coefs, var)
        divisor = poly_txt([1, -r], var)
        quotient = poly_txt(q, var)

        steps = [step("SYNDIV_SETUP", dividend, f"r = {r}")]
        row_txt = ", ".join(str(c) for c in coefs)
        if variant == "missing_term":
            deg = len(coefs) - 1 - coefs.index(0)
            missing = var if deg == 1 else f"{var}^{deg}"
            steps.append(step("COEFFS", row_txt,
                              f"0 inserted for missing {missing} term"))
        else:
            steps.append(step("COEFFS", row_txt))
        steps.append(step("SYN_DROP", coefs[0]))

        bottom = [coefs[0]]
        for c in coefs[1:]:
            prod = r * bottom[-1]
            steps.append(step("M", r, bottom[-1], prod))
            steps.append(step("A", c, prod, c + prod))
            bottom.append(c + prod)
        steps.append(step("SYN_ROW", ", ".join(str(v) for v in bottom)))
        steps.append(step("REWRITE", quotient))
        steps.append(step("R", rem))

        if rem == 0:
            answer = quotient
        elif rem > 0:
            answer = f"{quotient} + {rem}/({divisor})"
        else:
            answer = f"{quotient} - {-rem}/({divisor})"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="synthetic_division",
            problem=(f"Use synthetic division to divide "
                     f"({dividend}) by ({divisor})."),
            steps=steps,
            final_answer=answer,
        )
