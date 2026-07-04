import random
from base_generator import ProblemGenerator
from helpers import step, jid


def term_txt(c, var, p):
    """One term: 3x^2, -x, 7. Zero coefficient returns ''."""
    if c == 0:
        return ""
    head = {1: "", -1: "-"}.get(c, str(c))
    if p == 0:
        return str(c)
    v = var if p == 1 else f"{var}^{p}"
    return f"{head}{v}"


def poly_txt(coefs, var):
    """Coefficients highest degree first -> 'x^3 - 2x^2 - 5x + 6'."""
    deg = len(coefs) - 1
    parts = []
    for i, c in enumerate(coefs):
        if c == 0:
            continue
        t = term_txt(abs(c), var, deg - i)
        if not parts:
            parts.append(term_txt(c, var, deg - i))
        else:
            parts.append(f"+ {t}" if c > 0 else f"- {t}")
    return " ".join(parts) if parts else "0"


class PolynomialLongDivisionGenerator(ProblemGenerator):
    """
    Polynomial long division: cubic dividend by a linear divisor, the
    long-division scratchpad in algebra form. The dividend is built as
    quotient·divisor + remainder, so every DIV_TERM is exact and all
    dividend coefficients are nonzero.

    Each cycle: divide leading terms, multiply back through the divisor,
    subtract the pair of leading terms, bring down the next term. Ends
    with the remainder (often nonzero).

    Op-codes used:
    - POLYDIV_SETUP: dividend and divisor (dividend, divisor)
    - DIV_TERM: divide the leading terms (established)
    - MUL_TERM: quotient term times the divisor (established)
    - POLY_SUB: subtract the product from the running head (work, result)
    - B: bring down the next term (established long-division code)
    - R: the remainder (established)
    - Z: quotient, plus remainder/(divisor) when R is nonzero
    """

    VARIANTS = ["monic", "nonmonic"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or \
            random.choice(["monic", "monic", "nonmonic"])
        var = random.choice(["x", "x", "y"])

        while True:
            if variant == "monic":
                da, db = 1, -random.choice(
                    [v for v in range(-5, 6) if v != 0])
            else:
                da = random.choice([2, 3])
                db = random.choice([v for v in range(-5, 6) if v != 0])
            q2 = random.randint(1, 3)
            q1 = random.choice([v for v in range(-5, 6) if v != 0])
            q0 = random.choice([v for v in range(-5, 6) if v != 0])
            rem = random.choice([0, 0] + list(range(-9, 10)))
            # dividend = (q2 v^2 + q1 v + q0)(da v + db) + rem
            d3 = q2 * da
            d2 = q1 * da + q2 * db
            d1 = q0 * da + q1 * db
            d0 = q0 * db + rem
            if 0 not in (d2, d1, d0):
                break

        dividend = poly_txt([d3, d2, d1, d0], var)
        divisor = poly_txt([da, db], var)
        quotient = poly_txt([q2, q1, q0], var)

        steps = [step("POLYDIV_SETUP", dividend, divisor)]
        heads = [d3, d2, d1, d0]
        qs = [(q2, 2), (q1, 1), (q0, 0)]
        lead = [d3, d2]          # current two leading coefficients
        for idx, (qc, qp) in enumerate(qs):
            lead_deg = 3 - idx
            steps.append(step("DIV_TERM",
                              term_txt(lead[0], var, lead_deg),
                              term_txt(da, var, 1), term_txt(qc, var, qp)))
            prod = [qc * da, qc * db]     # degrees lead_deg, lead_deg-1
            prod_render = (
                term_txt(prod[0], var, lead_deg) +
                (f" + {term_txt(abs(prod[1]), var, lead_deg - 1)}"
                 if prod[1] > 0 else
                 f" - {term_txt(abs(prod[1]), var, lead_deg - 1)}"))
            steps.append(step("MUL_TERM", term_txt(qc, var, qp), divisor,
                              prod_render))
            head_txt = (
                term_txt(lead[0], var, lead_deg) +
                (f" + {term_txt(abs(lead[1]), var, lead_deg - 1)}"
                 if lead[1] > 0 else
                 f" - {term_txt(abs(lead[1]), var, lead_deg - 1)}"))
            new_lead = lead[1] - prod[1]
            steps.append(step("POLY_SUB",
                              f"({head_txt}) - ({prod_render})",
                              term_txt(new_lead, var, lead_deg - 1)
                              if new_lead != 0 else "0"))
            if idx < 2:
                nxt = heads[idx + 2]
                steps.append(step("B", term_txt(nxt, var, 1 - idx)))
                lead = [new_lead, nxt]

        steps.append(step("R", new_lead))
        if new_lead == 0:
            answer = quotient
        elif new_lead > 0:
            answer = f"{quotient} + {new_lead}/({divisor})"
        else:
            answer = f"{quotient} - {-new_lead}/({divisor})"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="polynomial_long_division",
            problem=f"Divide: ({dividend}) ÷ ({divisor}).",
            steps=steps,
            final_answer=answer,
        )
