import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.derivative_power_rule_generator import poly_pow, term_pow


class DefiniteIntegralGenerator(ProblemGenerator):
    """
    Definite integrals by the FTC, and average value: antiderivative
    term by term (coefficients divisible so F has integer
    coefficients), F evaluated at both limits with full arithmetic,
    then subtracted; the average-value variant divides by the width.

    Op-codes used:
    - INTEG_SETUP / INTEG_RULE / D / ANTIDERIV / REWRITE (established)
    - SUBST / E / M / A / S / EVAL: endpoint evaluations (established)
    - Z: the exact value
    """

    VARIANTS = ["ftc", "average"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _eval_F(steps, anti, x):
        """Evaluates F (list of (c, n)) at x with explicit steps."""
        wa = f"({x})" if x < 0 else str(x)
        vals = []
        for c, n in anti:
            if n >= 2:
                steps.append(step("E", wa, n, x ** n))
                if c != 1:
                    steps.append(step("M", c, x ** n, c * x ** n))
            elif n == 1:
                steps.append(step("M", c, x, c * x))
            vals.append(c * x ** n)
        acc = vals[0]
        for v in vals[1:]:
            steps.append(step("A", acc, v, acc + v))
            acc += v
        steps.append(step("EVAL", f"F({x})", acc))
        return acc

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        a = random.randint(-2, 2)
        b = a + random.randint(1, 4)
        degs = sorted(random.sample(range(1, 4), 2), reverse=True)
        terms = []
        for n in degs:
            k = random.choice([v for v in range(-3, 4) if v != 0])
            terms.append((k * (n + 1), n))
        f_txt = poly_pow(terms)

        steps = [step("INTEG_SETUP",
                      f"∫ from {a} to {b} of ({f_txt}) dx",
                      "FTC" if variant == "ftc"
                      else "average value = integral/(b - a)"),
                 step("INTEG_RULE", "power rule",
                      "∫ x^n dx = x^(n+1)/(n+1)")]
        anti = []
        for c, n in terms:
            newc = c // (n + 1)
            steps.append(step("D", c, n + 1, newc))
            steps.append(step("ANTIDERIV", term_pow(c, n),
                              term_pow(newc, n + 1)))
            anti.append((newc, n + 1))
        steps.append(step("REWRITE", f"F(x) = {poly_pow(anti)}"))
        Fb = self._eval_F(steps, anti, b)
        Fa = self._eval_F(steps, anti, a)
        integral = Fb - Fa
        steps.append(step("S", Fb, Fa, integral))

        if variant == "ftc":
            answer = str(integral)
            problem = (f"Evaluate ∫ from {a} to {b} of ({f_txt}) dx "
                       f"using the Fundamental Theorem of Calculus.")
        else:
            width = b - a
            avg = Fraction(integral, width)
            steps.append(step("S", b, a, width))
            steps.append(step("D", integral, width, avg))
            answer = str(avg)
            problem = (f"Find the average value of f(x) = {f_txt} on "
                       f"[{a}, {b}].")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"definite_integral_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
