import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

# Critical values are supplied in the problem text (Principle 5).
Z_STARS = ["1.28", "1.645", "1.96", "2.05", "2.576"]
# Perfect-square sample sizes, so √n is an integer and σ/√n and
# 0.5/√n terminate.
SQUARE_N = [25, 100, 400]
# Margins whose reciprocal terminates, so (z*·σ/E) stays exact.
MARGINS = ["0.1", "0.25", "0.5", "1", "2", "5"]
# Proportions are bounded in [0, 1], so their margins are small
# (reciprocals 50/40/25/20/10 all terminate).
PROP_MARGINS = ["0.02", "0.025", "0.04", "0.05", "0.1"]


class ConfidenceIntervalGenerator(ProblemGenerator):
    """
    Confidence intervals for a mean or a proportion, margins of error,
    and minimum sample sizes — with the critical value z* given in the
    problem (Principle 5). Sample sizes are perfect squares and the
    margins are chosen so √n is an integer and every quantity is an
    exact terminating decimal.

    Variants:
    - mean_margin: E = z*·σ/√n
    - mean_ci:     x̄ ± E as an interval
    - prop_margin: E = z*·√(p̂(1-p̂)/n) with p̂ = 0.5
    - sample_size_mean: n = ⌈(z*·σ/E)²⌉
    - sample_size_prop: n = ⌈(z*/E)²·p̂(1-p̂)⌉

    Op-codes used:
    - CI_SETUP: the givens and the goal
    - MOE_FORMULA / CI_FORMULA / SAMPLE_SIZE_FORMULA: the formula
    - ROOT / M / D / E / A / S / REWRITE (established)
    - CEIL: round a sample size up to the next whole unit
    - Z: the margin, interval, or sample size
    """

    VARIANTS = ["mean_margin", "mean_ci", "prop_margin",
                "sample_size_mean", "sample_size_prop"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        z = random.choice(Z_STARS)
        zf = Fraction(z)

        if variant in ("mean_margin", "mean_ci"):
            n = random.choice(SQUARE_N)
            root = int(math.isqrt(n))
            sigma = random.randint(2, 30)
            zsig = zf * sigma
            E = zsig / root
            steps = [
                step("CI_SETUP",
                     f"σ = {sigma}, n = {n}, z* = {z}",
                     "margin of error" if variant == "mean_margin"
                     else "confidence interval for μ"),
                step("MOE_FORMULA", "E = z*·σ/√n"),
                step("ROOT", f"√{n}", root),
                step("M", z, sigma, dec(zsig)),
                step("D", dec(zsig), root, dec(E)),
            ]
            if variant == "mean_margin":
                answer = dec(E)
                problem = (f"A sample of size {n} has population "
                           f"standard deviation σ = {sigma}. Using "
                           f"z* = {z}, find the margin of error for a "
                           f"confidence interval for the mean.")
            else:
                xbar = random.randint(20, 200)
                lo, hi = xbar - E, xbar + E
                steps += [
                    step("CI_FORMULA", "x̄ ± E"),
                    step("S", xbar, dec(E), dec(lo)),
                    step("A", xbar, dec(E), dec(hi)),
                    step("REWRITE", f"({dec(lo)}, {dec(hi)})"),
                ]
                answer = f"({dec(lo)}, {dec(hi)})"
                problem = (f"A sample of size {n} has mean x̄ = {xbar} "
                           f"and population standard deviation "
                           f"σ = {sigma}. Using z* = {z}, find the "
                           f"confidence interval for the mean.")
        elif variant == "prop_margin":
            n = random.choice(SQUARE_N)
            root = int(math.isqrt(n))
            phat = Fraction(1, 2)
            pq = phat * (1 - phat)
            se = pq / n
            se_root = Fraction(1, 2) / root
            E = zf * se_root
            steps = [
                step("CI_SETUP", f"p̂ = 0.5, n = {n}, z* = {z}",
                     "margin of error"),
                step("MOE_FORMULA", "E = z*·√(p̂(1-p̂)/n)"),
                step("M", "0.5", "0.5", dec(pq)),
                step("D", dec(pq), n, dec(se)),
                step("ROOT", f"√{dec(se)}", dec(se_root)),
                step("M", z, dec(se_root), dec(E)),
            ]
            answer = dec(E)
            problem = (f"A sample of size {n} has sample proportion "
                       f"p̂ = 0.5. Using z* = {z}, find the margin of "
                       f"error for a confidence interval for the "
                       f"proportion.")
        elif variant == "sample_size_mean":
            sigma = random.randint(2, 30)
            E = random.choice(MARGINS)
            Ef = Fraction(E)
            zsig = zf * sigma
            ratio = zsig / Ef
            sq = ratio * ratio
            n = math.ceil(sq)
            steps = [
                step("CI_SETUP",
                     f"σ = {sigma}, E = {E}, z* = {z}",
                     "minimum sample size for the mean"),
                step("SAMPLE_SIZE_FORMULA", "n = (z*·σ/E)^2"),
                step("M", z, sigma, dec(zsig)),
                step("D", dec(zsig), E, dec(ratio)),
                step("E", dec(ratio), 2, dec(sq)),
                step("CEIL", dec(sq), n),
            ]
            answer = str(n)
            problem = (f"You want a margin of error of {E} for a "
                       f"confidence interval for the mean, with "
                       f"population standard deviation σ = {sigma}. "
                       f"Using z* = {z}, find the minimum sample size.")
        else:
            phat = Fraction(random.choice([2, 3, 4, 5, 6, 7, 8]), 10)
            E = random.choice(PROP_MARGINS)
            Ef = Fraction(E)
            ratio = zf / Ef
            sq = ratio * ratio
            pq = phat * (1 - phat)
            val = sq * pq
            n = math.ceil(val)
            steps = [
                step("CI_SETUP",
                     f"p̂ = {dec(phat)}, E = {E}, z* = {z}",
                     "minimum sample size for the proportion"),
                step("SAMPLE_SIZE_FORMULA", "n = (z*/E)^2·p̂(1-p̂)"),
                step("D", z, E, dec(ratio)),
                step("E", dec(ratio), 2, dec(sq)),
                step("M", dec(phat), dec(1 - phat), dec(pq)),
                step("M", dec(sq), dec(pq), dec(val)),
                step("CEIL", dec(val), n),
            ]
            answer = str(n)
            problem = (f"You want a margin of error of {E} for a "
                       f"confidence interval for a proportion, with "
                       f"estimated p̂ = {dec(phat)}. Using z* = {z}, "
                       f"find the minimum sample size.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"confidence_interval_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
