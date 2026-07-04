import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def z_minus(a):
    if a == 0:
        return "z"
    if a > 0:
        return f"(z-{a})"
    return f"(z+{-a})"


def poly_text(coeffs, base):
    parts = []
    for power, coef in enumerate(coeffs):
        if coef == 0:
            continue
        abs_coef = abs(coef)
        if power == 0:
            body = str(abs_coef)
        elif power == 1:
            body = base if abs_coef == 1 else f"{abs_coef}{base}"
        else:
            body = f"{base}^{power}" if abs_coef == 1 else \
                f"{abs_coef}{base}^{power}"
        if not parts:
            parts.append(body if coef > 0 else f"-{body}")
        else:
            parts.append(f"+ {body}" if coef > 0 else f"- {body}")
    return " ".join(parts) if parts else "0"


def signed_term(value):
    return f"+ {value}" if value >= 0 else f"- {-value}"


def denominator_text(pole):
    return z_minus(pole)


def rational_text(numerator, pole):
    body = f"{abs(numerator)}/{denominator_text(pole)}"
    return body if numerator > 0 else f"-{body}"


def frac_text(value):
    return str(Fraction(value))


def coefficient_answer(coeffs):
    return ", ".join(f"c_{power}={frac_text(value)}"
                     for power, value in coeffs)


class LaurentSeriesGenerator(ProblemGenerator):
    """
    Taylor and Laurent coefficients for hand-friendly rational functions.

    Variants:
    - pole: divide a local polynomial by (z-a)^m and shift powers.
    - geometric: expand A/(z-b) around a regular center by the
      geometric-series coefficient formula.

    Op-codes used:
    - LAURENT_SETUP / POWER_SHIFT / COEFF: coefficient bookkeeping
    - GEOMETRIC_FORMULA: exact rational coefficient formula
    - E / M / D (established/shared): coefficient arithmetic
    - Z: finite coefficient list
    """

    VARIANTS = ["pole", "geometric"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "pole":
            problem, steps, answer = self._generate_pole()
        else:
            problem, steps, answer = self._generate_geometric()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"laurent_series_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_pole(self):
        a = random.randint(-4, 4)
        order = random.choice([2, 3])
        max_power = random.choice([2, 3, 4])
        coeffs = [
            random.choice([v for v in range(-6, 7) if v != 0])
            for _ in range(order + max_power + 1)
        ]
        base = z_minus(a)
        numerator = poly_text(coeffs, base)
        function = f"({numerator})/{base}^{order}"
        steps = [
            step("LAURENT_SETUP", f"center a={a}", f"w={base}",
                 f"f={function}"),
            step("REWRITE", f"f = numerator/w^{order}",
                 f"numerator power k gives c_(k-{order})"),
        ]
        answer_terms = []
        for power, coef in enumerate(coeffs):
            laurent_power = power - order
            steps.append(step("POWER_SHIFT", f"k={power}",
                              f"{power}-{order}", laurent_power))
            steps.append(step("COEFF", f"c_{laurent_power}", coef))
            answer_terms.append((laurent_power, coef))
        answer = coefficient_answer(answer_terms)
        problem = (
            f"Find the Laurent coefficients c_n for n=-{order}.."
            f"{max_power} about z={a} of f(z) = {function}. "
            f"The numerator coefficients in powers of {base} are {coeffs}."
        )
        return problem, steps, answer

    def _generate_geometric(self):
        a = random.randint(-4, 4)
        d = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        pole = a - d
        numerator = random.choice([v for v in range(-6, 7) if v != 0])
        degree = random.choice([3, 4, 5])
        base = z_minus(a)
        function = rational_text(numerator, pole)
        steps = [
            step("LAURENT_SETUP", f"center a={a}", f"w={base}",
                 f"f={function}"),
            step("REWRITE", f"{denominator_text(pole)} = w {signed_term(d)}",
                 f"d=a-b={d}"),
            step("GEOMETRIC_FORMULA",
                 "c_n = A*(-1)^n/d^(n+1)",
                 f"A={numerator}, d={d}"),
        ]
        answer_terms = []
        for n in range(degree + 1):
            sign = -1 if n % 2 else 1
            denominator_power = d ** (n + 1)
            signed_numerator = numerator * sign
            coef = Fraction(signed_numerator, denominator_power)
            steps.append(step("E", d, n + 1, denominator_power))
            steps.append(step("M", numerator, sign, signed_numerator))
            steps.append(step("D", signed_numerator, denominator_power,
                              frac_text(coef)))
            steps.append(step("COEFF", f"c_{n}", frac_text(coef)))
            answer_terms.append((n, coef))
        answer = coefficient_answer(answer_terms)
        problem = (
            f"Find the Taylor coefficients c_n for n=0..{degree} "
            f"about z={a} of f(z) = {function}, written as sum c_n "
            f"{base}^n."
        )
        return problem, steps, answer
