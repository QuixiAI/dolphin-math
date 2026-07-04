import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


MASS_SHELL_TRIPLES = [
    (3, 4, 5),
    (5, 12, 13),
    (8, 15, 17),
    (7, 24, 25),
    (20, 21, 29),
    (9, 40, 41),
    (12, 35, 37),
]

SPEEDS = [
    Fraction(1, 5),
    Fraction(2, 5),
    Fraction(3, 5),
    Fraction(1, 3),
    Fraction(2, 3),
    Fraction(-1, 5),
    Fraction(-2, 5),
    Fraction(-1, 3),
]


def fraction_text(value):
    return str(Fraction(value))


class RelativisticEnergyGenerator(ProblemGenerator):
    """
    Relativistic rest energy, mass-shell energy, and velocity addition.

    Variants:
    - rest_energy: E=m*c^2.
    - energy_momentum: E^2=p^2+m^2 in c=1 units.
    - velocity_addition: w=(u+v)/(1+uv) in c=1 units.

    Op-codes used:
    - REL_ENERGY_SETUP / REL_ENERGY_FORMULA
    - A / M / D / E / ROOT (established/shared): exact arithmetic
    - Z: rest energy, total energy, or composed velocity
    """

    VARIANTS = ["rest_energy", "energy_momentum", "velocity_addition"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "rest_energy":
            problem, steps, answer = self._generate_rest_energy()
        elif variant == "energy_momentum":
            problem, steps, answer = self._generate_energy_momentum()
        else:
            problem, steps, answer = self._generate_velocity_addition()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"relativistic_energy_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_rest_energy(self):
        mass = random.randint(1, 30)
        c = random.randint(2, 20)
        c_sq = c ** 2
        energy = mass * c_sq
        steps = [
            step("REL_ENERGY_SETUP", "rest_energy", f"m={mass}", f"c={c}"),
            step("REL_ENERGY_FORMULA", "E=m*c^2"),
            step("E", c, 2, c_sq),
            step("M", mass, c_sq, energy),
        ]
        answer = f"E={energy} J"
        problem = (
            f"Using E=m*c^2, find the rest energy for mass m={mass} kg "
            f"and c={c} m/s."
        )
        return problem, steps, answer

    def _generate_energy_momentum(self):
        momentum, mass, energy = random.choice(MASS_SHELL_TRIPLES)
        if random.choice([False, True]):
            momentum, mass = mass, momentum
        p_sq = momentum ** 2
        m_sq = mass ** 2
        e_sq = p_sq + m_sq
        steps = [
            step("REL_ENERGY_SETUP", "energy_momentum", "c=1",
                 f"p={momentum}, m={mass}"),
            step("REL_ENERGY_FORMULA", "E=sqrt(p^2+m^2)"),
            step("E", momentum, 2, p_sq),
            step("E", mass, 2, m_sq),
            step("A", p_sq, m_sq, e_sq),
            step("ROOT", f"sqrt({e_sq})", energy),
        ]
        answer = f"E={energy}"
        problem = (
            f"In c=1 units, a particle has momentum p={momentum} and "
            f"mass m={mass}. Find E from E^2=p^2+m^2."
        )
        return problem, steps, answer

    def _generate_velocity_addition(self):
        while True:
            u = random.choice(SPEEDS)
            v = random.choice(SPEEDS)
            denominator = 1 + u * v
            if denominator != 0:
                break
        numerator = u + v
        product = u * v
        velocity = numerator / denominator
        steps = [
            step("REL_ENERGY_SETUP", "velocity_addition",
                 f"u={fraction_text(u)}", f"v={fraction_text(v)}"),
            step("REL_ENERGY_FORMULA", "w=(u+v)/(1+u*v), c=1"),
            step("A", fraction_text(u), fraction_text(v),
                 fraction_text(numerator)),
            step("M", fraction_text(u), fraction_text(v),
                 fraction_text(product)),
            step("A", 1, fraction_text(product), fraction_text(denominator)),
            step("D", fraction_text(numerator), fraction_text(denominator),
                 fraction_text(velocity)),
        ]
        answer = f"w={fraction_text(velocity)}"
        problem = (
            f"In c=1 units, velocities u={fraction_text(u)} and "
            f"v={fraction_text(v)} are collinear. Compute the relativistic "
            "velocity sum w."
        )
        return problem, steps, answer
