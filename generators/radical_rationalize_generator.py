import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.radical_multiply_generator import rad, split_square

CORES = [2, 3, 5, 6, 7, 10, 13]


class RadicalRationalizeGenerator(ProblemGenerator):
    """
    Divides radicals and rationalizes denominators.

    Variants:
    - simple:    a/√m — multiply by √m/√m, then reduce the fraction
    - quotient:  √(nk)/√n — quotient rule √a/√b = √(a/b), then simplify
    - conjugate: a/(b + √m) — multiply by the conjugate; the denominator
      collapses via difference of squares (b² − m), then reduce

    Op-codes used:
    - ROOT_SETUP: the expression (string)
    - RATIONALIZE: the rationalizing multiplier (factor over itself)
    - FORM_IDENTIFY: quotient rule / difference of squares (name, formula)
    - M / D / E / S: the arithmetic (established meanings)
    - DIST: distribute over the conjugate numerator (factor, expr, result)
    - SQUARE_FACTOR / ROOT: simplify a leftover radical
    - F: reduce the fraction (from, to)
    - REWRITE: current form (string)
    - Z: final answer (denominator rationalized, fraction reduced)
    """

    VARIANTS = ["simple", "quotient", "conjugate"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        return getattr(self, f"_{variant}")()

    def _simple(self):
        m = random.choice(CORES)
        a = random.randint(2, 12)
        original = f"{a}/√{m}"
        steps = [
            step("ROOT_SETUP", original),
            step("RATIONALIZE", f"√{m}/√{m}"),
            step("M", a, f"√{m}", rad(a, m)),
            step("M", f"√{m}", f"√{m}", str(m)),
            step("REWRITE", f"{rad(a, m)}/{m}"),
        ]
        g = gcd(a, m)
        if g > 1:
            num, den = a // g, m // g
            reduced = rad(num, m) if den == 1 else f"{rad(num, m)}/{den}"
            steps.append(step("F", f"{rad(a, m)}/{m}", reduced))
            answer = reduced
        else:
            answer = f"{rad(a, m)}/{m}"
        steps.append(step("Z", answer))
        return self._pack(original, steps, answer)

    def _quotient(self):
        n = random.choice(CORES)
        k = random.choice([2, 3, 4, 5, 6, 8, 9, 12, 18])
        big = n * k
        original = f"√{big}/√{n}"
        steps = [
            step("ROOT_SETUP", original),
            step("FORM_IDENTIFY", "quotient_of_radicals",
                 "√a/√b = √(a/b)"),
            step("D", big, n, k),
            step("REWRITE", f"√{k}"),
        ]
        s, f = split_square(k)
        if s > 1:
            if f > 1:
                steps.append(step("SQUARE_FACTOR", k, f"{s * s} × {f}",
                                  s * s))
            steps.append(step("ROOT", s * s, s))
            answer = rad(s, f)
            steps.append(step("REWRITE", answer))
        else:
            answer = f"√{k}"
        steps.append(step("Z", answer))
        return self._pack(original, steps, answer)

    def _conjugate(self):
        while True:
            b = random.randint(2, 6)
            m = random.choice([c for c in CORES if c < b * b])
            a = random.randint(2, 9)
            if b * b != m:
                break
        d = b * b - m
        original = f"{a}/({b} + √{m})"
        conj = f"({b} - √{m})"
        steps = [
            step("ROOT_SETUP", original),
            step("RATIONALIZE", f"{conj}/{conj}"),
            step("FORM_IDENTIFY", "difference_of_squares",
                 "(a + b)(a - b) = a^2 - b^2"),
            step("E", b, 2, b * b),
            step("S", b * b, m, d),
            step("DIST", a, f"{b} - √{m}", f"{a * b} - {rad(a, m)}"),
            step("REWRITE", f"({a * b} - {rad(a, m)})/{d}"),
        ]
        g = gcd(gcd(a * b, a), d)
        n1, n2, dr = a * b // g, a // g, d // g
        if dr == 1:
            answer = f"{n1} - {rad(n2, m)}"
        else:
            answer = f"({n1} - {rad(n2, m)})/{dr}"
        if g > 1:
            steps.append(step("F", f"({a * b} - {rad(a, m)})/{d}", answer))
        steps.append(step("Z", answer))
        return self._pack(original, steps, answer)

    @staticmethod
    def _pack(original, steps, answer):
        return dict(
            problem_id=jid(),
            operation="radical_rationalize",
            problem=f"Rationalize the denominator and simplify: {original}",
            steps=steps,
            final_answer=answer,
        )
