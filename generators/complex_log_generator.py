import random

from base_generator import ProblemGenerator
from helpers import step, jid


ARG_TEXT = {
    0: "0",
    30: "pi/6",
    45: "pi/4",
    60: "pi/3",
    90: "pi/2",
    120: "2pi/3",
    135: "3pi/4",
    150: "5pi/6",
    180: "pi",
    -150: "-5pi/6",
    -135: "-3pi/4",
    -120: "-2pi/3",
    -90: "-pi/2",
    -60: "-pi/3",
    -45: "-pi/4",
    -30: "-pi/6",
}


ANGLES = [0, 30, 45, 60, 90, 120, 135, 150,
          180, 210, 225, 240, 270, 300, 315, 330]


def principal_degrees(theta):
    return theta - 360 if theta > 180 else theta


def ln_text(radius):
    return "0" if radius == 1 else f"ln({radius})"


def principal_log_text(radius, arg):
    ln_part = ln_text(radius)
    if arg == "0":
        return ln_part
    if arg.startswith("-"):
        arg_abs = arg.lstrip("-")
        if ln_part == "0":
            return f"-i*{arg_abs}"
        return f"{ln_part} - i*{arg_abs}"
    if ln_part == "0":
        return f"i*{arg}"
    return f"{ln_part} + i*{arg}"


def multivalued_log_text(radius, arg):
    ln_part = ln_text(radius)
    angle = "2pi*k" if arg == "0" else f"{arg} + 2pi*k"
    if ln_part == "0":
        return f"i*({angle})"
    return f"{ln_part} + i*({angle})"


class ComplexLogGenerator(ProblemGenerator):
    """
    Principal and multivalued complex logarithms, plus the principal power
    i^i = exp(i Log i).

    Variants:
    - log: Log(z) and all log(z) values for z = r cis(theta)
    - power_ii: principal value of i^i

    Op-codes used:
    - LOG_SETUP / LOG_FORMULA / PRINCIPAL_LOG / MULTIVALUED_LOG
    - POWER_SETUP / I_SQUARE / REWRITE for i^i
    - ARGUMENT / ANGLE_WRAP: principal argument bookkeeping
    - S (established/shared): subtract 360 degrees when wrapping
    - Z: final logarithm or power value
    """

    VARIANTS = ["log", "power_ii"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(["log", "log", "power_ii"])
        if variant == "log":
            problem, steps, answer = self._generate_log()
        else:
            problem, steps, answer = self._generate_power_ii()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"complex_log_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_log(self):
        radius = random.randint(1, 50)
        theta = random.choice(ANGLES)
        principal = principal_degrees(theta)
        arg = ARG_TEXT[principal]
        steps = [
            step("LOG_SETUP", f"z={radius} cis({theta} deg)"),
        ]
        if theta > 180:
            steps.append(step("S", theta, 360, principal))
            steps.append(step("ANGLE_WRAP", f"{theta} deg",
                              f"{principal} deg"))
        else:
            steps.append(step("ARGUMENT", f"{theta} deg",
                              f"{principal} deg"))
        principal_text = principal_log_text(radius, arg)
        multivalued_text = multivalued_log_text(radius, arg)
        steps.extend([
            step("LOG_FORMULA", "log z = ln r + i(arg + 2pi*k)"),
            step("PRINCIPAL_LOG", principal_text),
            step("MULTIVALUED_LOG", multivalued_text, "k in Z"),
        ])
        answer = (
            f"Log(z) = {principal_text}; "
            f"log(z) = {multivalued_text}, k in Z"
        )
        problem = (
            f"Find the principal Log and all logarithms of "
            f"z = {radius} cis({theta} deg)."
        )
        return problem, steps, answer

    def _generate_power_ii(self):
        steps = [
            step("POWER_SETUP", "i^i", "principal logarithm"),
            step("REWRITE", "i = cis(90 deg)"),
            step("PRINCIPAL_LOG", "Log(i) = i*pi/2"),
            step("REWRITE", "i^i = exp(i*Log(i))",
                 "exp(i*i*pi/2)"),
            step("I_SQUARE", "i^2", "-1"),
            step("REWRITE", "exp(-pi/2)", "e^(-pi/2)"),
        ]
        answer = "e^(-pi/2)"
        problem = "Compute i^i using the principal logarithm."
        return problem, steps, answer
