import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.factor_trinomial_generator import binomial
from generators.polynomial_long_division_generator import poly_txt


class LHopitalGenerator(ProblemGenerator):
    """
    L'Hôpital's rule with the 0/0 form checked before every
    application - including a variant that needs the rule twice.

    Variants:
    - rational: (x² + bx + c)/(x - r) at a root r
    - sin:      sin(kx)/x at 0 -> k
    - exp_log:  (e^(kx) - 1)/x at 0 -> k, or ln(x)/(x - 1) at 1 -> 1
    - double:   (1 - cos(kx))/x² at 0 -> k²/2, applied twice

    Op-codes used:
    - LIMIT_SETUP / CHECK / DERIV_RULE / POWER_RULE / REWRITE /
      SUBST (established)
    - Z: the limit
    """

    VARIANTS = ["rational", "sin", "exp_log", "double"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "rational":
            r, s = random.sample([v for v in range(-6, 7) if v != 0], 2)
            B, C = -(r + s), r * s
            num = poly_txt([1, B, C], "x")
            den = binomial("x", -r)
            val = 2 * r + B
            wr = f"({r})" if r < 0 else str(r)
            limit_txt = f"lim x→{r} of ({num})/{den}"
            steps = [
                step("LIMIT_SETUP", limit_txt, "L'Hôpital's rule"),
                step("CHECK", "substitution",
                     f"numerator and denominator both 0 at x = {r}",
                     "indeterminate 0/0"),
                step("DERIV_RULE", "L'Hôpital",
                     "replace with f'(x)/g'(x)"),
                step("POWER_RULE", num, poly_txt([2, B], "x")),
                step("POWER_RULE", den.strip("()"), "1"),
                step("REWRITE",
                     f"lim x→{r} of ({poly_txt([2, B], 'x')})/1"),
                step("SUBST", "x", r,
                     f"2{wr} {'+' if B > 0 else '-'} {abs(B)}"),
                step("M", 2, r, 2 * r),
                step("A", 2 * r, B, val),
            ]
            answer = str(val)
        elif variant == "sin":
            k = random.randint(2, 7)
            limit_txt = f"lim x→0 of sin({k}x)/x"
            steps = [
                step("LIMIT_SETUP", limit_txt, "L'Hôpital's rule"),
                step("CHECK", "substitution", "sin 0 = 0 and x = 0",
                     "indeterminate 0/0"),
                step("DERIV_RULE", "L'Hôpital",
                     "replace with f'(x)/g'(x)"),
                step("POWER_RULE", f"sin({k}x)", f"{k} cos({k}x)"),
                step("POWER_RULE", "x", "1"),
                step("REWRITE", f"lim x→0 of {k} cos({k}x)/1"),
                step("SUBST", "x", 0, f"{k} cos 0 = {k}"),
            ]
            answer = str(k)
        elif variant == "exp_log":
            if random.random() < 0.6:
                k = random.randint(2, 7)
                limit_txt = f"lim x→0 of (e^({k}x) - 1)/x"
                steps = [
                    step("LIMIT_SETUP", limit_txt, "L'Hôpital's rule"),
                    step("CHECK", "substitution",
                         "e^0 - 1 = 0 and x = 0", "indeterminate 0/0"),
                    step("DERIV_RULE", "L'Hôpital",
                         "replace with f'(x)/g'(x)"),
                    step("POWER_RULE", f"e^({k}x) - 1",
                         f"{k}e^({k}x)"),
                    step("POWER_RULE", "x", "1"),
                    step("REWRITE", f"lim x→0 of {k}e^({k}x)"),
                    step("SUBST", "x", 0, f"{k}e^0 = {k}"),
                ]
                answer = str(k)
            else:
                limit_txt = "lim x→1 of ln(x)/(x - 1)"
                steps = [
                    step("LIMIT_SETUP", limit_txt, "L'Hôpital's rule"),
                    step("CHECK", "substitution",
                         "ln 1 = 0 and 1 - 1 = 0",
                         "indeterminate 0/0"),
                    step("DERIV_RULE", "L'Hôpital",
                         "replace with f'(x)/g'(x)"),
                    step("POWER_RULE", "ln(x)", "1/x"),
                    step("POWER_RULE", "x - 1", "1"),
                    step("REWRITE", "lim x→1 of (1/x)/1"),
                    step("SUBST", "x", 1, "1/1 = 1"),
                ]
                answer = "1"
        else:
            k = random.randint(2, 6)
            val = Fraction(k * k, 2)
            limit_txt = f"lim x→0 of (1 - cos({k}x))/x^2"
            steps = [
                step("LIMIT_SETUP", limit_txt, "L'Hôpital's rule"),
                step("CHECK", "substitution",
                     "1 - cos 0 = 0 and 0^2 = 0", "indeterminate 0/0"),
                step("DERIV_RULE", "L'Hôpital",
                     "replace with f'(x)/g'(x)"),
                step("POWER_RULE", f"1 - cos({k}x)",
                     f"{k} sin({k}x)"),
                step("POWER_RULE", "x^2", "2x"),
                step("REWRITE", f"lim x→0 of {k} sin({k}x)/(2x)"),
                step("CHECK", "substitution",
                     f"{k} sin 0 = 0 and 2·0 = 0",
                     "still 0/0 — apply the rule again"),
                step("POWER_RULE", f"{k} sin({k}x)",
                     f"{k * k} cos({k}x)"),
                step("POWER_RULE", "2x", "2"),
                step("REWRITE", f"lim x→0 of {k * k} cos({k}x)/2"),
                step("SUBST", "x", 0, f"{k * k} cos 0/2 = {val}"),
            ]
            answer = str(val)
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"lhopital_{variant}",
            problem=f"Evaluate {limit_txt} using L'Hôpital's rule.",
            steps=steps,
            final_answer=answer,
        )
