import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class PartitionFunctionGenerator(ProblemGenerator):
    """
    Two-level partition functions with supplied Boltzmann factors.

    Variants:
    - two_level: nondegenerate ground and excited levels
    - degenerate_two_level: include level degeneracies

    Op-codes used:
    - PARTITION_SETUP: energies, degeneracies, and supplied Boltzmann factor
    - PARTITION_FORMULA: partition function or expectation relation
    - A / M / D (established/shared): exact probability arithmetic
    - Z: partition function, occupancy, and mean energy
    """

    VARIANTS = ["two_level", "degenerate_two_level"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "two_level":
            return self._generate_two_level(1, 1, variant)
        while True:
            g0 = random.randint(1, 5)
            g1 = random.randint(1, 5)
            if (g0, g1) != (1, 1):
                break
        return self._generate_two_level(g0, g1, variant)

    def _generate_two_level(self, g0, g1, variant):
        epsilon = random.randint(1, 20)
        boltzmann = Fraction(1, random.randint(2, 12))
        excited_weight = g1 * boltzmann
        partition = Fraction(g0) + excited_weight
        p_ground = Fraction(g0, 1) / partition
        p_excited = excited_weight / partition
        mean_energy = epsilon * p_excited
        steps = [
            step("PARTITION_SETUP", variant,
                 f"g0={g0}, g1={g1}", f"epsilon={epsilon}, b={boltzmann}"),
            step("PARTITION_FORMULA", "Z=g0+g1*b"),
            step("M", g1, fraction_text(boltzmann),
                 fraction_text(excited_weight)),
            step("A", g0, fraction_text(excited_weight),
                 fraction_text(partition)),
            step("D", g0, fraction_text(partition), fraction_text(p_ground)),
            step("D", fraction_text(excited_weight),
                 fraction_text(partition), fraction_text(p_excited)),
            step("PARTITION_FORMULA", "mean_energy=epsilon*p_excited"),
            step("M", epsilon, fraction_text(p_excited),
                 fraction_text(mean_energy)),
        ]
        answer = (
            f"Z={fraction_text(partition)}; "
            f"p_excited={fraction_text(p_excited)}; "
            f"mean_energy={fraction_text(mean_energy)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"A two-level system has ground degeneracy g0={g0}, excited "
            f"degeneracy g1={g1}, excited energy epsilon={epsilon}, and "
            f"Boltzmann factor b={fraction_text(boltzmann)} for the excited "
            "level. Compute Z, excited occupancy, and mean energy."
        )
        return dict(
            problem_id=jid(),
            operation=f"partition_function_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
