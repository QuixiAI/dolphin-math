import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.domain_range_generator import lin


def cmul(c, body):
    """c·body with unit coefficients hidden: '5 sin(3x)', '-e^(2x)',
    '-4·5^x' (explicit dot before a numeric base)."""
    if c == 1:
        return body
    if c == -1:
        return f"-{body}"
    if body[0].isdigit():
        return f"{c}·{body}"
    return f"{c} {body}" if body[0].isalpha() else f"{c}{body}"


class DerivativeTranscendentalGenerator(ProblemGenerator):
    """
    Derivatives of trig, exponential, and logarithmic functions with a
    linear inner function, the chain factor shown every time.

    Variants:
    - trig: c·sin(kx), c·cos(kx), c·tan(kx)
    - exp:  c·e^(kx), and c·a^x with the ln a factor
    - log:  c·ln(kx) — where the k cancels to c/x — and c·ln(ax + b)

    Op-codes used:
    - DERIV_SETUP / DERIV_RULE / POWER_RULE / M / CANCEL / REWRITE
      (established)
    - Z: the derivative
    """

    VARIANTS = ["trig", "exp", "log"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        c = random.choice([v for v in range(-6, 7) if v != 0])
        k = random.choice([2, 3, 4, 5])

        if variant == "trig":
            fn = random.choice(["sin", "cos", "tan"])
            y = cmul(c, f"{fn}({k}x)")
            rules = {"sin": ("d/dx sin(u) = cos(u)·u'", "cos"),
                     "cos": ("d/dx cos(u) = -sin(u)·u'", "sin"),
                     "tan": ("d/dx tan(u) = sec^2(u)·u'", "sec^2")}
            rule, dfn = rules[fn]
            out_c = c * k if fn != "cos" else -c * k
            answer = f"y' = {cmul(out_c, f'{dfn}({k}x)')}"
            steps = [
                step("DERIV_SETUP", f"y = {y}", "y'"),
                step("DERIV_RULE", rule, f"u = {k}x"),
                step("POWER_RULE", f"{k}x", str(k)),
                step("M", c if fn != "cos" else -c, k, out_c),
                step("REWRITE", answer),
            ]
        elif variant == "exp":
            if random.random() < 0.6:
                y = cmul(c, f"e^({k}x)")
                out_c = c * k
                answer = f"y' = {cmul(out_c, f'e^({k}x)')}"
                steps = [
                    step("DERIV_SETUP", f"y = {y}", "y'"),
                    step("DERIV_RULE", "d/dx e^u = e^u·u'",
                         f"u = {k}x"),
                    step("POWER_RULE", f"{k}x", str(k)),
                    step("M", c, k, out_c),
                    step("REWRITE", answer),
                ]
            else:
                base = random.choice([2, 3, 5, 10])
                y = cmul(c, f"{base}^x")
                answer = (f"y' = {cmul(c, f'{base}^x')} ln {base}")
                steps = [
                    step("DERIV_SETUP", f"y = {y}", "y'"),
                    step("DERIV_RULE",
                         "d/dx a^x = a^x ln a", f"a = {base}"),
                    step("REWRITE", answer),
                ]
        else:
            if random.random() < 0.5:
                y = cmul(c, f"ln({k}x)")
                answer = f"y' = {c}/x" if c != 1 else "y' = 1/x"
                steps = [
                    step("DERIV_SETUP", f"y = {y}", "y'"),
                    step("DERIV_RULE", "d/dx ln(u) = u'/u",
                         f"u = {k}x"),
                    step("POWER_RULE", f"{k}x", str(k)),
                    step("REWRITE",
                         f"y' = {cmul(c, f'{k}/({k}x)')}"),
                    step("CANCEL", str(k),
                         f"{c}/x" if c != 1 else "1/x"),
                    step("REWRITE", answer),
                ]
            else:
                a = random.choice([2, 3, 4, 5])
                b = random.choice([v for v in range(-8, 9) if v != 0])
                inner = lin(a, b, "x")
                y = cmul(c, f"ln({inner})")
                num = c * a
                answer = f"y' = {num}/({inner})"
                steps = [
                    step("DERIV_SETUP", f"y = {y}", "y'"),
                    step("DERIV_RULE", "d/dx ln(u) = u'/u",
                         f"u = {inner}"),
                    step("POWER_RULE", inner, str(a)),
                    step("M", c, a, num),
                    step("REWRITE", answer),
                ]
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"derivative_transcendental_{variant}",
            problem=f"Differentiate y = {y}.",
            steps=steps,
            final_answer=answer,
        )
