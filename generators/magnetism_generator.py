import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


TRIG_SINES = [Fraction(3, 5), Fraction(4, 5), Fraction(5, 13),
              Fraction(12, 13), Fraction(7, 25), Fraction(24, 25)]


def fraction_text(value):
    return str(Fraction(value))


def over_pi_text(value):
    coeff = Fraction(value)
    if coeff.denominator == 1:
        return f"{coeff.numerator}/π"
    return f"{coeff.numerator}/({coeff.denominator}π)"


class MagnetismGenerator(ProblemGenerator):
    """
    Magnetic force and standard magnetic-field cases.

    Variants:
    - force: F = q v B sin(theta)
    - straight_wire: B = mu0 I/(2πr), with mu0=1
    - loop_center: B = mu0 I/(2R), with mu0=1

    Op-codes used:
    - MAG_SETUP: magnetic system and supplied constants
    - MAG_FORMULA: magnetic force or field relation
    - PI_DEN: attach a symbolic π in the denominator
    - M / D (established/shared): exact arithmetic
    - Z: magnetic force or field
    """

    VARIANTS = ["force", "straight_wire", "loop_center"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "force":
            problem, steps, answer = self._generate_force()
        elif variant == "straight_wire":
            problem, steps, answer = self._generate_straight_wire()
        else:
            problem, steps, answer = self._generate_loop_center()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"magnetism_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_force(self):
        charge = random.randint(1, 12)
        speed = random.randint(1, 40)
        field = random.randint(1, 20)
        sin_theta = random.choice(TRIG_SINES)
        qv = charge * speed
        qvb = qv * field
        force = qvb * sin_theta
        steps = [
            step("MAG_SETUP", "force", f"q={charge}, v={speed}",
                 f"B={field}, sin={fraction_text(sin_theta)}"),
            step("MAG_FORMULA", "F=q*v*B*sin(theta)"),
            step("M", charge, speed, qv),
            step("M", qv, field, qvb),
            step("M", qvb, fraction_text(sin_theta), fraction_text(force)),
        ]
        answer = f"F={fraction_text(force)} N"
        problem = (
            f"A charge q={charge} C moves at speed v={speed} m/s through "
            f"a magnetic field B={field} T with sin(theta)="
            f"{fraction_text(sin_theta)}. Find the magnetic force magnitude."
        )
        return problem, steps, answer

    def _generate_straight_wire(self):
        current = random.randint(1, 80)
        radius = random.randint(1, 20)
        denominator = 2 * radius
        coeff = Fraction(current, denominator)
        field = over_pi_text(coeff)
        steps = [
            step("MAG_SETUP", "straight_wire", f"I={current}, r={radius}",
                 "mu0=1"),
            step("MAG_FORMULA", "B=mu0*I/(2πr)"),
            step("M", 2, radius, denominator),
            step("D", current, denominator, fraction_text(coeff)),
            step("PI_DEN", fraction_text(coeff), "π", field),
        ]
        answer = f"B={field} T"
        problem = (
            f"A long straight wire carries current I={current} A. At "
            f"distance r={radius} m, use mu0=1 to find the magnetic field "
            "magnitude B=mu0*I/(2πr)."
        )
        return problem, steps, answer

    def _generate_loop_center(self):
        current = random.randint(1, 80)
        radius = random.randint(1, 20)
        denominator = 2 * radius
        field = Fraction(current, denominator)
        steps = [
            step("MAG_SETUP", "loop_center", f"I={current}, R={radius}",
                 "mu0=1"),
            step("MAG_FORMULA", "B=mu0*I/(2R)"),
            step("M", 2, radius, denominator),
            step("D", current, denominator, fraction_text(field)),
        ]
        answer = f"B={fraction_text(field)} T"
        problem = (
            f"A circular loop carries current I={current} A and has radius "
            f"R={radius} m. Use mu0=1 to find the magnetic field at the "
            "center, B=mu0*I/(2R)."
        )
        return problem, steps, answer
