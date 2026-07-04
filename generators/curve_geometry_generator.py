import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def fmt_linear(coeff, const):
    if coeff == 0:
        return str(const)
    term = "t" if abs(coeff) == 1 else f"{abs(coeff)}*t"
    first = term if coeff > 0 else f"-{term}"
    if const == 0:
        return first
    return f"{first} {'+' if const > 0 else '-'} {abs(const)}"


def factor_text(value):
    return f"({value})" if value < 0 else str(value)


class CurveGeometryGenerator(ProblemGenerator):
    """
    Curve geometry: arc length, curvature, unit tangent, and unit normal.

    Variants:
    - arc_line: arc length of a constant-speed parametric line
    - circle_tn: curvature and unit tangent/normal for a circle at t=0

    Op-codes used:
    - CURVE_GEOM_SETUP: curve and target
    - PATH_DERIV (established): r'(t)
    - SPEED: compute |r'(t)|
    - ARC_LENGTH: integrate speed
    - CURVATURE_FORMULA: formula used for circle curvature
    - UNIT_TANGENT / UNIT_NORMAL: normalized vectors
    - Z: final curve-geometry result
    """

    VARIANTS = ["arc_line", "circle_tn"]
    TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "arc_line":
            a, c, speed = random.choice(self.TRIPLES)
            if random.choice([True, False]):
                a = -a
            if random.choice([True, False]):
                c = -c
            b = random.randint(-8, 8)
            d = random.randint(-8, 8)
            t_end = random.randint(2, 12)
            x_t = fmt_linear(a, b)
            y_t = fmt_linear(c, d)
            length = speed * t_end
            steps = [
                step("CURVE_GEOM_SETUP", f"r(t) = <{x_t}, {y_t}>",
                     f"0 <= t <= {t_end}", "arc length"),
                step("PATH_DERIV", "r'(t)", f"<{a}, {c}>"),
                step("SPEED", "sqrt(a^2 + b^2)",
                     f"sqrt({factor_text(a)}^2 + {factor_text(c)}^2)",
                     speed),
                step("ARC_LENGTH", "int_0^T speed dt",
                     f"{speed}*{t_end}", length),
                step("Z", f"arc length {length}"),
            ]
            answer = f"arc length {length}"
            problem = (
                f"Find the arc length of r(t) = <{x_t}, {y_t}> for "
                f"0 <= t <= {t_end}."
            )
        else:
            radius = random.randint(2, 20)
            curvature = fmt_frac(Fraction(1, radius))
            answer = (
                f"curvature {curvature}; T(0)=<0, 1>; N(0)=<-1, 0>"
            )
            steps = [
                step("CURVE_GEOM_SETUP",
                     f"r(t) = <{radius}*cos(t), {radius}*sin(t)>",
                     "at t = 0", "curvature, T, N"),
                step("PATH_DERIV", "r'(t)",
                     f"<-{radius}*sin(t), {radius}*cos(t)>"),
                step("SPEED", "norm r'(0)", radius),
                step("UNIT_TANGENT", "r'(0)/speed", "<0, 1>"),
                step("CURVATURE_FORMULA", "circle", "kappa = 1/R"),
                step("UNIT_NORMAL", "T'(0)/norm T'(0)", "<-1, 0>"),
                step("Z", answer),
            ]
            problem = (
                f"For r(t) = <{radius}*cos(t), {radius}*sin(t)>, "
                f"find curvature, unit tangent, and unit normal at t = 0."
            )

        return dict(
            problem_id=jid(),
            operation=f"curve_geometry_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
