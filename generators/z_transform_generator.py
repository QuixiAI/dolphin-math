import random

from base_generator import ProblemGenerator
from helpers import step, jid


def seq_text(values):
    return "[" + ",".join(str(value) for value in values) + "]"


def z_denom_text(r_value):
    if r_value > 0:
        return f"1-{r_value}z^-1"
    return f"1+{-r_value}z^-1"


def transform_text(numerator, r_value):
    return f"{numerator}/({z_denom_text(r_value)})"


def power_base_text(value):
    return f"({value})" if value < 0 else str(value)


class ZTransformGenerator(ProblemGenerator):
    """
    Basic z-transform pairs and first-order difference equations.

    Variants:
    - geometric: Z{A*r^n u[n]}
    - difference: solve y[n]-a*y[n-1]=delta[n]

    Op-codes used:
    - ZT_SETUP: transform problem setup
    - ZT_PAIR: basic z-transform pair
    - SHIFT: z-transform shift property
    - REWRITE: algebraic transform equation
    - TERMS: requested time-domain terms
    - E / M (established/shared): exact term arithmetic
    - Z: transform and terms
    """

    VARIANTS = ["geometric", "difference"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "geometric":
            problem, steps, answer = self._generate_geometric()
        else:
            problem, steps, answer = self._generate_difference()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"z_transform_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_geometric(self):
        amplitude = random.randint(1, 40)
        r_value = random.choice([v for v in range(-12, 13) if v not in (0,)])
        terms = []
        steps = [
            step("ZT_SETUP", "geometric",
                 f"x[n]={amplitude}*{power_base_text(r_value)}^n u[n]"),
            step("ZT_PAIR", "Z{r^n u[n]}=1/(1-r z^-1)"),
            step("REWRITE", f"X(z)={transform_text(amplitude, r_value)}"),
        ]
        for n in range(4):
            power = r_value ** n
            term = amplitude * power
            terms.append(term)
            steps += [
                step("E", r_value, n, power),
                step("M", amplitude, power, term),
            ]
        steps.append(step("TERMS", f"x[0..3]={seq_text(terms)}"))
        answer = (
            f"X(z)={transform_text(amplitude, r_value)}; "
            f"ROC magnitude(z)>{abs(r_value)}; terms={seq_text(terms)}"
        )
        problem = (
            f"Find the z-transform of x[n]={amplitude}*"
            f"{power_base_text(r_value)}^n u[n] "
            "and compute x[0] through x[3]."
        )
        return problem, steps, answer

    def _generate_difference(self):
        a_value = random.choice([v for v in range(-20, 21) if v not in (0,)])
        terms = []
        a_text = power_base_text(a_value)
        steps = [
            step("ZT_SETUP", "difference",
                 f"y[n]-{a_text}y[n-1]=delta[n]", "y[-1]=0"),
            step("SHIFT", "Z{y[n-1]}=z^-1Y(z)"),
            step("REWRITE", f"({z_denom_text(a_value)})Y(z)=1"),
            step("REWRITE", f"Y(z)={transform_text(1, a_value)}"),
        ]
        for n in range(5):
            term = a_value ** n
            terms.append(term)
            steps.append(step("E", a_value, n, term))
        steps.append(step("TERMS", f"y[0..4]={seq_text(terms)}"))
        answer = (
            f"Y(z)={transform_text(1, a_value)}; "
            f"y[0..4]={seq_text(terms)}"
        )
        problem = (
            f"Solve y[n]-{a_text}y[n-1]=delta[n] with y[-1]=0 using "
            "z-transforms, and list y[0] through y[4]."
        )
        return problem, steps, answer
