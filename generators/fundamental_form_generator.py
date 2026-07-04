import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


THETA_CHOICES = [
    Fraction(1, 6), Fraction(1, 4), Fraction(1, 3), Fraction(1, 2),
    Fraction(2, 3), Fraction(3, 4), Fraction(1, 1),
]
PHI_COS = {
    0: Fraction(1),
    60: Fraction(1, 2),
    90: Fraction(0),
    120: Fraction(-1, 2),
    180: Fraction(-1),
}


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


class FundamentalFormGenerator(ProblemGenerator):
    """
    First fundamental form coefficients and patch area for standard
    parametrized surfaces.

    Variants:
    - cylinder_patch: E=R^2, F=0, G=1 and area R*theta*h.
    - sphere_patch: E=R^2 sin^2(phi), F=0, G=R^2 and area from
      integrating R^2 sin(phi).

    Op-codes used:
    - FUNDAMENTAL_FORM_SETUP / PARTIAL / DOT / AREA_INTEGRAL
    - E / M / S / ROOT (established/shared): exact arithmetic
    - Z: first form and exact area
    """

    VARIANTS = ["cylinder_patch", "sphere_patch"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "cylinder_patch":
            problem, steps, answer = self._generate_cylinder()
        else:
            problem, steps, answer = self._generate_sphere()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"fundamental_form_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_cylinder(self):
        radius = random.randint(2, 12)
        height = random.randint(1, 12)
        theta = random.choice(THETA_CHOICES)
        radius_sq = radius * radius
        det = radius_sq
        density = radius
        radius_theta = radius * theta
        area_coeff = radius_theta * height
        area = pi_text(area_coeff)
        theta_text = pi_text(theta)
        steps = [
            step("FUNDAMENTAL_FORM_SETUP", "cylinder",
                 f"R={radius}", f"u in [0,{theta_text}], v in [0,{height}]"),
            step("PARTIAL", "r_u=(-R sin u,R cos u,0)",
                 "r_v=(0,0,1)"),
            step("E", radius, 2, radius_sq),
            step("DOT", "r_u dot r_u", radius_sq),
            step("DOT", "r_u dot r_v", 0),
            step("DOT", "r_v dot r_v", 1),
            step("M", radius_sq, 1, det),
            step("S", det, 0, det),
            step("ROOT", det, density),
            step("AREA_INTEGRAL", "sqrt(EG-F^2)=R",
                 f"area = R*theta*h"),
            step("M", radius, theta, radius_theta),
            step("M", radius_theta, height, area_coeff),
        ]
        answer = f"E = {radius_sq}, F = 0, G = 1, area = {area}"
        problem = (
            f"For the cylinder r(u,v)=({radius} cos u,{radius} sin u,v), "
            f"0<=u<={theta_text} and 0<=v<={height}, find E, F, G "
            f"and the patch area."
        )
        return problem, steps, answer

    def _generate_sphere(self):
        radius = random.randint(2, 12)
        theta = random.choice(THETA_CHOICES)
        phi1, phi2 = sorted(random.sample(list(PHI_COS), 2))
        radius_sq = radius * radius
        cos1 = PHI_COS[phi1]
        cos2 = PHI_COS[phi2]
        cos_diff = cos1 - cos2
        theta_factor = radius_sq * theta
        area_coeff = theta_factor * cos_diff
        area = pi_text(area_coeff)
        theta_text = pi_text(theta)
        e_text = f"{radius_sq}sin^2(phi)"
        steps = [
            step("FUNDAMENTAL_FORM_SETUP", "sphere",
                 f"R={radius}",
                 f"theta in [0,{theta_text}], phi in [{phi1},{phi2}]"),
            step("PARTIAL",
                 "r_theta=(-R sin phi sin theta,R sin phi cos theta,0)",
                 "r_phi=(R cos phi cos theta,R cos phi sin theta,-R sin phi)"),
            step("DOT", "r_theta dot r_theta", e_text),
            step("DOT", "r_theta dot r_phi", 0),
            step("E", radius, 2, radius_sq),
            step("DOT", "r_phi dot r_phi", radius_sq),
            step("AREA_INTEGRAL", "sqrt(EG-F^2)=R^2 sin(phi)",
                 "area = R^2*theta*(cos phi1 - cos phi2)"),
            step("S", fraction_text(cos1), fraction_text(cos2),
                 fraction_text(cos_diff)),
            step("M", radius_sq, theta, theta_factor),
            step("M", theta_factor, fraction_text(cos_diff), area_coeff),
        ]
        answer = f"E = {e_text}, F = 0, G = {radius_sq}, area = {area}"
        problem = (
            f"For the sphere r(theta,phi)=({radius} sin phi cos theta,"
            f"{radius} sin phi sin theta,{radius} cos phi), "
            f"0<=theta<={theta_text} and {phi1}<=phi<={phi2}. "
            f"Given cos({phi1})={fraction_text(cos1)} and "
            f"cos({phi2})={fraction_text(cos2)}, find E, F, G and the "
            f"patch area."
        )
        return problem, steps, answer
