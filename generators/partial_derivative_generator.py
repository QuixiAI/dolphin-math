import random

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_power(var, exp):
    if exp == 0:
        return ""
    return var if exp == 1 else f"{var}^{exp}"


def fmt_term(c, mx, ny):
    if c == 0:
        return ""
    factors = []
    if c != 1 or (mx == 0 and ny == 0):
        factors.append(str(c))
    for factor in (fmt_power("x", mx), fmt_power("y", ny)):
        if factor:
            factors.append(factor)
    return "*".join(factors) if factors else "0"


def fmt_poly(terms):
    combined = combine_terms(terms)
    ordered = [(c, mx, ny) for c, mx, ny in combined if c]
    ordered.sort(key=lambda t: (-t[1], -t[2], -t[0]))
    rendered = [fmt_term(c, mx, ny) for c, mx, ny in ordered]
    return " + ".join(rendered) if rendered else "0"


def combine_terms(terms):
    combined = {}
    for c, mx, ny in terms:
        combined[(mx, ny)] = combined.get((mx, ny), 0) + c
    return [(c, mx, ny) for (mx, ny), c in combined.items() if c]


def derivative_terms(terms, var):
    out = []
    for c, mx, ny in terms:
        if var == "x":
            if mx:
                out.append((c * mx, mx - 1, ny))
        else:
            if ny:
                out.append((c * ny, mx, ny - 1))
    return out


class PartialDerivativeGenerator(ProblemGenerator):
    """
    Partial derivatives of two-variable polynomials, including second partials
    and mixed partials with Clairaut equality as a check.

    Variants:
    - first_x:  f_x
    - first_y:  f_y
    - second_xx: f_xx
    - second_yy: f_yy
    - mixed_xy: f_xy with f_yx check

    Op-codes used:
    - PARTIAL_SETUP: function and target
    - PARTIAL_RULE: one term differentiated with respect to x or y
    - PARTIAL_RESULT: assembled derivative expression
    - CHECK (established): Clairaut equality for mixed partials
    - Z: final derivative expression
    """

    VARIANTS = ["first_x", "first_y", "second_xx", "second_yy", "mixed_xy"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _random_terms():
        return [
            (random.randint(2, 8), random.randint(1, 4), random.randint(1, 4)),
            (random.randint(2, 8), random.randint(1, 4), random.randint(1, 4)),
        ]

    @staticmethod
    def _rule_steps(steps, terms, var):
        result = []
        for term in terms:
            derived = derivative_terms([term], var)
            rendered = fmt_poly(derived)
            steps.append(step("PARTIAL_RULE", fmt_term(*term),
                              f"d/d{var}", rendered))
            result.extend(derived)
        return result

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        terms = combine_terms(self._random_terms())
        f_txt = fmt_poly(terms)

        if variant == "first_x":
            target = "f_x"
            steps = [step("PARTIAL_SETUP", f"f(x,y) = {f_txt}", target)]
            dx = self._rule_steps(steps, terms, "x")
            answer = fmt_poly(dx)
            steps.append(step("PARTIAL_RESULT", target, answer))
        elif variant == "first_y":
            target = "f_y"
            steps = [step("PARTIAL_SETUP", f"f(x,y) = {f_txt}", target)]
            dy = self._rule_steps(steps, terms, "y")
            answer = fmt_poly(dy)
            steps.append(step("PARTIAL_RESULT", target, answer))
        elif variant == "second_xx":
            target = "f_xx"
            steps = [step("PARTIAL_SETUP", f"f(x,y) = {f_txt}", target)]
            dx = self._rule_steps(steps, terms, "x")
            steps.append(step("PARTIAL_RESULT", "f_x", fmt_poly(dx)))
            dxx = self._rule_steps(steps, dx, "x")
            answer = fmt_poly(dxx)
            steps.append(step("PARTIAL_RESULT", target, answer))
        elif variant == "second_yy":
            target = "f_yy"
            steps = [step("PARTIAL_SETUP", f"f(x,y) = {f_txt}", target)]
            dy = self._rule_steps(steps, terms, "y")
            steps.append(step("PARTIAL_RESULT", "f_y", fmt_poly(dy)))
            dyy = self._rule_steps(steps, dy, "y")
            answer = fmt_poly(dyy)
            steps.append(step("PARTIAL_RESULT", target, answer))
        else:
            target = "f_xy"
            steps = [step("PARTIAL_SETUP", f"f(x,y) = {f_txt}", target)]
            dx = self._rule_steps(steps, terms, "x")
            steps.append(step("PARTIAL_RESULT", "f_x", fmt_poly(dx)))
            dxy = self._rule_steps(steps, dx, "y")
            answer = fmt_poly(dxy)
            steps.append(step("PARTIAL_RESULT", "f_xy", answer))
            dy = derivative_terms(terms, "y")
            dyx = derivative_terms(dy, "x")
            steps.append(step("PARTIAL_RESULT", "f_yx", fmt_poly(dyx)))
            steps.append(step("CHECK", "f_xy = f_yx", answer,
                              "Clairaut equality"))
        steps.append(step("Z", answer))
        problem = f"Let f(x,y) = {f_txt}. Find {target}."

        return dict(
            problem_id=jid(),
            operation=f"partial_derivative_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
