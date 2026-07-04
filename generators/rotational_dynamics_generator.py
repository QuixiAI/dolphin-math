import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class RotationalDynamicsGenerator(ProblemGenerator):
    """
    Rotational inertia and angular momentum conservation.

    Variants:
    - parallel_axis: apply I = I_cm + m d^2
    - angular_momentum: conserve I omega when inertia changes

    Op-codes used:
    - ROT_SETUP: rotational system givens
    - ROT_FORMULA: rotational dynamics relation
    - A / S / M / D / E (established/shared): exact arithmetic
    - CHECK: conservation or inverse-operation verification
    - Z: requested rotational quantity
    """

    VARIANTS = ["parallel_axis", "angular_momentum"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "parallel_axis":
            problem, steps, answer = self._generate_parallel_axis()
        else:
            problem, steps, answer = self._generate_angular_momentum()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"rotational_dynamics_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_parallel_axis(self):
        inertia_cm = random.randint(1, 80)
        mass = random.randint(1, 30)
        distance = random.randint(1, 12)
        distance_sq = distance ** 2
        added_inertia = mass * distance_sq
        inertia = inertia_cm + added_inertia
        check_cm = inertia - added_inertia
        steps = [
            step("ROT_SETUP", "parallel_axis", f"I_cm={inertia_cm}, m={mass}",
                 f"d={distance}"),
            step("ROT_FORMULA", "I=I_cm+m*d^2"),
            step("E", distance, 2, distance_sq),
            step("M", mass, distance_sq, added_inertia),
            step("A", inertia_cm, added_inertia, inertia),
            step("S", inertia, added_inertia, check_cm),
            step("CHECK", "recover I_cm", check_cm, f"given {inertia_cm}"),
        ]
        answer = f"I={inertia} kg*m^2"
        problem = (
            f"A rigid body has center-of-mass moment of inertia I_cm="
            f"{inertia_cm} kg*m^2 and mass {mass} kg. Find the moment of "
            f"inertia about a parallel axis {distance} m away."
        )
        return problem, steps, answer

    def _generate_angular_momentum(self):
        inertia1 = random.randint(1, 40)
        omega1 = random.randint(1, 30)
        inertia2 = random.randint(1, 40)
        angular_momentum = inertia1 * omega1
        omega2 = Fraction(angular_momentum, inertia2)
        check_l = inertia2 * omega2
        steps = [
            step("ROT_SETUP", "angular_momentum",
                 f"I1={inertia1}, omega1={omega1}", f"I2={inertia2}"),
            step("ROT_FORMULA", "I1*omega1=I2*omega2"),
            step("M", inertia1, omega1, angular_momentum),
            step("D", angular_momentum, inertia2, fraction_text(omega2)),
            step("M", inertia2, fraction_text(omega2),
                 fraction_text(check_l)),
            step("CHECK", "angular momentum", fraction_text(check_l),
                 f"initial {angular_momentum}"),
        ]
        answer = (
            f"omega2={fraction_text(omega2)} rad/s; "
            f"L={angular_momentum} kg*m^2/s"
        )
        problem = (
            f"A rotating system has moment of inertia I1={inertia1} kg*m^2 "
            f"and angular speed omega1={omega1} rad/s. Its moment of inertia "
            f"changes to I2={inertia2} kg*m^2 with no external torque. Find "
            "the new angular speed."
        )
        return problem, steps, answer
