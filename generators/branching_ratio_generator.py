import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


CHANNELS = ["a", "b", "c"]


def fraction_text(value):
    return str(Fraction(value))


class BranchingRatioGenerator(ProblemGenerator):
    """
    Particle partial widths, branching ratios, and lifetimes.

    Widths and hbar are supplied as exact numbers. Branching ratios and
    lifetimes are reduced fractions.

    Op-codes used:
    - WIDTH_SETUP: givens and requested quantity
    - A / D (established/shared): total widths and exact divisions
    - Z: requested BR and/or lifetime
    """

    VARIANTS = ["branching_ratio", "lifetime", "combined"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "branching_ratio":
            problem, steps, answer = self._generate_branching_ratio()
        elif variant == "lifetime":
            problem, steps, answer = self._generate_lifetime()
        else:
            problem, steps, answer = self._generate_combined()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"branching_ratio_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _random_widths(self):
        return {name: random.randint(1, 20) for name in CHANNELS}

    def _total_steps(self, steps, widths):
        sum_ab = widths["a"] + widths["b"]
        total = sum_ab + widths["c"]
        steps.append(step("A", widths["a"], widths["b"], sum_ab))
        steps.append(step("A", sum_ab, widths["c"], total))
        return total

    def _widths_text(self, widths, final_and=True):
        middle = f"Gamma_a={widths['a']}, Gamma_b={widths['b']}"
        if final_and:
            return f"{middle}, and Gamma_c={widths['c']}"
        return f"{middle}, Gamma_c={widths['c']}"

    def _generate_branching_ratio(self):
        widths = self._random_widths()
        channel = random.choice(CHANNELS)
        steps = [
            step("WIDTH_SETUP", "branching_ratio",
                 self._widths_text(widths, final_and=False),
                 f"target=BR_{channel}"),
        ]
        total = self._total_steps(steps, widths)
        br = Fraction(widths[channel], total)
        steps.append(step("D", widths[channel], total, fraction_text(br)))
        answer = f"BR_{channel} = {fraction_text(br)}"
        problem = (
            f"A particle has partial widths {self._widths_text(widths)}. "
            f"Compute the branching ratio BR_{channel}=Gamma_{channel}/"
            "Gamma_total."
        )
        return problem, steps, answer

    def _generate_lifetime(self):
        hbar = random.randint(1, 20)
        gamma = random.randint(1, 30)
        lifetime = Fraction(hbar, gamma)
        steps = [
            step("WIDTH_SETUP", "lifetime", f"hbar={hbar}",
                 f"Gamma={gamma}"),
            step("D", hbar, gamma, fraction_text(lifetime)),
        ]
        answer = f"tau = {fraction_text(lifetime)}"
        problem = (
            f"Given hbar={hbar} and total width Gamma={gamma}, compute "
            "the lifetime tau=hbar/Gamma."
        )
        return problem, steps, answer

    def _generate_combined(self):
        widths = self._random_widths()
        hbar = random.randint(1, 20)
        channel = random.choice(CHANNELS)
        steps = [
            step("WIDTH_SETUP", "combined",
                 f"{self._widths_text(widths, final_and=False)},hbar={hbar}",
                 f"target=BR_{channel},tau"),
        ]
        total = self._total_steps(steps, widths)
        br = Fraction(widths[channel], total)
        lifetime = Fraction(hbar, total)
        steps.append(step("D", widths[channel], total, fraction_text(br)))
        steps.append(step("D", hbar, total, fraction_text(lifetime)))
        answer = (
            f"Gamma_total = {total}, BR_{channel} = {fraction_text(br)}, "
            f"tau = {fraction_text(lifetime)}"
        )
        problem = (
            f"A particle has partial widths "
            f"{self._widths_text(widths, final_and=False)} and hbar={hbar}. "
            f"Compute Gamma_total, BR_{channel}=Gamma_{channel}/"
            "Gamma_total, and tau=hbar/Gamma_total."
        )
        return problem, steps, answer
