import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


SPHERE_POINTS = {
    45: {
        "sin_sq": Fraction(1, 2),
        "cos_sq": Fraction(1, 2),
        "gamma_phi": Fraction(-1, 2),
        "gamma_theta": Fraction(1),
        "deriv_gamma": Fraction(0),
    },
    90: {
        "sin_sq": Fraction(1),
        "cos_sq": Fraction(0),
        "gamma_phi": Fraction(0),
        "gamma_theta": Fraction(0),
        "deriv_gamma": Fraction(1),
    },
}


def fraction_text(value):
    return str(Fraction(value))


class RiemannTensorGenerator(ProblemGenerator):
    """
    Riemann -> Ricci -> scalar curvature for a 2-sphere.

    Uses the Christoffel-symbol sphere cases from ChristoffelGenerator:
    Gamma^phi_thetatheta = -sin(phi)cos(phi) and
    Gamma^theta_phitheta = cot(phi).

    Op-codes used:
    - RIEMANN_SETUP / CHRISTOFFEL_VALUE / DERIV / RIEMANN_ENTRY
    - RICCI_ENTRY / INVERSE_METRIC / CHECK
    - E / M / D / S / A (established/shared): exact arithmetic
    - Z: scalar curvature
    """

    def generate(self) -> dict:
        radius = random.randint(2, 150)
        phi = random.choice(sorted(SPHERE_POINTS))
        values = SPHERE_POINTS[phi]
        radius_sq = radius ** 2
        inv_radius_sq = Fraction(1, radius_sq)
        gamma_product = values["gamma_phi"] * values["gamma_theta"]
        riemann_phi = values["deriv_gamma"] - gamma_product
        ricci_phiphi = Fraction(1)
        ricci_thetatheta = riemann_phi
        scalar = 2 * inv_radius_sq
        steps = [
            step("RIEMANN_SETUP", "sphere", f"R={radius}",
                 f"phi={phi} deg"),
            step("CHRISTOFFEL_VALUE", "Gamma^phi_thetatheta",
                 fraction_text(values["gamma_phi"])),
            step("CHRISTOFFEL_VALUE", "Gamma^theta_phitheta",
                 fraction_text(values["gamma_theta"])),
            step("DERIV", "d_phi Gamma^phi_thetatheta",
                 fraction_text(values["deriv_gamma"])),
            step("M", fraction_text(values["gamma_phi"]),
                 fraction_text(values["gamma_theta"]),
                 fraction_text(gamma_product)),
            step("S", fraction_text(values["deriv_gamma"]),
                 fraction_text(gamma_product), fraction_text(riemann_phi)),
            step("RIEMANN_ENTRY", "R^phi_theta phi theta",
                 fraction_text(riemann_phi)),
            step("RIEMANN_ENTRY", "R^theta_phi theta phi", "1"),
            step("RICCI_ENTRY", "R_phiphi", "1"),
            step("RICCI_ENTRY", "R_thetatheta",
                 fraction_text(ricci_thetatheta)),
            step("E", radius, 2, radius_sq),
            step("D", 1, radius_sq, fraction_text(inv_radius_sq)),
            step("INVERSE_METRIC", "g^phiphi=1/R^2",
                 "g^thetatheta=1/(R^2 sin^2(phi))"),
            step("CHECK", "g^thetatheta R_thetatheta",
                 fraction_text(inv_radius_sq), "sin^2 cancels"),
            step("A", fraction_text(inv_radius_sq),
                 fraction_text(inv_radius_sq), fraction_text(scalar)),
        ]
        answer = f"scalar curvature = {fraction_text(scalar)}"
        steps.append(step("Z", answer))
        problem = (
            f"For a 2-sphere of radius R={radius} at phi={phi} deg with "
            f"sin^2(phi)={fraction_text(values['sin_sq'])} and "
            f"cos^2(phi)={fraction_text(values['cos_sq'])}, compute "
            "R^phi_theta phi theta, the Ricci entries, and scalar curvature."
        )
        return dict(
            problem_id=jid(),
            operation="riemann_tensor_sphere",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
