import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def point_text(points):
    return ", ".join(f"({x},{y})" for x, y in points)


class InterpolationGenerator(ProblemGenerator):
    """
    Three-point polynomial interpolation by Lagrange and Newton forms.

    Points are sampled from a small quadratic, but the prompt only supplies
    the points and target x-value. All interpolation arithmetic is exact.

    Op-codes used:
    - INTERP_SETUP: method, points, and target x
    - LAGRANGE_FACTOR / NEWTON_DD: identify table factors/differences
    - M / A / S / D (established/shared): exact interpolation arithmetic
    - Z: interpolated value
    """

    VARIANTS = ["lagrange", "newton"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        points, target = self._sample_points()
        if variant == "lagrange":
            problem, steps, answer = self._generate_lagrange(points, target)
        else:
            problem, steps, answer = self._generate_newton(points, target)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"interpolation_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _sample_points(self):
        a = random.randint(-3, 3)
        b = random.randint(-5, 5)
        c = random.randint(-8, 8)
        if a == 0 and b == 0:
            a = 1
        xs = sorted(random.sample(range(-5, 6), 3))
        target_choices = [x for x in range(-6, 7) if x not in xs]
        target = random.choice(target_choices)
        points = [(x, a * x * x + b * x + c) for x in xs]
        return points, target

    def _generate_lagrange(self, points, target):
        steps = [
            step("INTERP_SETUP", "lagrange", f"points={point_text(points)}",
                 f"x={target}"),
        ]
        terms = []
        for i, (x_i, y_i) in enumerate(points):
            basis = Fraction(1)
            for j, (x_j, _) in enumerate(points):
                if i == j:
                    continue
                numerator = target - x_j
                denominator = x_i - x_j
                factor = Fraction(numerator, denominator)
                steps.extend([
                    step("S", target, x_j, numerator),
                    step("S", x_i, x_j, denominator),
                    step("D", numerator, denominator, fraction_text(factor)),
                    step("LAGRANGE_FACTOR", f"L_{i}", f"j={j}",
                         fraction_text(factor)),
                    step("M", fraction_text(basis), fraction_text(factor),
                         fraction_text(basis * factor)),
                ])
                basis *= factor
            term = y_i * basis
            terms.append(term)
            steps.append(step("M", y_i, fraction_text(basis),
                              fraction_text(term)))
        total = Fraction(0)
        for term in terms:
            next_total = total + term
            steps.append(step("A", fraction_text(total),
                              fraction_text(term), fraction_text(next_total)))
            total = next_total
        answer = f"P({target}) = {fraction_text(total)}"
        problem = (
            f"Use Lagrange interpolation through points {point_text(points)} "
            f"to find P({target})."
        )
        return problem, steps, answer

    def _generate_newton(self, points, target):
        (x0, y0), (x1, y1), (x2, y2) = points
        steps = [
            step("INTERP_SETUP", "newton", f"points={point_text(points)}",
                 f"x={target}"),
        ]
        dy01 = y1 - y0
        dx01 = x1 - x0
        dd01 = Fraction(dy01, dx01)
        dy12 = y2 - y1
        dx12 = x2 - x1
        dd12 = Fraction(dy12, dx12)
        diff_dd = dd12 - dd01
        dx02 = x2 - x0
        dd012 = diff_dd / dx02
        steps.extend([
            step("S", y1, y0, dy01),
            step("S", x1, x0, dx01),
            step("D", dy01, dx01, fraction_text(dd01)),
            step("NEWTON_DD", "f[x0,x1]", fraction_text(dd01)),
            step("S", y2, y1, dy12),
            step("S", x2, x1, dx12),
            step("D", dy12, dx12, fraction_text(dd12)),
            step("NEWTON_DD", "f[x1,x2]", fraction_text(dd12)),
            step("S", fraction_text(dd12), fraction_text(dd01),
                 fraction_text(diff_dd)),
            step("S", x2, x0, dx02),
            step("D", fraction_text(diff_dd), dx02, fraction_text(dd012)),
            step("NEWTON_DD", "f[x0,x1,x2]", fraction_text(dd012)),
        ])
        x_minus_x0 = target - x0
        x_minus_x1 = target - x1
        linear_term = dd01 * x_minus_x0
        product = x_minus_x0 * x_minus_x1
        quad_term = dd012 * product
        partial = Fraction(y0) + linear_term
        total = partial + quad_term
        steps.extend([
            step("S", target, x0, x_minus_x0),
            step("M", fraction_text(dd01), x_minus_x0,
                 fraction_text(linear_term)),
            step("S", target, x1, x_minus_x1),
            step("M", x_minus_x0, x_minus_x1, product),
            step("M", fraction_text(dd012), product,
                 fraction_text(quad_term)),
            step("A", y0, fraction_text(linear_term),
                 fraction_text(partial)),
            step("A", fraction_text(partial), fraction_text(quad_term),
                 fraction_text(total)),
        ])
        answer = f"P({target}) = {fraction_text(total)}"
        problem = (
            f"Use Newton divided differences through points "
            f"{point_text(points)} to find P({target})."
        )
        return problem, steps, answer
