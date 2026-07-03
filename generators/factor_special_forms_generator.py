import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


def sq_term(coef, var, power=2):
    """'4x^2' / 'x^2' for the squared leading term."""
    c = "" if coef == 1 else str(coef)
    return f"{c}{var}^{power}"


def lin(coef, var):
    """'2x' / 'x' for a linear term."""
    return var if coef == 1 else f"{coef}{var}"


class FactorSpecialFormsGenerator(ProblemGenerator):
    """
    Factors the special forms by pattern recognition:
    - difference of squares:      a² − b² = (a − b)(a + b)
    - perfect-square trinomials:  a² ± 2ab + b² = (a ± b)²
    - sum / difference of cubes:  a³ ± b³ = (a ± b)(a² ∓ ab + b²)

    The scratchpad identifies the pattern, extracts the roots, VERIFIES the
    pattern actually applies (the PST middle-term check is the load-bearing
    one), and expands back as the final check. All inputs are primitive
    (gcd of the two roots is 1) so no GCF hides inside.

    Op-codes used:
    - POLY_SETUP: the polynomial (string)
    - FORM_IDENTIFY: the pattern (name, formula)
    - ROOT: square root, numeric or symbolic (value, root)
    - CBRT: cube root, numeric or symbolic (value, root)
    - M / E: arithmetic for the cube-trinomial coefficients
    - CHECK: middle-term verification or expansion (method, lhs, rhs)
    - REWRITE: the factored form (string)
    - Z: final answer
    """

    VARIANTS = ["difference_of_squares", "perfect_square",
                "sum_of_cubes", "difference_of_cubes"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _cube_expansion(a, b, var, plus):
        """The six FOIL-style terms of (ax ± b)(a²x² ∓ abx + b²)."""
        A3 = sq_term(a ** 3, var, 3)
        A2B = sq_term(a * a * b, var)
        AB2 = lin(a * b * b, var)
        B3 = b ** 3
        if plus:   # (ax + b)(a²x² − abx + b²)
            return f"{A3} - {A2B} + {AB2} + {A2B} - {AB2} + {B3}"
        return f"{A3} + {A2B} + {AB2} - {A2B} - {AB2} - {B3}"

    def _roots(self, a_hi, b_hi):
        while True:
            a = random.randint(1, a_hi)
            b = random.randint(1, b_hi)
            if gcd(a, b) == 1:
                return a, b

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        var = random.choice(["x", "x", "y", "n"])

        if variant == "difference_of_squares":
            a, b = self._roots(6, 9)
            original = f"{sq_term(a * a, var)} - {b * b}"
            factored = f"({lin(a, var)} - {b})({lin(a, var)} + {b})"
            steps = [
                step("POLY_SETUP", original),
                step("FORM_IDENTIFY", "difference_of_squares",
                     "a^2 - b^2 = (a - b)(a + b)"),
                step("ROOT", sq_term(a * a, var), lin(a, var)),
                step("ROOT", b * b, b),
                step("REWRITE", factored),
                step("CHECK", "foil",
                     f"{sq_term(a * a, var)} + {lin(a * b, var)} - "
                     f"{lin(a * b, var)} - {b * b}", original),
                step("Z", factored),
            ]
            op = "factor_difference_of_squares"

        elif variant == "perfect_square":
            a, b = self._roots(5, 9)
            sign = random.choice(["+", "-"])
            mid = 2 * a * b
            original = f"{sq_term(a * a, var)} {sign} {lin(mid, var)} + {b * b}"
            factored = f"({lin(a, var)} {sign} {b})^2"
            formula = ("a^2 + 2ab + b^2 = (a + b)^2" if sign == "+"
                       else "a^2 - 2ab + b^2 = (a - b)^2")
            mid_txt = f"{sign if sign == '-' else ''}{lin(mid, var)}"
            steps = [
                step("POLY_SETUP", original),
                step("FORM_IDENTIFY", "perfect_square_trinomial", formula),
                step("ROOT", sq_term(a * a, var), lin(a, var)),
                step("ROOT", b * b, b),
                step("CHECK", "middle_term",
                     f"{sign if sign == '-' else ''}2·({lin(a, var)})·({b}) "
                     f"= {mid_txt}", mid_txt),
                step("REWRITE", factored),
                step("Z", factored),
            ]
            op = "factor_perfect_square"

        else:
            a, b = self._roots(4, 6)
            plus = variant == "sum_of_cubes"
            sign, inner_sign = ("+", "-") if plus else ("-", "+")
            original = f"{sq_term(a ** 3, var, 3)} {sign} {b ** 3}"
            trinomial = (f"{sq_term(a * a, var)} {inner_sign} "
                         f"{lin(a * b, var)} + {b * b}")
            factored = f"({lin(a, var)} {sign} {b})({trinomial})"
            formula = ("a^3 + b^3 = (a + b)(a^2 - ab + b^2)" if plus
                       else "a^3 - b^3 = (a - b)(a^2 + ab + b^2)")
            steps = [
                step("POLY_SETUP", original),
                step("FORM_IDENTIFY",
                     "sum_of_cubes" if plus else "difference_of_cubes",
                     formula),
                step("CBRT", sq_term(a ** 3, var, 3), lin(a, var)),
                step("CBRT", b ** 3, b),
                step("E", lin(a, var), 2, sq_term(a * a, var)),
                step("M", lin(a, var), b, lin(a * b, var)),
                step("E", b, 2, b * b),
                step("REWRITE", factored),
                step("CHECK", "expand", self._cube_expansion(a, b, var, plus),
                     original),
                step("Z", factored),
            ]
            op = f"factor_{variant}"

        return dict(
            problem_id=jid(),
            operation=op,
            problem=f"Factor: {original}",
            steps=steps,
            final_answer=factored,
        )
