import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.integration_by_parts_generator import cm


def xpow(p):
    """x^p with the unit power cleaned up."""
    return "x" if p == 1 else f"x^{p}"


def bpow(p):
    """b^p with the unit power cleaned up."""
    return "b" if p == 1 else f"b^{p}"


class ImproperIntegralGenerator(ProblemGenerator):
    """
    Improper integrals rewritten as limits, integrated, and collapsed
    by sending the bound to its limit. Coefficients are constructed so
    every antiderivative has an integer coefficient; convergent
    answers are exact integers or fractions, divergent ones say so.

    Variants:
    - p_integral: ∫ from a to ∞ of c/x^p dx with p >= 2 -> m/a^(p-1)
    - exponential: ∫ from 0 to ∞ of c·e^(-kx) dx -> c/k (integer)
    - zero_bound: ∫ from 0 to 1 of c/√x or c/x^(2/3) dx (convergent)
    - divergent: c/x or c/√x on [1, ∞), or c/x on (0, 1] -> diverges

    Op-codes used:
    - INTEG_SETUP / LIMIT_SETUP / ANTIDERIV / EVAL / REWRITE /
      FRAC_REDUCE (established)
    - Z: the exact value, or "diverges"
    """

    VARIANTS = ["p_integral", "exponential", "zero_bound", "divergent"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "p_integral":
            a = random.randint(1, 4)
            p = random.randint(2, 4)
            m = random.randint(1, 9)
            c = m * (p - 1)
            pw = p - 1
            den = a ** pw
            val = Fraction(m, den)
            body = f"{c}/{xpow(p)}"
            anti = f"-{m}/{xpow(pw)}"
            at_a = f"-{m}/({a})^{pw}" if pw > 1 else f"-{m}/({a})"
            raw = f"{m}/{den}" if den > 1 else str(m)
            steps = [
                step("INTEG_SETUP", f"∫ from {a} to ∞ of ({body}) dx",
                     "improper integral"),
                step("LIMIT_SETUP",
                     f"lim b→∞ ∫ from {a} to b of ({body}) dx"),
                step("ANTIDERIV", f"{body} dx", anti),
                step("EVAL",
                     f"(-{m}/{bpow(pw)}) - ({at_a}) = "
                     f"{raw} - {m}/{bpow(pw)}"),
            ]
            if str(val) != raw:
                steps.append(step("FRAC_REDUCE", raw, str(val)))
            steps += [
                step("REWRITE", f"lim b→∞ ({val} - {m}/{bpow(pw)})"),
                step("EVAL", f"lim b→∞ {m}/{bpow(pw)} = 0"),
            ]
            answer = str(val)
            problem = (f"Evaluate ∫ from {a} to ∞ of ({body}) dx "
                       f"or state that it diverges.")
        elif variant == "exponential":
            m = random.randint(1, 9)
            k = random.randint(1, 6)
            c = m * k
            kx = "x" if k == 1 else f"{k}x"
            ex = f"e^(-{kx})"
            eb = f"e^(-{'b' if k == 1 else f'{k}b'})"
            body = cm(c, ex)
            steps = [
                step("INTEG_SETUP", f"∫ from 0 to ∞ of ({body}) dx",
                     "improper integral"),
                step("LIMIT_SETUP",
                     f"lim b→∞ ∫ from 0 to b of ({body}) dx"),
                step("ANTIDERIV", f"{body} dx", f"-{cm(m, ex)}"),
                step("EVAL", "e^(0) = 1"),
                step("EVAL",
                     f"(-{cm(m, eb)}) - (-{cm(m, 'e^(0)')}) = "
                     f"{m} - {cm(m, eb)}"),
                step("REWRITE", f"lim b→∞ ({m} - {cm(m, eb)})"),
                step("EVAL", f"lim b→∞ {cm(m, eb)} = 0"),
            ]
            answer = str(m)
            problem = (f"Evaluate ∫ from 0 to ∞ of ({body}) dx "
                       f"or state that it diverges.")
        elif variant == "zero_bound":
            c = random.randint(1, 9)
            form = random.choice(["sqrt", "cbrt"])
            if form == "sqrt":
                body = f"{c}/√x"
                t = 2 * c
                anti = f"{t}√x"
                at_1, at_a = f"{t}√(1)", f"{t}√a"
            else:
                body = f"{c}/x^(2/3)"
                t = 3 * c
                anti = f"{t}x^(1/3)"
                at_1, at_a = f"{t}(1)^(1/3)", f"{t}a^(1/3)"
            steps = [
                step("INTEG_SETUP", f"∫ from 0 to 1 of ({body}) dx",
                     "improper integral"),
                step("LIMIT_SETUP",
                     f"lim a→0+ ∫ from a to 1 of ({body}) dx"),
                step("ANTIDERIV", f"{body} dx", anti),
                step("EVAL", "√(1) = 1" if form == "sqrt"
                     else "(1)^(1/3) = 1"),
                step("EVAL", f"({at_1}) - ({at_a}) = {t} - {at_a}"),
                step("REWRITE", f"lim a→0+ ({t} - {at_a})"),
                step("EVAL", f"lim a→0+ {at_a} = 0"),
            ]
            answer = str(t)
            problem = (f"Evaluate ∫ from 0 to 1 of ({body}) dx "
                       f"or state that it diverges.")
        else:
            c = random.randint(1, 8)
            form = random.choice(["harmonic", "sqrt", "at_zero"])
            if form == "harmonic":
                body = f"{c}/x"
                anti = cm(c, "ln(abs(x))")
                steps = [
                    step("INTEG_SETUP", f"∫ from 1 to ∞ of ({body}) dx",
                         "improper integral"),
                    step("LIMIT_SETUP",
                         f"lim b→∞ ∫ from 1 to b of ({body}) dx"),
                    step("ANTIDERIV", f"{body} dx", anti),
                    step("EVAL", "ln(1) = 0"),
                    step("EVAL",
                         f"({cm(c, 'ln(b)')}) - ({cm(c, 'ln(1)')}) = "
                         f"{cm(c, 'ln(b)')}"),
                    step("EVAL", f"lim b→∞ {cm(c, 'ln(b)')} = ∞"),
                ]
                problem = (f"Evaluate ∫ from 1 to ∞ of ({body}) dx "
                           f"or state that it diverges.")
            elif form == "sqrt":
                body = f"{c}/√x"
                t = 2 * c
                steps = [
                    step("INTEG_SETUP", f"∫ from 1 to ∞ of ({body}) dx",
                         "improper integral"),
                    step("LIMIT_SETUP",
                         f"lim b→∞ ∫ from 1 to b of ({body}) dx"),
                    step("ANTIDERIV", f"{body} dx", f"{t}√x"),
                    step("EVAL", "√(1) = 1"),
                    step("EVAL",
                         f"({t}√b) - ({t}√(1)) = {t}√b - {t}"),
                    step("EVAL", f"lim b→∞ ({t}√b - {t}) = ∞"),
                ]
                problem = (f"Evaluate ∫ from 1 to ∞ of ({body}) dx "
                           f"or state that it diverges.")
            else:
                body = f"{c}/x"
                steps = [
                    step("INTEG_SETUP", f"∫ from 0 to 1 of ({body}) dx",
                         "improper integral"),
                    step("LIMIT_SETUP",
                         f"lim a→0+ ∫ from a to 1 of ({body}) dx"),
                    step("ANTIDERIV", f"{body} dx", cm(c, "ln(abs(x))")),
                    step("EVAL", "ln(1) = 0"),
                    step("EVAL",
                         f"({cm(c, 'ln(1)')}) - ({cm(c, 'ln(a)')}) = "
                         f"-{cm(c, 'ln(a)')}"),
                    step("EVAL", f"lim a→0+ -{cm(c, 'ln(a)')} = ∞"),
                ]
                problem = (f"Evaluate ∫ from 0 to 1 of ({body}) dx "
                           f"or state that it diverges.")
            answer = "diverges"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"improper_integral_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
