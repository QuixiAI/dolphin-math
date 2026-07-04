import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def pi_text(multiplier):
    multiplier = Fraction(multiplier)
    if multiplier == 0:
        return "0"
    if multiplier == 1:
        return "pi"
    if multiplier == -1:
        return "-pi"
    if multiplier.denominator == 1:
        return f"{multiplier.numerator}pi"
    if multiplier.numerator == 1:
        return f"pi/{multiplier.denominator}"
    if multiplier.numerator == -1:
        return f"-pi/{multiplier.denominator}"
    return f"{multiplier.numerator}pi/{multiplier.denominator}"


class GaussBonnetGenerator(ProblemGenerator):
    """
    Gauss-Bonnet verification for closed surfaces:
    integral K dA = 2*pi*chi.

    Variants:
    - sphere: K=1/R^2 and area=4*pi*R^2.
    - flat_torus: K=0 on a rectangular flat torus and chi=0.

    Op-codes used:
    - GAUSS_BONNET_SETUP / THEOREM / CHECK
    - E / D / M (established/shared): exact arithmetic
    - Z: theorem verification
    """

    VARIANTS = ["sphere", "flat_torus"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "sphere":
            problem, steps, answer = self._generate_sphere()
        else:
            problem, steps, answer = self._generate_flat_torus()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"gauss_bonnet_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_sphere(self):
        radius = random.randint(2, 80)
        radius_sq = radius * radius
        curvature = Fraction(1, radius_sq)
        area_coeff = 4 * radius_sq
        total_coeff = curvature * area_coeff
        rhs_coeff = 2 * 2
        steps = [
            step("GAUSS_BONNET_SETUP", "sphere", f"R={radius}", "chi=2"),
            step("THEOREM", "integral K dA = 2*pi*chi"),
            step("E", radius, 2, radius_sq),
            step("D", 1, radius_sq, fraction_text(curvature)),
            step("M", 4, radius_sq, area_coeff),
            step("M", fraction_text(curvature), area_coeff,
                 fraction_text(total_coeff)),
            step("M", 2, 2, rhs_coeff),
            step("CHECK", "integral K dA", pi_text(total_coeff),
                 f"2pi chi = {pi_text(rhs_coeff)}"),
        ]
        answer = (
            f"verified: integral K dA = {pi_text(total_coeff)} = "
            f"2pi chi"
        )
        problem = (
            f"Verify Gauss-Bonnet for a sphere of radius {radius} "
            f"with Euler characteristic 2."
        )
        return problem, steps, answer

    def _generate_flat_torus(self):
        width = random.randint(2, 40)
        height = random.randint(2, 40)
        area = width * height
        total_coeff = 0
        rhs_coeff = 0
        steps = [
            step("GAUSS_BONNET_SETUP", "flat_torus",
                 f"width={width}, height={height}", "chi=0"),
            step("THEOREM", "integral K dA = 2*pi*chi"),
            step("M", width, height, area),
            step("M", 0, area, total_coeff),
            step("M", 2, 0, rhs_coeff),
            step("CHECK", "integral K dA", pi_text(total_coeff),
                 f"2pi chi = {pi_text(rhs_coeff)}"),
        ]
        answer = (
            f"verified: integral K dA = {pi_text(total_coeff)} = "
            f"2pi chi"
        )
        problem = (
            f"Verify Gauss-Bonnet for a flat rectangular torus of width "
            f"{width} and height {height}, with Euler characteristic 0."
        )
        return problem, steps, answer
