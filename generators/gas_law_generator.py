import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class GasLawGenerator(ProblemGenerator):
    """
    Ideal-gas and combined-gas law computations with R supplied as 1.

    Variants:
    - ideal_moles: solve n = PV/(RT)
    - combined_pressure: solve P2 from P1 V1 / T1 = P2 V2 / T2

    Op-codes used:
    - GAS_SETUP: gas-law givens and units
    - GAS_FORMULA: gas-law relation
    - M / D (established/shared): exact arithmetic
    - Z: requested gas quantity
    """

    VARIANTS = ["ideal_moles", "combined_pressure"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "ideal_moles":
            problem, steps, answer = self._generate_ideal_moles()
        else:
            problem, steps, answer = self._generate_combined_pressure()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"gas_law_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_ideal_moles(self):
        pressure = random.randint(1, 30)
        volume = random.randint(1, 30)
        temperature = random.randint(1, 30)
        pv = pressure * volume
        moles = Fraction(pv, temperature)
        steps = [
            step("GAS_SETUP", "ideal_moles",
                 f"P={pressure}, V={volume}", f"T={temperature}, R=1"),
            step("GAS_FORMULA", "PV=nRT so n=PV/T"),
            step("M", pressure, volume, pv),
            step("D", pv, temperature, fraction_text(moles)),
        ]
        answer = f"n={fraction_text(moles)} mol"
        problem = (
            f"An ideal gas has pressure P={pressure} atm, volume V={volume} L, "
            f"and temperature T={temperature} K. Use R=1 to find moles n."
        )
        return problem, steps, answer

    def _generate_combined_pressure(self):
        p1 = random.randint(1, 30)
        v1 = random.randint(1, 30)
        t1 = random.randint(1, 30)
        v2 = random.randint(1, 30)
        t2 = random.randint(1, 30)
        p1v1 = p1 * v1
        numerator = p1v1 * t2
        denominator = t1 * v2
        p2 = Fraction(numerator, denominator)
        steps = [
            step("GAS_SETUP", "combined_pressure",
                 f"P1={p1}, V1={v1}, T1={t1}", f"V2={v2}, T2={t2}"),
            step("GAS_FORMULA", "P1*V1/T1=P2*V2/T2"),
            step("GAS_FORMULA", "P2=P1*V1*T2/(T1*V2)"),
            step("M", p1, v1, p1v1),
            step("M", p1v1, t2, numerator),
            step("M", t1, v2, denominator),
            step("D", numerator, denominator, fraction_text(p2)),
        ]
        answer = f"P2={fraction_text(p2)} atm"
        problem = (
            f"A gas changes from P1={p1} atm, V1={v1} L, T1={t1} K to "
            f"V2={v2} L and T2={t2} K. Use the combined gas law to find P2."
        )
        return problem, steps, answer
