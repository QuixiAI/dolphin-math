import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.complex_number_ops_generator import cx


class ComplexQuadraticGenerator(ProblemGenerator):
    """
    Solves monic quadratics with negative discriminant by the quadratic
    formula, producing complex conjugate roots.

    Variants:
    - gaussian: roots p ± qi with integers p, q (discriminant -4q^2)
    - radical:  roots p ± i√k with k squarefree (discriminant -4k)

    The equation is built from the roots, so the discriminant is negative
    by construction and the division by 2a is always exact.

    Op-codes used:
    - EQ_SETUP: the equation (established)
    - DISC: discriminant work and value (established)
    - DISC_CLASSIFY: negative discriminant -> two complex conjugate
      roots (established)
    - SQRT_NEG: square root of a negative number in i-form
      (radicand work, value)
    - ROOT_SIMPLIFY: pull the square factor out of i√n (established)
    - Q1 / Q2: each root from the formula (-b, sqrt_disc, denom, root)
      (established shapes from QuadraticGenerator)
    - Z: 'x = p + qi or x = p - qi' (roots with + listed first)
    """

    VARIANTS = ["gaussian", "radical"]
    SQUAREFREE = [2, 3, 5, 6, 7, 10, 11, 13]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        p = random.randint(-6, 6)
        B = -2 * p

        if variant == "gaussian":
            q = random.randint(1, 6)
            k = q * q
        else:
            k = random.choice(self.SQUAREFREE)
        C = p * p + k
        disc = -4 * k

        b_txt = "" if B == 0 else (f" + {B}x" if B > 0 else f" - {-B}x")
        b_txt = b_txt.replace(" 1x", " x")
        eq = f"x^2{b_txt} + {C} = 0"

        wb = f"({B})" if B < 0 else str(B)
        steps = [
            step("EQ_SETUP", eq, "solve"),
            step("DISC", f"{wb}^2 - 4(1)({C})", disc),
            step("DISC_CLASSIFY", f"{disc} < 0",
                 "two complex conjugate roots"),
        ]

        if variant == "gaussian":
            sqrt_txt = f"{2 * q}i"
            root_hi, root_lo = cx(p, q), cx(p, -q)
            steps.append(step("SQRT_NEG", f"√({disc})", sqrt_txt))
        else:
            sqrt_txt = f"2i√{k}"
            imag = f"i√{k}"
            root_hi = f"{p} + {imag}" if p != 0 else imag
            root_lo = f"{p} - {imag}" if p != 0 else f"-{imag}"
            steps.append(step("SQRT_NEG", f"√({disc})", f"i√{-disc}"))
            steps.append(step("ROOT_SIMPLIFY", sqrt_txt))

        answer = f"x = {root_hi} or x = {root_lo}"
        steps.append(step("Q1", -B, sqrt_txt, 2, root_hi))
        steps.append(step("Q2", -B, sqrt_txt, 2, root_lo))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="quadratic_complex_roots",
            problem=f"Solve: {eq}.",
            steps=steps,
            final_answer=answer,
        )
