import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def log_term(coeff, arg):
    coeff = Fraction(coeff)
    if coeff == 1:
        return f"ln({arg})"
    if coeff.denominator == 1:
        return f"{coeff.numerator}*ln({arg})"
    return f"({coeff})*ln({arg})"


class EntropyChangeGenerator(ProblemGenerator):
    """
    Entropy changes for ideal-gas processes and ideal mixing.

    Variants:
    - isothermal_expansion: DeltaS = nR ln(V2/V1), R=1
    - constant_volume_heating: DeltaS = nCv ln(T2/T1)
    - equal_gas_mixing: DeltaS_mix = 2n ln 2 for equal moles, R=1

    Op-codes used:
    - ENTROPY_SETUP: process givens
    - ENTROPY_FORMULA: symbolic entropy relation
    - LOG_TERM: exact logarithmic term
    - A / M / D (established/shared): exact coefficient arithmetic
    - Z: exact symbolic entropy change
    """

    VARIANTS = ["isothermal_expansion", "constant_volume_heating",
                "equal_gas_mixing"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "isothermal_expansion":
            problem, steps, answer = self._generate_isothermal_expansion()
        elif variant == "constant_volume_heating":
            problem, steps, answer = self._generate_constant_volume_heating()
        else:
            problem, steps, answer = self._generate_equal_gas_mixing()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"entropy_change_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_isothermal_expansion(self):
        moles = random.randint(1, 12)
        v1 = random.randint(1, 12)
        ratio = random.randint(2, 10)
        v2 = v1 * ratio
        coeff = moles
        value = log_term(coeff, ratio)
        steps = [
            step("ENTROPY_SETUP", "isothermal_expansion",
                 f"n={moles}, R=1", f"V1={v1}, V2={v2}"),
            step("ENTROPY_FORMULA", "DeltaS=nR*ln(V2/V1)"),
            step("D", v2, v1, ratio),
            step("M", moles, 1, coeff),
            step("LOG_TERM", coeff, f"ln({ratio})", value),
        ]
        answer = f"DeltaS={value} J/K"
        problem = (
            f"An ideal gas undergoes isothermal expansion with n={moles} mol, "
            f"R=1, V1={v1} L, and V2={v2} L. Find DeltaS exactly."
        )
        return problem, steps, answer

    def _generate_constant_volume_heating(self):
        moles = random.randint(1, 12)
        cv = random.randint(1, 8)
        t1 = random.randint(1, 12)
        ratio = random.randint(2, 10)
        t2 = t1 * ratio
        coeff = moles * cv
        value = log_term(coeff, ratio)
        steps = [
            step("ENTROPY_SETUP", "constant_volume_heating",
                 f"n={moles}, Cv={cv}", f"T1={t1}, T2={t2}"),
            step("ENTROPY_FORMULA", "DeltaS=nCv*ln(T2/T1)"),
            step("M", moles, cv, coeff),
            step("D", t2, t1, ratio),
            step("LOG_TERM", coeff, f"ln({ratio})", value),
        ]
        answer = f"DeltaS={value} J/K"
        problem = (
            f"An ideal gas is heated at constant volume with n={moles} mol, "
            f"Cv={cv}, T1={t1} K, and T2={t2} K. Find DeltaS exactly."
        )
        return problem, steps, answer

    def _generate_equal_gas_mixing(self):
        each = random.randint(1, 12)
        total = each + each
        mole_fraction = Fraction(each, total)
        coeff = 2 * each
        value = log_term(coeff, 2)
        steps = [
            step("ENTROPY_SETUP", "equal_gas_mixing",
                 f"nA={each}, nB={each}", "R=1"),
            step("ENTROPY_FORMULA", "DeltaS_mix=-sum n_i ln(x_i)"),
            step("A", each, each, total),
            step("D", each, total, fraction_text(mole_fraction)),
            step("ENTROPY_FORMULA", "-ln(1/2)=ln(2)"),
            step("M", 2, each, coeff),
            step("LOG_TERM", coeff, "ln(2)", value),
        ]
        answer = f"DeltaS_mix={value} J/K"
        problem = (
            f"Two ideal gases mix at the same temperature: nA={each} mol and "
            f"nB={each} mol. With R=1, find DeltaS_mix exactly."
        )
        return problem, steps, answer
