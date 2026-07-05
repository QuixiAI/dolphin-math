import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.domain_range_generator import lin


class USubstitutionGenerator(ProblemGenerator):
    """
    u-substitution with the du bookkeeping written out: name u, state
    du, trade the dx for du (with the constant adjustment), integrate
    in u, then substitute back. Coefficients are constructed so every
    constant stays an integer.

    Variants:
    - power_form: ∫ c(ax + b)^n dx
    - poly_inner: ∫ cx(x² + k)^n dx
    - exp_inner:  ∫ cx·e^(x²) dx
    - log_form:   ∫ c(2x + b)/(x² + bx + k) dx -> c·ln(abs(...))

    Op-codes used:
    - INTEG_SETUP / INTEG_RULE / ANTIDERIV / D (established)
    - SUBST: u = inner, and the back-substitution (established)
    - REWRITE: the du trade and the u-integral (established)
    - Z: F(x) + C
    """

    VARIANTS = ["power_form", "poly_inner", "exp_inner", "log_form"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "power_form":
            a = random.choice([2, 3, 4])
            b = random.choice([v for v in range(-6, 7) if v != 0])
            n = random.randint(2, 4)
            mult = random.choice([1, 2, 3])
            c = a * (n + 1) * mult
            inner = lin(a, b, "x")
            newc = c // (a * (n + 1))
            res_head = "" if newc == 1 else str(newc)
            F = f"{res_head}({inner})^{n + 1}"
            steps = [
                step("INTEG_SETUP", f"∫ {c}({inner})^{n} dx",
                     "u-substitution"),
                step("SUBST", "u", inner, f"du = {a} dx"),
                step("REWRITE", f"{c} dx = {c // a} du"),
                step("REWRITE", f"∫ {c // a}u^{n} du"),
                step("INTEG_RULE", "power rule",
                     "∫ u^n du = u^(n+1)/(n+1) + C"),
                step("D", c // a, n + 1, newc),
                step("ANTIDERIV", f"{c // a}u^{n}",
                     f"{res_head}u^{n + 1}"),
                step("SUBST", "u", inner, F),
            ]
            answer = f"{F} + C"
            problem = f"Find ∫ {c}({inner})^{n} dx."
        elif variant == "poly_inner":
            k = random.choice([v for v in range(-6, 7) if v != 0])
            n = random.randint(2, 4)
            mult = random.choice([1, 2])
            c = 2 * (n + 1) * mult
            inner = f"x^2 {'+' if k > 0 else '-'} {abs(k)}"
            newc = c // (2 * (n + 1))
            res_head = "" if newc == 1 else str(newc)
            F = f"{res_head}({inner})^{n + 1}"
            steps = [
                step("INTEG_SETUP", f"∫ {c}x({inner})^{n} dx",
                     "u-substitution"),
                step("SUBST", "u", inner, "du = 2x dx"),
                step("REWRITE", f"{c}x dx = {c // 2} du"),
                step("REWRITE", f"∫ {c // 2}u^{n} du"),
                step("INTEG_RULE", "power rule",
                     "∫ u^n du = u^(n+1)/(n+1) + C"),
                step("D", c // 2, n + 1, newc),
                step("ANTIDERIV", f"{c // 2}u^{n}",
                     f"{res_head}u^{n + 1}"),
                step("SUBST", "u", inner, F),
            ]
            answer = f"{F} + C"
            problem = f"Find ∫ {c}x({inner})^{n} dx."
        elif variant == "exp_inner":
            c = 2 * random.choice([v for v in range(-4, 5) if v != 0])
            newc = c // 2
            res_head = "" if newc == 1 else \
                ("-" if newc == -1 else str(newc))
            F = f"{res_head}e^(x^2)"
            steps = [
                step("INTEG_SETUP", f"∫ {c}x e^(x^2) dx",
                     "u-substitution"),
                step("SUBST", "u", "x^2", "du = 2x dx"),
                step("REWRITE", f"{c}x dx = {newc} du"),
                step("REWRITE", f"∫ {res_head}e^u du"),
                step("INTEG_RULE", "exponential rule",
                     "∫ e^u du = e^u + C"),
                step("ANTIDERIV", f"{res_head}e^u",
                     f"{res_head}e^u"),
                step("SUBST", "u", "x^2", F),
            ]
            answer = f"{F} + C"
            problem = f"Find ∫ {c}x e^(x^2) dx."
        else:
            b = random.choice([2, 4, 6])
            k = random.randint(b, b + 8)  # keep x²+bx+k positive-ish
            c = random.choice([1, 2, 3, 5])
            den = f"x^2 + {b}x + {k}"
            num = f"{2}x + {b}" if c == 1 else f"{c}(2x + {b})"
            res_head = "" if c == 1 else str(c)
            F = f"{res_head} ln(abs({den}))".strip()
            steps = [
                step("INTEG_SETUP", f"∫ ({num})/({den}) dx",
                     "u-substitution"),
                step("SUBST", "u", den, f"du = (2x + {b}) dx"),
                step("REWRITE", f"∫ {c}/u du" if c > 1
                     else "∫ 1/u du"),
                step("INTEG_RULE", "log rule",
                     "∫ (1/u) du = ln(abs(u)) + C"),
                step("ANTIDERIV", f"{c}/u" if c > 1 else "1/u",
                     f"{res_head} ln(abs(u))".strip()),
                step("SUBST", "u", den, F),
            ]
            answer = f"{F} + C"
            problem = f"Find ∫ ({num})/({den}) dx."
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"u_substitution_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
