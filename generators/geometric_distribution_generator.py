import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


PS = [
    Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5),
    Fraction(2, 5), Fraction(3, 10), Fraction(3, 4), Fraction(7, 10),
    Fraction(1, 6), Fraction(5, 6), Fraction(2, 3), Fraction(3, 5),
    Fraction(4, 5),
]


def exact(fr):
    """Terminating decimal when possible, else the reduced fraction."""
    d = fr.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return dec(fr) if d == 1 else str(fr)


def pow_step(base, exponent):
    value = base ** exponent
    return step("POW", f"({base})^{exponent}", exact(value)), value


class GeometricDistributionGenerator(ProblemGenerator):
    """
    Geometric distribution for the trial number of the first success.
    The scratchpad shows repeated failures followed by success, complement
    rules, tail probabilities, and the expected waiting time.

    Variants:
    - exact_k:   P(X = k) = (1-p)^(k-1)p
    - at_most:   P(X <= k) = 1 - (1-p)^k
    - after_k:   P(X > k) = (1-p)^k
    - mean:      E[X] = 1/p

    Op-codes used:
    - GEOM_SETUP: p, q, and target probability
    - GEOM_FORMULA: first-success probability rule
    - POW / M / S / D (established): exact arithmetic
    - Z: the exact probability or expected trial number
    """

    VARIANTS = ["exact_k", "at_most", "after_k", "mean"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        p = random.choice(PS)
        q = 1 - p

        if variant == "exact_k":
            k = random.randint(2, 8)
            qpow_step, qpow = pow_step(q, k - 1)
            probability = qpow * p
            steps = [
                step("GEOM_SETUP", f"p = {p}, q = {q}", f"P(X = {k})"),
                step("GEOM_FORMULA", "P(X=k) = (1-p)^(k-1) * p"),
                qpow_step,
                step("M", exact(qpow), p, exact(probability)),
                step("Z", exact(probability)),
            ]
            problem = (
                f"A geometric experiment has success probability p = {p}. "
                "Let X be the trial number of the first success. Find "
                f"P(X = {k}). Give an exact answer."
            )
            answer = exact(probability)
        elif variant == "at_most":
            k = random.randint(2, 8)
            qpow_step, qpow = pow_step(q, k)
            probability = 1 - qpow
            steps = [
                step("GEOM_SETUP", f"p = {p}, q = {q}", f"P(X <= {k})"),
                step("GEOM_FORMULA", "P(X <= k) = 1 - (1-p)^k"),
                qpow_step,
                step("S", 1, exact(qpow), exact(probability)),
                step("Z", exact(probability)),
            ]
            problem = (
                f"A geometric experiment has success probability p = {p}. "
                "Let X be the trial number of the first success. Find "
                f"P(X <= {k}). Give an exact answer."
            )
            answer = exact(probability)
        elif variant == "after_k":
            k = random.randint(1, 8)
            qpow_step, probability = pow_step(q, k)
            steps = [
                step("GEOM_SETUP", f"p = {p}, q = {q}", f"P(X > {k})"),
                step("GEOM_FORMULA", "P(X > k) = (1-p)^k"),
                qpow_step,
                step("Z", exact(probability)),
            ]
            problem = (
                f"A geometric experiment has success probability p = {p}. "
                "Let X be the trial number of the first success. Find "
                f"P(X > {k}). Give an exact answer."
            )
            answer = exact(probability)
        else:
            mean = 1 / p
            steps = [
                step("GEOM_SETUP", f"p = {p}", "E[X]"),
                step("GEOM_FORMULA", "E[X] = 1/p"),
                step("D", 1, p, exact(mean)),
                step("Z", exact(mean)),
            ]
            problem = (
                f"A geometric experiment has success probability p = {p}. "
                "Let X be the trial number of the first success. Find the "
                "expected trial number of the first success."
            )
            answer = exact(mean)

        return dict(
            problem_id=jid(),
            operation=f"geometric_distribution_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
