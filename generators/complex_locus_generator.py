import random

from base_generator import ProblemGenerator
from helpers import step, jid


def point_text(point):
    return f"({point[0]},{point[1]})"


def square_binomial(var, value):
    if value == 0:
        return f"{var}^2"
    if value > 0:
        return f"({var} - {value})^2"
    return f"({var} + {-value})^2"


def line_text(a, b, c):
    parts = []
    for coef, var in ((a, "x"), (b, "y")):
        if coef == 0:
            continue
        abs_coef = abs(coef)
        term = var if abs_coef == 1 else f"{abs_coef}{var}"
        if not parts:
            parts.append(term if coef > 0 else f"-{term}")
        else:
            parts.append(f"+ {term}" if coef > 0 else f"- {term}")
    if c != 0:
        if not parts:
            parts.append(str(c))
        else:
            parts.append(f"+ {c}" if c > 0 else f"- {-c}")
    return " ".join(parts) + " = 0"


class ComplexLocusGenerator(ProblemGenerator):
    """
    Complex loci converted to Cartesian equations.

    Variants:
    - circle: |z-a| = r
    - bisector: |z-a| = |z-b|

    Op-codes used:
    - LOCUS_SETUP / DIST_FORMULA / EXPAND / CANCEL: locus translation
    - CIRCLE_EQ / LINE_EQ: final Cartesian equation
    - E / A / S / M (established/shared): coefficient arithmetic
    - Z: equation and locus type
    """

    VARIANTS = ["circle", "bisector"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "circle":
            problem, steps, answer = self._generate_circle()
        else:
            problem, steps, answer = self._generate_bisector()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"complex_locus_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_circle(self):
        center = (random.randint(-6, 6), random.randint(-6, 6))
        radius = random.randint(1, 9)
        r2 = radius * radius
        equation = (
            f"{square_binomial('x', center[0])} + "
            f"{square_binomial('y', center[1])} = {r2}"
        )
        steps = [
            step("LOCUS_SETUP", f"z=x+iy", f"center={point_text(center)}",
                 f"radius={radius}"),
            step("DIST_FORMULA",
                 f"sqrt({square_binomial('x', center[0])}+"
                 f"{square_binomial('y', center[1])})={radius}"),
            step("E", radius, 2, r2),
            step("CIRCLE_EQ", equation),
        ]
        answer = (
            f"{equation}; type = circle; center = {point_text(center)}; "
            f"radius = {radius}"
        )
        problem = (
            f"Identify the locus |z - {point_text(center)}| = {radius}, "
            "where z=x+iy. Give the Cartesian equation and type."
        )
        return problem, steps, answer

    def _generate_bisector(self):
        while True:
            p = (random.randint(-5, 5), random.randint(-5, 5))
            q = (random.randint(-5, 5), random.randint(-5, 5))
            if p != q:
                break
        dx = q[0] - p[0]
        dy = q[1] - p[1]
        a = 2 * dx
        b = 2 * dy
        p_norm = p[0] * p[0] + p[1] * p[1]
        q_norm = q[0] * q[0] + q[1] * q[1]
        c = p_norm - q_norm
        equation = line_text(a, b, c)
        steps = [
            step("LOCUS_SETUP", "z=x+iy", f"p={point_text(p)}",
                 f"q={point_text(q)}"),
            step("DIST_FORMULA",
                 f"{square_binomial('x', p[0])}+"
                 f"{square_binomial('y', p[1])} = "
                 f"{square_binomial('x', q[0])}+"
                 f"{square_binomial('y', q[1])}"),
            step("EXPAND", "cancel x^2 and y^2"),
            step("S", q[0], p[0], dx),
            step("M", 2, dx, a),
            step("S", q[1], p[1], dy),
            step("M", 2, dy, b),
            step("E", p[0], 2, p[0] * p[0]),
            step("E", p[1], 2, p[1] * p[1]),
            step("A", p[0] * p[0], p[1] * p[1], p_norm),
            step("E", q[0], 2, q[0] * q[0]),
            step("E", q[1], 2, q[1] * q[1]),
            step("A", q[0] * q[0], q[1] * q[1], q_norm),
            step("S", p_norm, q_norm, c),
            step("LINE_EQ", equation),
        ]
        answer = f"{equation}; type = line"
        problem = (
            f"Identify the locus |z - {point_text(p)}| = "
            f"|z - {point_text(q)}|, where z=x+iy. Give the Cartesian "
            "equation and type."
        )
        return problem, steps, answer
