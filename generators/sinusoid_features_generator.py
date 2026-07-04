import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.arc_sector_generator import pi_txt


def head_txt(A, fn):
    """'2sin', '-cos', 'sin'."""
    coef = {1: "", -1: "-"}.get(A, str(A))
    return f"{coef}{fn}"


def d_txt(D):
    if D == 0:
        return ""
    return f" + {D}" if D > 0 else f" - {-D}"


class SinusoidFeaturesGenerator(ProblemGenerator):
    """
    Amplitude, period, phase shift, and midline from a sinusoid
    equation. The unfactored form A·cos(Bx - φ) forces the classic
    factor-out step: the phase shift is φ/B, not φ.

    Variants:
    - factored:   y = A sin(B(x - C°)) + D
    - unfactored: y = A cos(Bx - φ°) + D, factored explicitly first
    - radians:    y = A sin(B(x - π/k)) + D, period 2π/B

    Op-codes used:
    - SINUSOID_SETUP: the equation and the goal
    - AMPLITUDE: abs of the leading coefficient (work, value)
    - D: period = 360°/B or 2π/B; shift = φ/B (established)
    - PERIOD / PHASE_SHIFT / MIDLINE: the named features
    - REWRITE: the factoring of Bx - φ (established)
    - Z: 'amplitude ...; period ...; phase shift ...; midline ...'
    """

    VARIANTS = ["factored", "unfactored", "radians"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        A = random.choice([v for v in range(-5, 6) if v != 0])
        fn = random.choice(["sin", "cos"])
        D = random.randint(-6, 6)
        B = random.choice([2, 3, 4, 6])
        right = random.random() < 0.5
        sgn = "-" if right else "+"
        direction = "right" if right else "left"

        steps = []
        if variant == "radians":
            k = random.choice([2, 3, 4, 6])
            shift = f"π/{k}"
            eq = (f"y = {head_txt(A, fn)}({B}(x {sgn} {shift}))"
                  f"{d_txt(D)}")
            period = pi_txt(Fraction(2, B))
            steps.append(step("SINUSOID_SETUP", eq,
                              "amplitude, period, phase shift, midline"))
            steps.append(step("AMPLITUDE", f"abs({A})", abs(A)))
            steps.append(step("D", "2π", B, period))
            steps.append(step("PERIOD", period))
            shift_txt = f"{shift} {direction}"
        elif variant == "factored":
            C = random.choice([10, 15, 20, 30, 45, 60, 90])
            eq = (f"y = {head_txt(A, fn)}({B}(x {sgn} {C}°))"
                  f"{d_txt(D)}")
            period = f"{360 // B}°"
            steps.append(step("SINUSOID_SETUP", eq,
                              "amplitude, period, phase shift, midline"))
            steps.append(step("AMPLITUDE", f"abs({A})", abs(A)))
            steps.append(step("D", 360, B, 360 // B))
            steps.append(step("PERIOD", period))
            shift_txt = f"{C}° {direction}"
        else:
            C = random.choice([10, 15, 20, 30, 45])
            phi = B * C
            eq = (f"y = {head_txt(A, fn)}({B}x {sgn} {phi}°)"
                  f"{d_txt(D)}")
            period = f"{360 // B}°"
            steps.append(step("SINUSOID_SETUP", eq,
                              "amplitude, period, phase shift, midline"))
            steps.append(step("AMPLITUDE", f"abs({A})", abs(A)))
            steps.append(step("D", 360, B, 360 // B))
            steps.append(step("PERIOD", period))
            steps.append(step("REWRITE",
                              f"{B}x {sgn} {phi}° = {B}(x {sgn} {C}°)"))
            steps.append(step("D", phi, B, C))
            shift_txt = f"{C}° {direction}"
        steps.append(step("PHASE_SHIFT", shift_txt))
        steps.append(step("MIDLINE", f"y = {D}"))

        answer = (f"amplitude {abs(A)}; period {period}; phase shift "
                  f"{shift_txt}; midline y = {D}")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"sinusoid_features_{variant}",
            problem=(f"State the amplitude, period, phase shift, and "
                     f"midline of {eq}."),
            steps=steps,
            final_answer=answer,
        )
