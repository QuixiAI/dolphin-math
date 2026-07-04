import random

from base_generator import ProblemGenerator
from helpers import step, jid


def exp_txt(rate):
    if rate == 1:
        return "e^x"
    if rate == -1:
        return "e^(-x)"
    return f"e^({rate}x)"


def term_txt(coeff, rate=None):
    if rate is None:
        return str(abs(coeff))
    body = exp_txt(rate)
    if abs(coeff) == 1:
        return body
    return f"{abs(coeff)}{body}"


def coeff_exp_txt(coeff, rate):
    if coeff == 1:
        return exp_txt(rate)
    if coeff == -1:
        return f"-{exp_txt(rate)}"
    return f"{coeff}{exp_txt(rate)}"


def left_side_txt(a):
    return "y' + y" if a == 1 else f"y' + {a}y"


def if_left_txt(a):
    return (f"{exp_txt(a)}y' + {exp_txt(a)}y" if a == 1 else
            f"{exp_txt(a)}y' + {a}{exp_txt(a)}y")


def solution_txt(terms):
    pieces = []
    for coeff, rate in terms:
        if coeff == 0:
            continue
        body = term_txt(coeff, rate)
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return "y = " + " ".join(pieces)


class IntegratingFactorGenerator(ProblemGenerator):
    """
    First-order linear differential equations solved by an integrating factor.
    Coefficients are chosen so the particular coefficient and integration
    constant are exact integers.

    Variants:
    - constant_rhs:    y' + ay = b
    - exponential_rhs: y' + ay = ce^(kx)

    Op-codes used:
    - ODE_SETUP (established): equation and initial condition
    - IFACTOR: integrating factor
    - MULTIPLY_IF: multiply the equation by the integrating factor
    - REWRITE / ANTIDERIV / SUBST (established)
    - A / D / S (established): coefficient and constant arithmetic
    - SOLVE_Y: divide by the integrating factor
    - Z: particular solution
    """

    VARIANTS = ["constant_rhs", "exponential_rhs"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        a = random.randint(1, 5)
        m = random.choice([1, 2, 3, 4, 5])
        C = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])

        if variant == "constant_rhs":
            b = a * m
            y0 = m + C
            answer = solution_txt([(m, None), (C, -a)])
            steps = [
                step("ODE_SETUP", f"{left_side_txt(a)} = {b}, y(0) = {y0}",
                     "integrating factor"),
                step("IFACTOR", f"mu = e^(∫ {a} dx)", exp_txt(a)),
                step("MULTIPLY_IF",
                     if_left_txt(a), coeff_exp_txt(b, a)),
                step("REWRITE", f"({exp_txt(a)}y)' = "
                     f"{coeff_exp_txt(b, a)}"),
                step("D", b, a, m),
                step("ANTIDERIV", f"{coeff_exp_txt(b, a)} dx",
                     f"{coeff_exp_txt(m, a)} + C"),
                step("SOLVE_Y", f"{exp_txt(a)}y = "
                     f"{coeff_exp_txt(m, a)} + C",
                     f"y = {m} + C{exp_txt(-a)}"),
                step("SUBST", "x", 0, f"{y0} = {m} + C"),
                step("S", y0, m, C),
            ]
            problem = (f"Solve {left_side_txt(a)} = {b} with y(0) = {y0} "
                       f"using an integrating factor.")
        else:
            k = random.choice([1, 2, 3, 4])
            denom = a + k
            c = denom * m
            y0 = m + C
            answer = solution_txt([(m, k), (C, -a)])
            steps = [
                step("ODE_SETUP",
                     f"{left_side_txt(a)} = {coeff_exp_txt(c, k)}, "
                     f"y(0) = {y0}",
                     "integrating factor"),
                step("IFACTOR", f"mu = e^(∫ {a} dx)", exp_txt(a)),
                step("MULTIPLY_IF",
                     if_left_txt(a), coeff_exp_txt(c, a + k)),
                step("REWRITE", f"({exp_txt(a)}y)' = "
                     f"{coeff_exp_txt(c, a + k)}"),
                step("A", a, k, denom),
                step("D", c, denom, m),
                step("ANTIDERIV", f"{coeff_exp_txt(c, a + k)} dx",
                     f"{coeff_exp_txt(m, a + k)} + C"),
                step("SOLVE_Y", f"{exp_txt(a)}y = "
                     f"{coeff_exp_txt(m, a + k)} + C",
                     f"y = {coeff_exp_txt(m, k)} + C{exp_txt(-a)}"),
                step("SUBST", "x", 0, f"{y0} = {m} + C"),
                step("S", y0, m, C),
            ]
            problem = (f"Solve {left_side_txt(a)} = {coeff_exp_txt(c, k)} "
                       f"with "
                       f"y(0) = {y0} using an integrating factor.")

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"integrating_factor_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
