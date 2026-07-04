import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


TRIG_PAIRS = [
    (Fraction(3, 5), Fraction(4, 5)),
    (Fraction(5, 13), Fraction(12, 13)),
    (Fraction(7, 25), Fraction(24, 25)),
]


def fraction_text(value):
    return str(Fraction(value))


class NewtonsLawsGenerator(ProblemGenerator):
    """
    Newton's-law force systems: Atwood machines and frictional inclines.

    Variants:
    - atwood: simultaneous equations for acceleration and tension
    - incline_friction: component forces on an incline with supplied trig

    Op-codes used:
    - NEWTON_SETUP: physical system and givens
    - FORCE_EQ: Newton's second-law equation
    - ELIMINATE: combine equations
    - FORCE_COMPONENT: resolved force component
    - A / S / M / D (established/shared): exact force arithmetic
    - Z: acceleration and requested force/tension
    """

    VARIANTS = ["atwood", "incline_friction"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "atwood":
            problem, steps, answer = self._generate_atwood()
        else:
            problem, steps, answer = self._generate_incline()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"newtons_laws_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_atwood(self):
        m1 = random.randint(1, 20)
        m2 = random.randint(m1 + 1, m1 + 25)
        g = 10
        mass_diff = m2 - m1
        force_diff = mass_diff * g
        total_mass = m1 + m2
        acceleration = Fraction(force_diff, total_mass)
        g_plus_a = Fraction(g) + acceleration
        tension = m1 * g_plus_a
        steps = [
            step("NEWTON_SETUP", "atwood", f"m1={m1}, m2={m2}", f"g={g}"),
            step("FORCE_EQ", "T-m1*g=m1*a"),
            step("FORCE_EQ", "m2*g-T=m2*a"),
            step("ELIMINATE", "(m2-m1)g=(m1+m2)a"),
            step("S", m2, m1, mass_diff),
            step("M", mass_diff, g, force_diff),
            step("A", m1, m2, total_mass),
            step("D", force_diff, total_mass, fraction_text(acceleration)),
            step("A", g, fraction_text(acceleration), fraction_text(g_plus_a)),
            step("M", m1, fraction_text(g_plus_a), fraction_text(tension)),
        ]
        answer = (
            f"a={fraction_text(acceleration)} m/s^2; "
            f"T={fraction_text(tension)} N"
        )
        problem = (
            f"An Atwood machine has masses m1={m1} kg and m2={m2} kg with "
            "m2 heavier. Use g=10 m/s^2 to solve for acceleration and "
            "tension."
        )
        return problem, steps, answer

    def _generate_incline(self):
        mass = random.randint(2, 30)
        sin_value, cos_value = random.choice(TRIG_PAIRS)
        max_mu_num = max(1, sin_value.numerator * cos_value.denominator - 1)
        mu = Fraction(random.randint(1, max_mu_num),
                      sin_value.denominator * cos_value.numerator)
        if mu * cos_value >= sin_value:
            mu = sin_value / (2 * cos_value)
        g = 10
        weight = mass * g
        parallel = weight * sin_value
        normal = weight * cos_value
        friction = mu * normal
        net = parallel - friction
        acceleration = net / mass
        steps = [
            step("NEWTON_SETUP", "incline_friction",
                 f"m={mass}, mu={fraction_text(mu)}", f"g={g}"),
            step("NEWTON_SETUP", f"sin={fraction_text(sin_value)}",
                 f"cos={fraction_text(cos_value)}"),
            step("M", mass, g, weight),
            step("FORCE_COMPONENT", "parallel=m*g*sin"),
            step("M", weight, fraction_text(sin_value),
                 fraction_text(parallel)),
            step("FORCE_COMPONENT", "normal=m*g*cos"),
            step("M", weight, fraction_text(cos_value),
                 fraction_text(normal)),
            step("FORCE_COMPONENT", "friction=mu*N"),
            step("M", fraction_text(mu), fraction_text(normal),
                 fraction_text(friction)),
            step("FORCE_EQ", "m*a=parallel-friction"),
            step("S", fraction_text(parallel), fraction_text(friction),
                 fraction_text(net)),
            step("D", fraction_text(net), mass, fraction_text(acceleration)),
        ]
        answer = (
            f"N={fraction_text(normal)} N; friction={fraction_text(friction)} N; "
            f"a={fraction_text(acceleration)} m/s^2"
        )
        problem = (
            f"A {mass} kg block slides down an incline with supplied "
            f"sin(theta)={fraction_text(sin_value)}, cos(theta)="
            f"{fraction_text(cos_value)}, and friction coefficient "
            f"mu={fraction_text(mu)}. Use g=10 m/s^2 to find normal force, "
            "friction, and acceleration."
        )
        return problem, steps, answer
