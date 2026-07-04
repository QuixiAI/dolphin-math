import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class CollisionGenerator(ProblemGenerator):
    """
    Momentum and collision calculations in 1D and 2D.

    Variants:
    - inelastic_1d: objects stick together
    - elastic_1d: standard one-dimensional elastic collision formulas
    - inelastic_2d: objects stick together, component momentum

    Op-codes used:
    - COLLISION_SETUP: masses and velocities
    - MOMENTUM: momentum quantity being computed
    - FORMULA: collision formula
    - A / S / M / D (established/shared): exact arithmetic
    - Z: final velocity or velocity components
    """

    VARIANTS = ["inelastic_1d", "elastic_1d", "inelastic_2d"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "inelastic_1d":
            problem, steps, answer = self._generate_inelastic_1d()
        elif variant == "elastic_1d":
            problem, steps, answer = self._generate_elastic_1d()
        else:
            problem, steps, answer = self._generate_inelastic_2d()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"collision_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_inelastic_1d(self):
        m1 = random.randint(1, 20)
        m2 = random.randint(1, 20)
        u1 = random.randint(-20, 30)
        u2 = random.randint(-20, 30)
        p1 = m1 * u1
        p2 = m2 * u2
        total_p = p1 + p2
        total_m = m1 + m2
        v = Fraction(total_p, total_m)
        steps = [
            step("COLLISION_SETUP", "inelastic_1d",
                 f"m1={m1}, u1={u1}", f"m2={m2}, u2={u2}"),
            step("MOMENTUM", "p1=m1*u1"),
            step("M", m1, u1, p1),
            step("MOMENTUM", "p2=m2*u2"),
            step("M", m2, u2, p2),
            step("A", p1, p2, total_p),
            step("A", m1, m2, total_m),
            step("FORMULA", "v=(p1+p2)/(m1+m2)"),
            step("D", total_p, total_m, fraction_text(v)),
        ]
        answer = f"stuck-together velocity={fraction_text(v)} m/s"
        problem = (
            f"In a 1D perfectly inelastic collision, m1={m1} kg has "
            f"u1={u1} m/s and m2={m2} kg has u2={u2} m/s. Find the "
            "common final velocity."
        )
        return problem, steps, answer

    def _generate_elastic_1d(self):
        m1 = random.randint(1, 15)
        m2 = random.randint(1, 15)
        u1 = random.randint(-15, 25)
        u2 = random.randint(-15, 25)
        total_m = m1 + m2
        diff12 = m1 - m2
        diff21 = m2 - m1
        two_m2 = 2 * m2
        two_m1 = 2 * m1
        v1_num_part1 = diff12 * u1
        v1_num_part2 = two_m2 * u2
        v1_num = v1_num_part1 + v1_num_part2
        v2_num_part1 = two_m1 * u1
        v2_num_part2 = diff21 * u2
        v2_num = v2_num_part1 + v2_num_part2
        v1 = Fraction(v1_num, total_m)
        v2 = Fraction(v2_num, total_m)
        steps = [
            step("COLLISION_SETUP", "elastic_1d",
                 f"m1={m1}, u1={u1}", f"m2={m2}, u2={u2}"),
            step("A", m1, m2, total_m),
            step("FORMULA", "v1=((m1-m2)u1+2m2u2)/(m1+m2)"),
            step("S", m1, m2, diff12),
            step("M", diff12, u1, v1_num_part1),
            step("M", 2, m2, two_m2),
            step("M", two_m2, u2, v1_num_part2),
            step("A", v1_num_part1, v1_num_part2, v1_num),
            step("D", v1_num, total_m, fraction_text(v1)),
            step("FORMULA", "v2=(2m1u1+(m2-m1)u2)/(m1+m2)"),
            step("M", 2, m1, two_m1),
            step("M", two_m1, u1, v2_num_part1),
            step("S", m2, m1, diff21),
            step("M", diff21, u2, v2_num_part2),
            step("A", v2_num_part1, v2_num_part2, v2_num),
            step("D", v2_num, total_m, fraction_text(v2)),
        ]
        answer = f"v1={fraction_text(v1)} m/s; v2={fraction_text(v2)} m/s"
        problem = (
            f"In a 1D elastic collision, m1={m1} kg has u1={u1} m/s and "
            f"m2={m2} kg has u2={u2} m/s. Find final velocities v1 and v2."
        )
        return problem, steps, answer

    def _generate_inelastic_2d(self):
        m1 = random.randint(1, 20)
        m2 = random.randint(1, 20)
        v1x = random.randint(-12, 15)
        v1y = random.randint(-12, 15)
        v2x = random.randint(-12, 15)
        v2y = random.randint(-12, 15)
        p1x = m1 * v1x
        p2x = m2 * v2x
        px = p1x + p2x
        p1y = m1 * v1y
        p2y = m2 * v2y
        py = p1y + p2y
        total_m = m1 + m2
        vx = Fraction(px, total_m)
        vy = Fraction(py, total_m)
        steps = [
            step("COLLISION_SETUP", "inelastic_2d",
                 f"m1={m1}, v1=({v1x},{v1y})",
                 f"m2={m2}, v2=({v2x},{v2y})"),
            step("MOMENTUM", "x components"),
            step("M", m1, v1x, p1x),
            step("M", m2, v2x, p2x),
            step("A", p1x, p2x, px),
            step("MOMENTUM", "y components"),
            step("M", m1, v1y, p1y),
            step("M", m2, v2y, p2y),
            step("A", p1y, p2y, py),
            step("A", m1, m2, total_m),
            step("D", px, total_m, fraction_text(vx)),
            step("D", py, total_m, fraction_text(vy)),
        ]
        answer = (
            f"stuck-together velocity=({fraction_text(vx)},"
            f"{fraction_text(vy)}) m/s"
        )
        problem = (
            f"In a 2D perfectly inelastic collision, m1={m1} kg has "
            f"v1=({v1x},{v1y}) m/s and m2={m2} kg has v2=({v2x},{v2y}) "
            "m/s. Find the common final velocity vector."
        )
        return problem, steps, answer
