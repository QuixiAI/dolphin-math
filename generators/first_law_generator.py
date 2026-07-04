import random

from base_generator import ProblemGenerator
from helpers import step, jid


class FirstLawGenerator(ProblemGenerator):
    """
    First-law bookkeeping with DeltaU = Q - W, W done by the gas/system.

    Variants:
    - isochoric: W = 0
    - adiabatic: Q = 0
    - isothermal: DeltaU = 0 for an ideal gas
    - isobaric: W = P(V2 - V1), then DeltaU = Q - W

    Op-codes used:
    - FIRSTLAW_SETUP: process givens and sign convention
    - FIRSTLAW_FORMULA: first-law or process relation
    - S / M (established/shared): exact bookkeeping arithmetic
    - Z: requested heat, work, or internal-energy change
    """

    VARIANTS = ["isochoric", "adiabatic", "isothermal", "isobaric"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "isochoric":
            problem, steps, answer = self._generate_isochoric()
        elif variant == "adiabatic":
            problem, steps, answer = self._generate_adiabatic()
        elif variant == "isothermal":
            problem, steps, answer = self._generate_isothermal()
        else:
            problem, steps, answer = self._generate_isobaric()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"first_law_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_isochoric(self):
        heat = random.randint(-80, 120)
        work = 0
        delta_u = heat - work
        steps = [
            step("FIRSTLAW_SETUP", "isochoric", f"Q={heat}", "W=0"),
            step("FIRSTLAW_FORMULA", "DeltaU=Q-W"),
            step("S", heat, work, delta_u),
        ]
        answer = f"W=0 J; DeltaU={delta_u} J"
        problem = (
            f"An isochoric process has heat Q={heat} J added to the gas. "
            "Using W as work done by the gas, find W and DeltaU."
        )
        return problem, steps, answer

    def _generate_adiabatic(self):
        work = random.randint(-80, 120)
        heat = 0
        delta_u = heat - work
        steps = [
            step("FIRSTLAW_SETUP", "adiabatic", "Q=0", f"W={work}"),
            step("FIRSTLAW_FORMULA", "DeltaU=Q-W"),
            step("S", heat, work, delta_u),
        ]
        answer = f"Q=0 J; DeltaU={delta_u} J"
        problem = (
            f"An adiabatic process has work W={work} J done by the gas. "
            "Using DeltaU=Q-W, find Q and DeltaU."
        )
        return problem, steps, answer

    def _generate_isothermal(self):
        work = random.randint(-80, 120)
        heat = work
        delta_u = heat - work
        steps = [
            step("FIRSTLAW_SETUP", "isothermal", f"W={work}", "ideal gas"),
            step("FIRSTLAW_FORMULA", "isothermal ideal gas: DeltaU=0"),
            step("FIRSTLAW_FORMULA", "DeltaU=Q-W so Q=W"),
            step("S", heat, work, delta_u),
        ]
        answer = f"Q={heat} J; DeltaU=0 J"
        problem = (
            f"An isothermal ideal-gas process has work W={work} J done by "
            "the gas. Find Q and DeltaU."
        )
        return problem, steps, answer

    def _generate_isobaric(self):
        pressure = random.randint(1, 20)
        v1 = random.randint(1, 20)
        delta_v = random.choice([value for value in range(-10, 11)
                                 if value != 0 and v1 + value > 0])
        v2 = v1 + delta_v
        heat = random.randint(-80, 160)
        work = pressure * delta_v
        delta_u = heat - work
        steps = [
            step("FIRSTLAW_SETUP", "isobaric",
                 f"P={pressure}, V1={v1}, V2={v2}", f"Q={heat}"),
            step("FIRSTLAW_FORMULA", "W=P*(V2-V1)"),
            step("S", v2, v1, delta_v),
            step("M", pressure, delta_v, work),
            step("FIRSTLAW_FORMULA", "DeltaU=Q-W"),
            step("S", heat, work, delta_u),
        ]
        answer = f"W={work} J; DeltaU={delta_u} J"
        problem = (
            f"An isobaric process has pressure P={pressure} Pa, volume "
            f"changes from V1={v1} m^3 to V2={v2} m^3, and heat Q={heat} J. "
            "Using W=P(V2-V1) and DeltaU=Q-W, find W and DeltaU."
        )
        return problem, steps, answer
