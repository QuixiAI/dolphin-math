import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


SPHERE_POINTS = {
    45: {
        "sin": "sqrt(2)/2",
        "cos": "sqrt(2)/2",
        "sin_cos": "1/2",
        "gamma_phi": "-1/2",
        "cot": "1",
    },
    90: {
        "sin": "1",
        "cos": "0",
        "sin_cos": "0",
        "gamma_phi": "0",
        "cot": "0",
    },
}


def fraction_text(value):
    return str(Fraction(value))


class ChristoffelGenerator(ProblemGenerator):
    """
    Christoffel symbols for hand-friendly 2D diagonal metrics.

    Variants:
    - polar: ds^2 = dr^2 + r^2 dtheta^2, evaluated at r=a.
    - sphere: ds^2 = R^2 dphi^2 + R^2 sin^2(phi)dtheta^2,
      evaluated at a supplied phi.

    Op-codes used:
    - CHRISTOFFEL_SETUP / INVERSE_METRIC / CHRISTOFFEL_FORMULA /
      DERIV / TRIG_VALUE
    - E / M / D (established/shared): exact arithmetic
    - Z: nonzero Christoffel symbols
    """

    VARIANTS = ["polar", "sphere"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "polar":
            problem, steps, answer = self._generate_polar()
        else:
            problem, steps, answer = self._generate_sphere()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"christoffel_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_polar(self):
        radius = random.randint(2, 100)
        radius_sq = radius * radius
        two_r = 2 * radius
        gamma_r = -radius
        inv_rr = Fraction(1, radius_sq)
        temp = inv_rr * two_r
        gamma_theta = temp / 2
        steps = [
            step("CHRISTOFFEL_SETUP", "polar",
                 "g_rr=1, g_thetatheta=r^2", f"r={radius}"),
            step("INVERSE_METRIC", "g^rr=1",
                 "g^thetatheta=1/r^2"),
            step("CHRISTOFFEL_FORMULA",
                 "Gamma^i_jk = 1/2 g^im(d_j g_mk + d_k g_mj - d_m g_jk)"),
            step("DERIV", "d_r g_thetatheta = 2r", f"at r={radius}",
                 two_r),
            step("M", "-1/2", two_r, gamma_r),
            step("E", radius, 2, radius_sq),
            step("D", 1, radius_sq, fraction_text(inv_rr)),
            step("M", fraction_text(inv_rr), two_r, fraction_text(temp)),
            step("D", fraction_text(temp), 2, fraction_text(gamma_theta)),
        ]
        answer = (
            f"Gamma^r_thetatheta = {gamma_r}, "
            f"Gamma^theta_rtheta = Gamma^theta_thetar = "
            f"{fraction_text(gamma_theta)}"
        )
        problem = (
            f"For the polar metric ds^2 = dr^2 + r^2 dtheta^2, compute "
            f"the nonzero Christoffel symbols at r={radius}."
        )
        return problem, steps, answer

    def _generate_sphere(self):
        radius = random.randint(2, 150)
        phi = random.choice(sorted(SPHERE_POINTS))
        values = SPHERE_POINTS[phi]
        radius_sq = radius * radius
        steps = [
            step("CHRISTOFFEL_SETUP", "sphere",
                 "g_phiphi=R^2, g_thetatheta=R^2 sin^2(phi)",
                 f"R={radius}, phi={phi} deg"),
            step("INVERSE_METRIC", "g^phiphi=1/R^2",
                 "g^thetatheta=1/(R^2 sin^2(phi))"),
            step("CHRISTOFFEL_FORMULA",
                 "Gamma^i_jk = 1/2 g^im(d_j g_mk + d_k g_mj - d_m g_jk)"),
            step("E", radius, 2, radius_sq),
            step("TRIG_VALUE", f"sin(phi)={values['sin']}",
                 f"cos(phi)={values['cos']}"),
            step("DERIV", "d_phi g_thetatheta",
                 "2R^2 sin(phi)cos(phi)"),
            step("M", values["sin"], values["cos"], values["sin_cos"]),
            step("M", -1, values["sin_cos"], values["gamma_phi"]),
            step("D", values["cos"], values["sin"], values["cot"]),
        ]
        answer = (
            f"Gamma^phi_thetatheta = {values['gamma_phi']}, "
            f"Gamma^theta_phitheta = Gamma^theta_thetaphi = "
            f"{values['cot']}"
        )
        problem = (
            f"For the sphere metric ds^2 = R^2 dphi^2 + R^2 sin^2(phi) "
            f"dtheta^2 with R={radius}, compute the nonzero Christoffel "
            f"symbols at phi={phi} deg. Given sin(phi)={values['sin']} "
            f"and cos(phi)={values['cos']}."
        )
        return problem, steps, answer
