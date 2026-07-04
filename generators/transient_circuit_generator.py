import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def scale_expr(scale, body):
    scale = Fraction(scale)
    if scale == 1:
        return body
    if scale.denominator == 1:
        return f"{scale.numerator}*{body}"
    return f"({scale})*{body}"


class TransientCircuitGenerator(ProblemGenerator):
    """
    RC and RL first-order transients with exact symbolic exponentials.

    Variants:
    - rc_charging: V_C(t) = Vs(1 - e^(-t/RC))
    - rl_rise: I(t) = (V/R)(1 - e^(-tR/L))

    Op-codes used:
    - TRANSIENT_SETUP: circuit values and initial condition
    - TRANSIENT_FORMULA: first-order transient formula
    - EXP_SUB: substitute an exact exponent
    - M / D (established/shared): exact time-constant arithmetic
    - Z: exact transient value
    """

    VARIANTS = ["rc_charging", "rl_rise"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "rc_charging":
            problem, steps, answer = self._generate_rc_charging()
        else:
            problem, steps, answer = self._generate_rl_rise()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"transient_circuit_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_rc_charging(self):
        resistance = random.randint(1, 12)
        capacitance = random.randint(1, 12)
        source = random.randint(2, 24)
        multiple = random.randint(1, 6)
        tau = resistance * capacitance
        time = tau * multiple
        body = f"(1-e^-{multiple})"
        voltage = scale_expr(source, body)
        steps = [
            step("TRANSIENT_SETUP", "rc_charging",
                 f"R={resistance}, C={capacitance}", f"Vs={source}, t={time}"),
            step("TRANSIENT_FORMULA", "tau=R*C"),
            step("M", resistance, capacitance, tau),
            step("D", time, tau, multiple),
            step("TRANSIENT_FORMULA", "V_C=Vs*(1-e^(-t/tau))"),
            step("EXP_SUB", "t/tau", multiple, f"e^-{multiple}"),
            step("TRANSIENT_FORMULA", f"V_C={source}*(1-e^-{multiple})"),
        ]
        answer = f"V_C={voltage} V"
        problem = (
            f"An RC circuit has R={resistance} ohm, C={capacitance} F, "
            f"source Vs={source} V, and starts uncharged. Find capacitor "
            f"voltage at t={time} s in exact exponential form."
        )
        return problem, steps, answer

    def _generate_rl_rise(self):
        resistance = random.randint(1, 12)
        tau = random.randint(1, 12)
        inductance = resistance * tau
        source = random.randint(2, 48)
        multiple = random.randint(1, 6)
        time = tau * multiple
        steady_current = Fraction(source, resistance)
        body = f"(1-e^-{multiple})"
        current = scale_expr(steady_current, body)
        steps = [
            step("TRANSIENT_SETUP", "rl_rise",
                 f"R={resistance}, L={inductance}", f"V={source}, t={time}"),
            step("TRANSIENT_FORMULA", "tau=L/R"),
            step("D", inductance, resistance, tau),
            step("TRANSIENT_FORMULA", "I_inf=V/R"),
            step("D", source, resistance, fraction_text(steady_current)),
            step("D", time, tau, multiple),
            step("TRANSIENT_FORMULA", "I=I_inf*(1-e^(-t/tau))"),
            step("EXP_SUB", "t/tau", multiple, f"e^-{multiple}"),
            step("TRANSIENT_FORMULA",
                 f"I={fraction_text(steady_current)}*(1-e^-{multiple})"),
        ]
        answer = f"I={current} A"
        problem = (
            f"An RL circuit has R={resistance} ohm, L={inductance} H, "
            f"source V={source} V, and starts with zero current. Find "
            f"current at t={time} s in exact exponential form."
        )
        return problem, steps, answer
