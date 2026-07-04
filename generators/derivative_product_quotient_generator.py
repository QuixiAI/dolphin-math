import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.domain_range_generator import lin
from generators.derivative_power_rule_generator import poly_pow


class DerivativeProductQuotientGenerator(ProblemGenerator):
    """
    Product and quotient rules with the expansion and combination
    worked out.

    Variants:
    - product:  y = (x² + p)(cx + d) -> f'g + fg', both distributions
                shown, like terms combined
    - quotient: y = (ax + b)/(cx + d) -> (f'g - fg')/g²; the x-terms
                cancel and the answer collapses to (ad - bc)/(cx + d)²

    Op-codes used:
    - DERIV_SETUP / DERIV_RULE / POWER_RULE (established)
    - REWRITE / DIST (established)
    - COMB_X / COMB_CONST: combining like terms (established)
    - Z: the simplified derivative
    """

    VARIANTS = ["product", "quotient"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "product":
            p = random.choice([v for v in range(-6, 7) if v != 0])
            c = random.choice([v for v in range(-4, 5)
                               if v not in (-1, 0, 1)])
            d = random.choice([v for v in range(-6, 7) if v != 0])
            f_txt = f"(x^2 {'+' if p > 0 else '-'} {abs(p)})"
            g_txt = f"({lin(c, d, 'x')})"
            # y' = 2x(cx+d) + c(x^2+p) = 3c x^2 + 2d x + c p
            a2, a1, a0 = 3 * c, 2 * d, c * p
            deriv = poly_pow([(a2, 2), (a1, 1), (a0, 0)])
            dist1 = poly_pow([(2 * c, 2), (2 * d, 1)])
            dist2 = poly_pow([(c, 2), (c * p, 0)])
            steps = [
                step("DERIV_SETUP", f"y = {f_txt}{g_txt}", "y'"),
                step("DERIV_RULE", "product rule",
                     "(fg)' = f'g + fg'"),
                step("POWER_RULE", f_txt, "2x"),
                step("POWER_RULE", g_txt, str(c)),
                step("REWRITE", f"y' = 2x{g_txt} + {c}{f_txt}"),
                step("DIST", "2x", g_txt.strip("()"), dist1),
                step("DIST", c, f_txt.strip("()"), dist2),
                step("COMB_X", f"{2 * c}x^2", f"{c}x^2", f"{a2}x^2"),
            ]
            answer = f"y' = {deriv}"
            steps.append(step("REWRITE", answer))
            problem = f"Differentiate y = {f_txt}{g_txt}."
        else:
            while True:
                a = random.choice([v for v in range(-4, 5) if v != 0])
                b = random.choice([v for v in range(-6, 7) if v != 0])
                c = random.choice([v for v in range(-4, 5) if v != 0])
                d = random.choice([v for v in range(-6, 7) if v != 0])
                if a * d - b * c != 0:
                    break
            k = a * d - b * c
            f_txt = lin(a, b, "x")
            g_txt = lin(c, d, "x")
            num1 = poly_pow([(a * c, 1), (a * d, 0)])
            num2 = poly_pow([(-a * c, 1), (-b * c, 0)])
            answer_body = f"{k}/({g_txt})^2"
            steps = [
                step("DERIV_SETUP", f"y = ({f_txt})/({g_txt})", "y'"),
                step("DERIV_RULE", "quotient rule",
                     "(f/g)' = (f'g - fg')/g^2"),
                step("POWER_RULE", f"({f_txt})", str(a)),
                step("POWER_RULE", f"({g_txt})", str(c)),
                step("REWRITE",
                     f"y' = ("
                     f"{'' if a == 1 else '-' if a == -1 else a}"
                     f"({g_txt}) - "
                     f"{'' if c == 1 else '-' if c == -1 else c}"
                     f"({f_txt}))/({g_txt})^2"),
                step("DIST", a, g_txt, num1),
                step("DIST", -c, f_txt, num2),
                step("COMB_X", f"{a * c}x", f"{-a * c}x", "0"),
                step("COMB_CONST", a * d, -b * c, k),
            ]
            answer = f"y' = {answer_body}"
            steps.append(step("REWRITE", answer))
            problem = f"Differentiate y = ({f_txt})/({g_txt})."
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"derivative_{variant}_rule",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
