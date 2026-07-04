import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.polynomial_long_division_generator import poly_txt


def lin_h(coef_x, coef_h, const):
    """Renders like '6xh + 3h^2 - 2h' pieces assembled sign-aware."""
    parts = []
    for c, sym in ((coef_x, "xh"), (coef_h, "h^2"), (const, "h")):
        if c == 0:
            continue
        mag = "" if abs(c) == 1 else str(abs(c))
        if not parts:
            parts.append(f"{'-' if c < 0 else ''}{mag}{sym}")
        else:
            parts.append(f"{'+' if c > 0 else '-'} {mag}{sym}")
    return " ".join(parts)


class DerivativeLimitDefGenerator(ProblemGenerator):
    """
    The limit definition of the derivative, worked in full: substitute
    x + h, expand the square, subtract f(x) (watching the constant and
    x² terms cancel), factor h out of every surviving term, cancel it,
    and send h to 0.

    Variants:
    - general:  f(x) = ax² + bx + c -> f'(x) as an expression
    - at_point: the same computation with a number in place of x

    Op-codes used:
    - LIMIT_SETUP: the function and the definition (established)
    - SUBST / DIST / REWRITE / FACTOR_GROUP / CANCEL (established)
    - E / M / A / S: numeric work in the at_point variant (established)
    - Z: 'f'(x) = ...' or 'f'(a) = ...'
    """

    VARIANTS = ["general", "at_point"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        a = random.choice([v for v in range(-4, 5) if v != 0])
        b = random.choice([v for v in range(-6, 7) if v != 0])
        c = random.randint(-6, 6)
        f_txt = poly_txt([a, b, c], "x")

        if variant == "general":
            deriv = poly_txt([2 * a, b], "x")
            answer = f"f'(x) = {deriv}"
            am = "" if abs(a) == 1 else str(abs(a))
            group = (f"({2 * a}x " +
                     f"{'+' if a > 0 else '-'} {am}h " +
                     (f"+ {b})" if b > 0 else f"- {-b})"))
            a2 = 2 * a
            dist_txt = (f"{'' if a == 1 else '-' if a == -1 else a}x^2 "
                        f"{'+' if a2 > 0 else '-'} {abs(a2)}xh "
                        f"{'+' if a > 0 else '-'} {am}h^2")
            steps = [
                step("LIMIT_SETUP",
                     f"f(x) = {f_txt}; f'(x) = lim h→0 "
                     f"(f(x+h) - f(x))/h", "expand and simplify"),
                step("SUBST", "x", "x + h",
                     f"{'' if a == 1 else '-' if a == -1 else a}"
                     f"(x + h)^2 "
                     f"{'+' if b > 0 else '-'} "
                     f"{'' if abs(b) == 1 else abs(b)}(x + h)" +
                     (f" {'+' if c > 0 else '-'} {abs(c)}" if c else "")),
                step("REWRITE", "(x + h)^2 = x^2 + 2xh + h^2"),
                step("DIST", a, "x^2 + 2xh + h^2", dist_txt),
                step("REWRITE",
                     f"f(x+h) - f(x) = {lin_h(2 * a, a, b)} "
                     f"(the x^2, x, and constant terms cancel)"),
                step("FACTOR_GROUP", lin_h(2 * a, a, b), "h", group),
                step("CANCEL", "h", group[1:-1]),
                step("SUBST", "h", 0,
                     group[1:-1].replace("h", "(0)")),
                step("REWRITE", deriv),
            ]
            problem = (f"Use the limit definition of the derivative to "
                       f"find f'(x) for f(x) = {f_txt}.")
            op = "derivative_limit_general"
        else:
            p = random.randint(-4, 4)
            fp = a * p * p + b * p + c
            dcoef = 2 * a * p + b       # h coefficient after expansion
            deriv_val = dcoef
            am = "" if abs(a) == 1 else str(abs(a))
            group = f"({dcoef} {'+' if a > 0 else '-'} {am}h)"
            steps = [
                step("LIMIT_SETUP",
                     f"f(x) = {f_txt}; f'({p}) = lim h→0 "
                     f"(f({p}+h) - f({p}))/h", "expand and simplify"),
                step("E", f"({p})" if p < 0 else str(p), 2, p * p),
                step("M", a, p * p, a * p * p),
                step("M", b, p, b * p),
                step("A", a * p * p + b * p, c, fp),
                step("EVAL", f"f({p})", fp),
                step("SUBST", "x", f"{p} + h",
                     f"{'' if a == 1 else '-' if a == -1 else a}"
                     f"({p} + h)^2 "
                     f"{'+' if b > 0 else '-'} "
                     f"{'' if abs(b) == 1 else abs(b)}({p} + h)" +
                     (f" {'+' if c > 0 else '-'} {abs(c)}" if c else "")),
                step("REWRITE",
                     f"f({p}+h) - f({p}) = "
                     f"{lin_h(0, a, dcoef).replace('xh', 'h')}"),
                step("FACTOR_GROUP",
                     lin_h(0, a, dcoef).replace('xh', 'h'), "h",
                     group),
                step("CANCEL", "h", group[1:-1]),
                step("SUBST", "h", 0,
                     f"{dcoef} {'+' if a > 0 else '-'} "
                     f"{'' if abs(a) == 1 else abs(a)}(0)"),
                step("A", dcoef, 0, dcoef),
            ]
            answer = f"f'({p}) = {deriv_val}"
            steps.append(step("REWRITE", answer))
            problem = (f"Use the limit definition of the derivative to "
                       f"find f'({p}) for f(x) = {f_txt}.")
            op = "derivative_limit_at_point"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
