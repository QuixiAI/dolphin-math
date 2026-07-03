import random
from math import gcd, lcm

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.factor_trinomial_generator import binomial
from generators.special_solution_equation_generator import lin


class RationalExprAddSubGenerator(ProblemGenerator):
    """
    Adds and subtracts rational expressions.

    Variants:
    - like:     a/(x+d) ± b/(x+d) — combine numerators over the shared
      denominator
    - monomial: a/(mx) ± b/(nx) — numeric LCD with the classic L/C fraction
      vocabulary, then reduce
    - binomial: a/(x+p) ± b/(x+q) — LCD is the product; cross-distribute,
      combine like terms

    Op-codes used:
    - POLY_SETUP / FORM_IDENTIFY / REWRITE (established)
    - L: lcm of the numeric denominators (m, n, lcm)
    - C: convert one fraction to the LCD (fraction, multiplier, result)
    - DIST: distribute a numerator over a binomial (factor, expr, result)
    - COMB_X / COMB_CONST: combine the linear numerator (t1, t2, result)
    - A / S: combine numeric numerators (a, b, result)
    - F: reduce the result (from, to)
    - Z: final answer
    """

    VARIANTS = ["like", "monomial", "binomial"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        var = random.choice(["x", "x", "x", "y", "n"])
        plus = random.random() < 0.5
        sign = "+" if plus else "-"

        if variant == "like":
            d = random.choice([v for v in range(-8, 9) if v != 0])
            while True:
                a, b = random.randint(1, 12), random.randint(1, 12)
                if (a + b if plus else a - b) != 0:
                    break
            den = binomial(var, d).strip("()")
            total = a + b if plus else a - b
            original = f"{a}/({den}) {sign} {b}/({den})"
            answer = f"{total}/({den})"
            steps = [
                step("POLY_SETUP", original),
                step("FORM_IDENTIFY", "like_denominators",
                     "a/c ± b/c = (a ± b)/c"),
                step("A" if plus else "S", a, b, total),
                step("Z", answer),
            ]
            return self._pack(original, steps, answer)

        if variant == "monomial":
            while True:
                m, n = random.randint(2, 9), random.randint(2, 9)
                a, b = random.randint(1, 9), random.randint(1, 9)
                if m == n:
                    continue
                L = lcm(m, n)
                k1, k2 = L // m, L // n
                total = a * k1 + b * k2 if plus else a * k1 - b * k2
                if total != 0:
                    break
            original = f"{a}/({m}{var}) {sign} {b}/({n}{var})"
            steps = [
                step("POLY_SETUP", original),
                step("L", m, n, L),
                step("C", f"{a}/{m}{var}", k1, f"{a * k1}/{L}{var}"),
                step("C", f"{b}/{n}{var}", k2, f"{b * k2}/{L}{var}"),
                step("A" if plus else "S", a * k1, b * k2, total),
                step("REWRITE", f"{total}/({L}{var})"),
            ]
            g = gcd(abs(total), L)
            num, den_c = total // g, L // g
            den_txt = var if den_c == 1 else f"{den_c}{var}"
            answer = f"{num}/({den_txt})"
            if g > 1:
                steps.append(step("F", f"{total}/({L}{var})", answer))
            steps.append(step("Z", answer))
            return self._pack(original, steps, answer)

        # binomial denominators
        while True:
            p, q = random.sample([v for v in range(-7, 8) if v != 0], 2)
            a, b = random.randint(1, 9), random.randint(1, 9)
            x_coef = a + b if plus else a - b
            const = a * q + b * p if plus else a * q - b * p
            if x_coef != 0 and const != 0:
                break
        fp, fq = binomial(var, p), binomial(var, q)
        original = (f"{a}/{fp} {sign} {b}/{fq}")
        lcd = f"{fp}{fq}"
        num_lin = lin(x_coef, const, var)
        answer = f"({num_lin})/({lcd})"
        steps = [
            step("POLY_SETUP", original),
            step("FORM_IDENTIFY", "unlike_denominators",
                 f"LCD = {lcd}"),
            step("C", f"{a}/{fp}", fq.strip("()"),
                 f"{a}({fq.strip('()')})/({lcd})"),
            step("C", f"{b}/{fq}", fp.strip("()"),
                 f"{b}({fp.strip('()')})/({lcd})"),
            step("DIST", a, fq.strip("()"), lin(a, a * q, var)),
            step("DIST", b, fp.strip("()"), lin(b, b * p, var)),
            step("COMB_X", f"{a}{var}", f"{sign}{b}{var}",
                 f"{x_coef}{var}"),
            step("COMB_CONST", a * q, b * p if plus else -b * p, const),
            step("REWRITE", answer),
            step("Z", answer),
        ]
        return self._pack(original, steps, answer)

    @staticmethod
    def _pack(original, steps, answer):
        return dict(
            problem_id=jid(),
            operation="rational_expr_add_sub",
            problem=f"Simplify: {original}",
            steps=steps,
            final_answer=answer,
        )
