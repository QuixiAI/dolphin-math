import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class HydrogenAtomGenerator(ProblemGenerator):
    """
    Hydrogen-atom Rydberg transition and ionization arithmetic.

    Variants:
    - transition_energy: Delta_E = R_E(1/n_low^2 - 1/n_high^2).
    - transition_wavelength: 1/lambda = R_L(1/n_low^2 - 1/n_high^2).
    - ionization_energy: E_ion = R_E/n^2 from level n.

    Op-codes used:
    - HYDROGEN_SETUP / HYDROGEN_FORMULA
    - E / D / S / M (established/shared): exact Rydberg arithmetic
    - Z: transition energy, wavelength, or ionization energy
    """

    VARIANTS = ["transition_energy", "transition_wavelength",
                "ionization_energy"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "transition_energy":
            problem, steps, answer = self._generate_transition_energy()
        elif variant == "transition_wavelength":
            problem, steps, answer = self._generate_transition_wavelength()
        else:
            problem, steps, answer = self._generate_ionization_energy()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"hydrogen_atom_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    @staticmethod
    def _transition_levels():
        n_low = random.randint(1, 6)
        n_high = random.randint(n_low + 1, n_low + 8)
        return n_low, n_high

    @staticmethod
    def _level_difference_steps(n_low, n_high):
        low_sq = n_low ** 2
        high_sq = n_high ** 2
        low_recip = Fraction(1, low_sq)
        high_recip = Fraction(1, high_sq)
        diff = low_recip - high_recip
        return [
            step("E", n_low, 2, low_sq),
            step("E", n_high, 2, high_sq),
            step("D", 1, low_sq, fraction_text(low_recip)),
            step("D", 1, high_sq, fraction_text(high_recip)),
            step("S", fraction_text(low_recip), fraction_text(high_recip),
                 fraction_text(diff)),
        ], diff

    def _generate_transition_energy(self):
        n_low, n_high = self._transition_levels()
        rydberg_energy = random.randint(1, 40)
        diff_steps, diff = self._level_difference_steps(n_low, n_high)
        energy = rydberg_energy * diff
        steps = [
            step("HYDROGEN_SETUP", "transition_energy",
                 f"n_low={n_low}, n_high={n_high}",
                 f"R_E={rydberg_energy} eV"),
            step("HYDROGEN_FORMULA",
                 "Delta_E=R_E*(1/n_low^2-1/n_high^2)"),
        ]
        steps.extend(diff_steps)
        steps.append(step("M", rydberg_energy, fraction_text(diff),
                          fraction_text(energy)))
        answer = f"Delta_E={fraction_text(energy)} eV"
        problem = (
            f"In a hydrogen atom with R_E={rydberg_energy} eV, an electron "
            f"drops from n={n_high} to n={n_low}. Find the photon energy "
            "Delta_E."
        )
        return problem, steps, answer

    def _generate_transition_wavelength(self):
        n_low, n_high = self._transition_levels()
        rydberg_length = random.randint(1, 30)
        diff_steps, diff = self._level_difference_steps(n_low, n_high)
        inverse_lambda = rydberg_length * diff
        wavelength = Fraction(1, inverse_lambda)
        steps = [
            step("HYDROGEN_SETUP", "transition_wavelength",
                 f"n_low={n_low}, n_high={n_high}",
                 f"R_L={rydberg_length} 1/m"),
            step("HYDROGEN_FORMULA",
                 "1/lambda=R_L*(1/n_low^2-1/n_high^2)"),
        ]
        steps.extend(diff_steps)
        steps.extend([
            step("M", rydberg_length, fraction_text(diff),
                 fraction_text(inverse_lambda)),
            step("D", 1, fraction_text(inverse_lambda),
                 fraction_text(wavelength)),
        ])
        answer = f"lambda={fraction_text(wavelength)} m"
        problem = (
            f"For hydrogen with R_L={rydberg_length} 1/m, an electron drops "
            f"from n={n_high} to n={n_low}. Use the Rydberg formula to find "
            "lambda."
        )
        return problem, steps, answer

    def _generate_ionization_energy(self):
        n = random.randint(1, 12)
        rydberg_energy = random.randint(1, 60)
        n_sq = n ** 2
        energy = Fraction(rydberg_energy, n_sq)
        steps = [
            step("HYDROGEN_SETUP", "ionization_energy", f"n={n}",
                 f"R_E={rydberg_energy} eV"),
            step("HYDROGEN_FORMULA", "E_ion=R_E/n^2"),
            step("E", n, 2, n_sq),
            step("D", rydberg_energy, n_sq, fraction_text(energy)),
        ]
        answer = f"E_ion={fraction_text(energy)} eV"
        problem = (
            f"Hydrogen has ionization constant R_E={rydberg_energy} eV. "
            f"Find the ionization energy from n={n}."
        )
        return problem, steps, answer
