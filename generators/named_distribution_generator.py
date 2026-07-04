import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


EXP_VALUES = {
    1: Fraction(3679, 10000),
    2: Fraction(1353, 10000),
    3: Fraction(4979, 100000),
    4: Fraction(1832, 100000),
}
PHI_VALUES = {
    -2: Fraction(228, 10000),
    -1: Fraction(1587, 10000),
    0: Fraction(1, 2),
    1: Fraction(8413, 10000),
    2: Fraction(9772, 10000),
}


def fraction_text(value):
    return str(Fraction(value))


class NamedDistributionGenerator(ProblemGenerator):
    """
    Poisson, exponential, uniform, and normal distribution arithmetic.

    Lookup/transcendental values are supplied in the problem.

    Op-codes used:
    - DIST_SETUP: distribution, givens, and target
    - LOOKUP_SUPPLIED: supplied table/exponential value
    - FACT: factorial arithmetic
    - E / M / D / S / A (established/shared): exact probability arithmetic
    - Z: requested probability or summary
    """

    VARIANTS = ["poisson", "exponential", "uniform", "normal"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "poisson":
            problem, steps, answer = self._generate_poisson()
        elif variant == "exponential":
            problem, steps, answer = self._generate_exponential()
        elif variant == "uniform":
            problem, steps, answer = self._generate_uniform()
        else:
            problem, steps, answer = self._generate_normal()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"named_distribution_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_poisson(self):
        lam = random.choice(list(EXP_VALUES))
        k = random.randint(0, 5)
        exp_value = EXP_VALUES[lam]
        power = lam ** k
        fact = math.factorial(k)
        numerator = exp_value * power
        probability = numerator / fact
        steps = [
            step("DIST_SETUP", "poisson", f"lambda={lam}", f"k={k}"),
            step("LOOKUP_SUPPLIED", f"e^-{lam}", fraction_text(exp_value)),
            step("E", lam, k, power),
            step("FACT", k, fact),
            step("M", fraction_text(exp_value), power, fraction_text(numerator)),
            step("D", fraction_text(numerator), fact,
                 fraction_text(probability)),
        ]
        answer = f"P(X={k}) = {fraction_text(probability)}"
        problem = (
            f"For X~Poisson(lambda={lam}), use supplied e^-lambda="
            f"{fraction_text(exp_value)} to compute P(X={k})."
        )
        return problem, steps, answer

    def _generate_exponential(self):
        exp_value = Fraction(random.randint(1, 9), random.randint(10, 20))
        if exp_value >= 1:
            exp_value = Fraction(1, 2)
        probability = 1 - exp_value
        steps = [
            step("DIST_SETUP", "exponential", "target=P(X<t)",
                 f"e^(-lambda*t)={fraction_text(exp_value)}"),
            step("LOOKUP_SUPPLIED", "e^(-lambda*t)",
                 fraction_text(exp_value)),
            step("S", 1, fraction_text(exp_value), fraction_text(probability)),
        ]
        answer = f"P(X<t) = {fraction_text(probability)}"
        problem = (
            "For an exponential random variable, use supplied "
            f"e^(-lambda*t)={fraction_text(exp_value)} to compute P(X<t)."
        )
        return problem, steps, answer

    def _generate_uniform(self):
        low = random.randint(-5, 5)
        high = low + random.randint(4, 12)
        left = random.randint(low, high - 1)
        right = random.randint(left + 1, high)
        interval = high - low
        favorable = right - left
        probability = Fraction(favorable, interval)
        mean_num = low + high
        mean = Fraction(mean_num, 2)
        width_sq = interval ** 2
        variance = Fraction(width_sq, 12)
        steps = [
            step("DIST_SETUP", "uniform", f"[{low},{high}]",
                 f"interval=({left},{right})"),
            step("S", high, low, interval),
            step("S", right, left, favorable),
            step("D", favorable, interval, fraction_text(probability)),
            step("A", low, high, mean_num),
            step("D", mean_num, 2, fraction_text(mean)),
            step("E", interval, 2, width_sq),
            step("D", width_sq, 12, fraction_text(variance)),
        ]
        answer = (
            f"P = {fraction_text(probability)}, mean = {fraction_text(mean)}, "
            f"variance = {fraction_text(variance)}"
        )
        problem = (
            f"For X~Uniform({low},{high}), compute P({left}<X<{right}), "
            "mean, and variance."
        )
        return problem, steps, answer

    def _generate_normal(self):
        z = random.choice(list(PHI_VALUES))
        sigma = random.randint(1, 6)
        mu = random.randint(-5, 5)
        x_value = mu + z * sigma
        phi = PHI_VALUES[z]
        diff = x_value - mu
        steps = [
            step("DIST_SETUP", "normal", f"mu={mu},sigma={sigma}",
                 f"x={x_value}"),
            step("S", x_value, mu, diff),
            step("D", diff, sigma, z),
            step("LOOKUP_SUPPLIED", f"Phi({z})", fraction_text(phi)),
        ]
        answer = f"P(X<{x_value}) = {fraction_text(phi)}"
        problem = (
            f"For X~Normal(mu={mu}, sigma={sigma}), compute P(X<{x_value}). "
            f"Use supplied Phi({z})={fraction_text(phi)}."
        )
        return problem, steps, answer
