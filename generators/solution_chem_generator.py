import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def random_molarity(max_num=12, max_den=5):
    return Fraction(random.randint(1, max_num), random.randint(1, max_den))


class SolutionChemGenerator(ProblemGenerator):
    """
    Exact solution-concentration arithmetic for dilution and mixing.

    Variants:
    - dilution_final_molarity: solve M2=M1*V1/V2.
    - dilution_stock_volume: solve V1=M2*V2/M1.
    - mixing_molarity: solve weighted concentration after mixing.

    Op-codes used:
    - SOLUTION_SETUP / SOLUTION_FORMULA
    - A / M / D (established/shared): exact concentration arithmetic
    - Z: requested molarity or volume
    """

    VARIANTS = [
        "dilution_final_molarity",
        "dilution_stock_volume",
        "mixing_molarity",
    ]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "dilution_final_molarity":
            problem, steps, answer = self._generate_final_molarity()
        elif variant == "dilution_stock_volume":
            problem, steps, answer = self._generate_stock_volume()
        else:
            problem, steps, answer = self._generate_mixing()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"solution_chem_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_final_molarity(self):
        m1 = random_molarity()
        v1 = random.randint(10, 200)
        v2 = random.randint(v1 + 10, v1 + 400)
        amount_units = m1 * v1
        m2 = amount_units / v2
        steps = [
            step("SOLUTION_SETUP", "dilution_final_molarity",
                 f"M1={fraction_text(m1)}, V1={v1}", f"V2={v2}"),
            step("SOLUTION_FORMULA", "M1*V1=M2*V2"),
            step("M", fraction_text(m1), v1, fraction_text(amount_units)),
            step("D", fraction_text(amount_units), v2, fraction_text(m2)),
        ]
        answer = f"M2={fraction_text(m2)} M"
        problem = (
            f"A dilution uses stock molarity M1={fraction_text(m1)} M and "
            f"stock volume V1={v1} mL, diluted to final volume V2={v2} mL. "
            "Find final molarity M2."
        )
        return problem, steps, answer

    def _generate_stock_volume(self):
        m1 = Fraction(random.randint(2, 12), 1)
        m2 = Fraction(random.randint(1, m1.numerator - 1),
                      random.randint(1, 4))
        v2 = random.randint(50, 500)
        amount_units = m2 * v2
        v1 = amount_units / m1
        steps = [
            step("SOLUTION_SETUP", "dilution_stock_volume",
                 f"M1={fraction_text(m1)}", f"M2={fraction_text(m2)}, V2={v2}"),
            step("SOLUTION_FORMULA", "M1*V1=M2*V2"),
            step("M", fraction_text(m2), v2, fraction_text(amount_units)),
            step("D", fraction_text(amount_units), fraction_text(m1),
                 fraction_text(v1)),
        ]
        answer = f"V1={fraction_text(v1)} mL"
        problem = (
            f"A stock solution has molarity M1={fraction_text(m1)} M. "
            f"Prepare V2={v2} mL at M2={fraction_text(m2)} M. Find stock "
            "volume V1."
        )
        return problem, steps, answer

    def _generate_mixing(self):
        ma = random_molarity()
        mb = random_molarity()
        va = random.randint(10, 250)
        vb = random.randint(10, 250)
        amount_a = ma * va
        amount_b = mb * vb
        total_amount = amount_a + amount_b
        total_volume = va + vb
        final_molarity = total_amount / total_volume
        steps = [
            step("SOLUTION_SETUP", "mixing_molarity",
                 f"Ma={fraction_text(ma)}, Va={va}",
                 f"Mb={fraction_text(mb)}, Vb={vb}"),
            step("SOLUTION_FORMULA",
                 "M_final=(Ma*Va+Mb*Vb)/(Va+Vb)"),
            step("M", fraction_text(ma), va, fraction_text(amount_a)),
            step("M", fraction_text(mb), vb, fraction_text(amount_b)),
            step("A", fraction_text(amount_a), fraction_text(amount_b),
                 fraction_text(total_amount)),
            step("A", va, vb, total_volume),
            step("D", fraction_text(total_amount), total_volume,
                 fraction_text(final_molarity)),
        ]
        answer = f"M_final={fraction_text(final_molarity)} M"
        problem = (
            f"Mix Va={va} mL of Ma={fraction_text(ma)} M solution with "
            f"Vb={vb} mL of Mb={fraction_text(mb)} M solution. Find final "
            "molarity M_final."
        )
        return problem, steps, answer
