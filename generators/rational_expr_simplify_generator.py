import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.factor_trinomial_generator import binomial, pair_search, xterm


def trinomial_txt(var, b, c):
    """'x^2 - x - 6' from coefficients."""
    c_txt = f"+ {c}" if c > 0 else f"- {-c}"
    return f"{var}^2 {xterm(b, var)} {c_txt}"


class RationalExprSimplifyGenerator(ProblemGenerator):
    """
    Simplifies rational expressions by factoring and cancelling. The full
    factor-pair trial-and-error runs for every trinomial — numerator and
    denominator alike — then the shared factor cancels.

    Variants:
    - over_binomial:  (x² + bx + c)/(x + d), the binomial divides the top
    - two_trinomials: both factor; exactly one common factor cancels
    - gcf_monomial:   (Ax² + Bx)/(gx) — GCF factoring, monomial cancel

    Op-codes used:
    - POLY_SETUP / REWRITE / FACTOR_PAIR_GOAL / TRY / REJECT / ACCEPT
    - GCF_COEFF / GCF_VAR / GCF_RESULT (gcf variant)
    - CANCEL: cancel the common factor (factor, result)
    - Z: final answer
    """

    VARIANTS = ["over_binomial", "two_trinomials", "gcf_monomial"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _roots():
        """Two distinct nonzero roots with nonzero sum (pair_search needs
        b ≠ 0 and c ≠ 0)."""
        while True:
            p = random.choice([v for v in range(-8, 9) if v != 0])
            q = random.choice([v for v in range(-8, 9) if v != 0])
            if p != q and p + q != 0:
                return p, q

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        var = random.choice(["x", "x", "x", "y", "n"])

        if variant == "gcf_monomial":
            g = random.randint(2, 6)
            while True:
                a = random.randint(2, 9)
                b = random.choice([v for v in range(-9, 10) if v != 0])
                if gcd(a, abs(b)) == 1:
                    break
            A, B = g * a, g * b
            num = f"{A}{var}^2 {xterm(B, var)}"
            den = f"{g}{var}"
            original = f"({num})/({den})"
            inner = f"{a}{var} + {b}" if b > 0 else f"{a}{var} - {-b}"
            steps = [
                step("POLY_SETUP", original),
                step("GCF_COEFF", f"{A}, {abs(B)}", g),
                step("GCF_VAR", f"{var}^2, {var}", var),
                step("GCF_RESULT", f"{g}{var}"),
                step("REWRITE", f"({g}{var}({inner}))/({g}{var})"),
                step("CANCEL", f"{g}{var}", inner),
                step("Z", inner),
            ]
            return self._pack(original, steps, inner)

        p, q = self._roots()
        b_n, c_n = -(p + q), p * q
        num = trinomial_txt(var, b_n, c_n)
        fn1, fn2 = binomial(var, -p), binomial(var, -q)

        if variant == "over_binomial":
            den = binomial(var, -p).strip("()")
            original = f"({num})/({den})"
            answer = binomial(var, -q).strip("()")
            steps = [step("POLY_SETUP", original)]
            pair_search(steps, c_n, b_n)
            steps.append(step("REWRITE", f"({fn1}{fn2})/({den})"))
            steps.append(step("CANCEL", fn1, answer))
            steps.append(step("Z", answer))
            return self._pack(original, steps, answer)

        # two_trinomials: shared root p; other roots q (top) and r (bottom)
        while True:
            r = random.choice([v for v in range(-8, 9) if v != 0])
            if r not in (p, q) and p + r != 0:
                break
        b_d, c_d = -(p + r), p * r
        den = trinomial_txt(var, b_d, c_d)
        fd2 = binomial(var, -r)
        original = f"({num})/({den})"
        answer = f"{fn2}/{fd2}"

        steps = [step("POLY_SETUP", original)]
        pair_search(steps, c_n, b_n)
        steps.append(step("REWRITE", f"({fn1}{fn2})/({den})"))
        pair_search(steps, c_d, b_d)
        steps.append(step("REWRITE", f"({fn1}{fn2})/({fn1}{fd2})"))
        steps.append(step("CANCEL", fn1, answer))
        steps.append(step("Z", answer))
        return self._pack(original, steps, answer)

    @staticmethod
    def _pack(original, steps, answer):
        return dict(
            problem_id=jid(),
            operation="rational_expr_simplify",
            problem=f"Simplify: {original}",
            steps=steps,
            final_answer=answer,
        )
