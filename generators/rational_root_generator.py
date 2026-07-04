import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.polynomial_long_division_generator import poly_txt


def divisors(n):
    n = abs(n)
    return sorted(d for d in range(1, n + 1) if n % d == 0)


class RationalRootGenerator(ProblemGenerator):
    """
    Rational root theorem: list every candidate ±p/q (p dividing the
    constant, q dividing the leading coefficient), then test candidates
    in order of size until one gives P = 0 (A2 trial-and-error).

    The cubic is built as (divisor root factor)·(irreducible quadratic),
    so exactly one rational root exists and every earlier candidate
    honestly rejects.

    Variants:
    - integer_root:  root r with leading coefficient 1 or 2
    - fraction_root: root p/2 (odd p) with leading coefficient 2

    Op-codes used:
    - THEOREM: the rule instantiated with this P (established)
    - CANDIDATES: the full ±p/q list (list)
    - TRY / REJECT / ACCEPT: the sweep (established: candidate, work)
    - Z: 'x = root'
    """

    VARIANTS = ["integer_root", "fraction_root"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _irreducible_quadratic():
        """Monic x^2 + bx + c with no rational roots."""
        while True:
            b = random.randint(-4, 4)
            c = random.choice([v for v in range(-6, 7) if v != 0])
            disc = b * b - 4 * c
            if disc < 0 or math.isqrt(disc) ** 2 != disc:
                return b, c

    def generate(self) -> dict:
        variant = self.variant or \
            random.choice(["integer_root", "integer_root", "fraction_root"])
        var = "x"
        b, c = self._irreducible_quadratic()

        if variant == "integer_root":
            a3 = random.choice([1, 1, 2])
            r = Fraction(random.choice([1, -1, 2, -2, 3, -3]))
            # P = a3(x - r)(x^2 + bx + c)
            coefs = [a3, a3 * (b - r), a3 * (c - r * b), -a3 * r * c]
        else:
            a3 = 2
            r = Fraction(random.choice([1, -1, 3, -3]), 2)
            # P = (2x - 2r)(x^2 + bx + c), 2r odd numerator
            coefs = [2, b * 2 - 2 * r, c * 2 - 2 * r * b, -2 * r * c]
        coefs = [int(v) for v in coefs]
        if 0 in coefs:
            return self.generate()
        poly = poly_txt(coefs, var)

        a0 = coefs[-1]
        cands = set()
        for p in divisors(a0):
            for q in divisors(coefs[0]):
                cands.add(Fraction(p, q))
        ordered = sorted(cands)
        cand_txt = ", ".join(f"±{v}" for v in ordered)
        sweep = sorted({x for v in cands for x in (v, -v)},
                       key=lambda f: (abs(f), f < 0))

        def P(x):
            acc = Fraction(0)
            for co in coefs:
                acc = acc * x + co
            return acc

        assert P(r) == 0
        steps = [
            step("THEOREM", "rational root theorem",
                 f"candidates: ± (divisors of {abs(a0)}) / "
                 f"(divisors of {coefs[0]})"),
            step("CANDIDATES", cand_txt),
        ]
        for cand in sweep:
            val = P(cand)
            steps.append(step("TRY", f"{var} = {cand}",
                              f"P({cand}) = {val}"))
            if val == 0:
                steps.append(step("ACCEPT", f"{var} = {cand}",
                                  f"P({cand}) = 0"))
                break
            steps.append(step("REJECT", f"{var} = {cand}",
                              f"P({cand}) = {val} ≠ 0"))
        answer = f"{var} = {r}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="rational_root_search",
            problem=(f"Use the rational root theorem to find a rational "
                     f"root of P({var}) = {poly}."),
            steps=steps,
            final_answer=answer,
        )
