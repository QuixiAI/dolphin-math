import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def nonzero_charge():
    return random.choice([value for value in range(-9, 10) if value != 0])


class ElectrostaticsGenerator(ProblemGenerator):
    """
    Coulomb superposition for point charges on a line, with k=1 supplied.

    Variants:
    - field_axis: signed electric field at the origin
    - potential_axis: scalar electric potential at the origin

    Op-codes used:
    - ELEC_SETUP: charge geometry and sign convention
    - ELEC_FORMULA: Coulomb field or potential contribution
    - A / M / D / E (established/shared): exact arithmetic
    - Z: total field or potential
    """

    VARIANTS = ["field_axis", "potential_axis"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "field_axis":
            problem, steps, answer = self._generate_field_axis()
        else:
            problem, steps, answer = self._generate_potential_axis()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"electrostatics_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_field_axis(self):
        q1 = nonzero_charge()
        q2 = nonzero_charge()
        r1 = random.randint(1, 12)
        r2 = random.randint(1, 12)
        r1_sq = r1 ** 2
        r2_sq = r2 ** 2
        e1 = Fraction(q1, r1_sq)
        neg_q2 = -q2
        e2 = Fraction(neg_q2, r2_sq)
        total = e1 + e2
        steps = [
            step("ELEC_SETUP", "field_axis", f"q1={q1}, x1=-{r1}",
                 f"q2={q2}, x2={r2}"),
            step("ELEC_SETUP", "right positive", "k=1"),
            step("ELEC_FORMULA", "left charge: E1=q1/r1^2"),
            step("E", r1, 2, r1_sq),
            step("D", q1, r1_sq, fraction_text(e1)),
            step("ELEC_FORMULA", "right charge: E2=-q2/r2^2"),
            step("M", -1, q2, neg_q2),
            step("E", r2, 2, r2_sq),
            step("D", neg_q2, r2_sq, fraction_text(e2)),
            step("A", fraction_text(e1), fraction_text(e2),
                 fraction_text(total)),
        ]
        answer = f"E={fraction_text(total)} N/C right-positive"
        problem = (
            f"In scaled units with k=1, charges q1={q1} C at x=-{r1} m "
            f"and q2={q2} C at x={r2} m lie on the x-axis. Find the "
            "signed electric field at the origin, taking right as positive."
        )
        return problem, steps, answer

    def _generate_potential_axis(self):
        q1 = nonzero_charge()
        q2 = nonzero_charge()
        q3 = nonzero_charge()
        r1 = random.randint(1, 12)
        r2 = random.randint(1, 12)
        r3 = random.randint(1, 12)
        v1 = Fraction(q1, r1)
        v2 = Fraction(q2, r2)
        partial = v1 + v2
        v3 = Fraction(q3, r3)
        total = partial + v3
        steps = [
            step("ELEC_SETUP", "potential_axis", f"q1={q1}, r1={r1}",
                 f"q2={q2}, r2={r2}"),
            step("ELEC_SETUP", f"q3={q3}, r3={r3}", "k=1"),
            step("ELEC_FORMULA", "V=sum(q_i/r_i)"),
            step("D", q1, r1, fraction_text(v1)),
            step("D", q2, r2, fraction_text(v2)),
            step("A", fraction_text(v1), fraction_text(v2),
                 fraction_text(partial)),
            step("D", q3, r3, fraction_text(v3)),
            step("A", fraction_text(partial), fraction_text(v3),
                 fraction_text(total)),
        ]
        answer = f"V={fraction_text(total)} V"
        problem = (
            f"In scaled units with k=1, three point charges are at distances "
            f"r1={r1} m, r2={r2} m, r3={r3} m from the origin with "
            f"charges q1={q1} C, q2={q2} C, q3={q3} C. Find the electric "
            "potential at the origin."
        )
        return problem, steps, answer
