import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class OrbitalMechanicsGenerator(ProblemGenerator):
    """
    Circular motion, Newtonian gravitation, and Kepler's third law.

    Variants:
    - centripetal_force: compute a_c and F_c from m, r, and v
    - gravity_force: inverse-square gravitational force with supplied G=1
    - kepler_third: scale orbital period by a^(3/2)

    Op-codes used:
    - ORBIT_SETUP: physical givens
    - ORBIT_FORMULA: orbital/circular-motion relation
    - A / M / D / E / ROOT (established/shared): exact arithmetic
    - Z: requested orbital result
    """

    VARIANTS = ["centripetal_force", "gravity_force", "kepler_third"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "centripetal_force":
            problem, steps, answer = self._generate_centripetal_force()
        elif variant == "gravity_force":
            problem, steps, answer = self._generate_gravity_force()
        else:
            problem, steps, answer = self._generate_kepler_third()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"orbital_mechanics_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_centripetal_force(self):
        mass = random.randint(1, 30)
        radius = random.randint(2, 40)
        speed = random.randint(2, 50)
        speed_sq = speed ** 2
        acceleration = Fraction(speed_sq, radius)
        force = mass * acceleration
        steps = [
            step("ORBIT_SETUP", "centripetal_force", f"m={mass}",
                 f"r={radius}, v={speed}"),
            step("ORBIT_FORMULA", "a_c=v^2/r"),
            step("E", speed, 2, speed_sq),
            step("D", speed_sq, radius, fraction_text(acceleration)),
            step("ORBIT_FORMULA", "F_c=m*a_c"),
            step("M", mass, fraction_text(acceleration),
                 fraction_text(force)),
        ]
        answer = (
            f"a_c={fraction_text(acceleration)} m/s^2; "
            f"F_c={fraction_text(force)} N"
        )
        problem = (
            f"A {mass} kg object moves in a circle of radius {radius} m "
            f"with speed {speed} m/s. Find centripetal acceleration and "
            "centripetal force."
        )
        return problem, steps, answer

    def _generate_gravity_force(self):
        m1 = random.randint(1, 80)
        m2 = random.randint(1, 80)
        radius = random.randint(2, 30)
        g_const = 1
        mass_product = m1 * m2
        numerator = g_const * mass_product
        radius_sq = radius ** 2
        force = Fraction(numerator, radius_sq)
        steps = [
            step("ORBIT_SETUP", "gravity_force", f"m1={m1}, m2={m2}",
                 f"r={radius}, G={g_const}"),
            step("ORBIT_FORMULA", "F=G*m1*m2/r^2"),
            step("M", m1, m2, mass_product),
            step("M", g_const, mass_product, numerator),
            step("E", radius, 2, radius_sq),
            step("D", numerator, radius_sq, fraction_text(force)),
        ]
        answer = f"F_g={fraction_text(force)} N"
        problem = (
            "In a scaled gravitation problem, two masses "
            f"m1={m1} kg and m2={m2} kg are {radius} m apart with G=1. "
            "Find the gravitational force magnitude."
        )
        return problem, steps, answer

    def _generate_kepler_third(self):
        radius1 = random.randint(1, 8)
        scale = random.randint(2, 6)
        radius2 = radius1 * scale ** 2
        period1 = random.randint(5, 80)
        radius_ratio = Fraction(radius2, radius1)
        radius_ratio_cubed = radius_ratio ** 3
        period_ratio = scale ** 3
        period2 = period1 * period_ratio
        steps = [
            step("ORBIT_SETUP", "kepler_third",
                 f"T1={period1}, a1={radius1}", f"a2={radius2}"),
            step("ORBIT_FORMULA", "(T2/T1)^2=(a2/a1)^3"),
            step("D", radius2, radius1, fraction_text(radius_ratio)),
            step("E", fraction_text(radius_ratio), 3,
                 fraction_text(radius_ratio_cubed)),
            step("ROOT", fraction_text(radius_ratio_cubed), period_ratio),
            step("M", period1, period_ratio, period2),
        ]
        answer = f"T2={period2} days"
        problem = (
            f"A planet has orbital radius a1={radius1} AU and period "
            f"T1={period1} days. Another planet orbits the same star at "
            f"a2={radius2} AU. Use Kepler's third law to find the second "
            "period."
        )
        return problem, steps, answer
