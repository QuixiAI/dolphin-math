import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.parabola_features_generator import shift


def wrap(n):
    return f"({n})" if n < 0 else str(n)


class CircleEquationGenerator(ProblemGenerator):
    """
    Equation of a circle in standard form, from three kinds of given
    information. (The general-form-to-standard direction lives in
    ConicStandardFormGenerator.)

    Variants:
    - center_radius: read off (x-h)^2 + (y-k)^2 = r^2
    - center_point:  r^2 computed as the squared distance to the point
    - diameter:      center from the midpoint, r^2 from the squared
                     distance to one endpoint

    Op-codes used:
    - CIRCLE_SETUP: the given data and the goal (given, goal)
    - MID_FORMULA / A / D: midpoint work (established)
    - CENTER: the center (established)
    - S / E: deltas and squares (established)
    - EVAL: r^2 (established)
    - REWRITE / Z: the equation (established)
    """

    VARIANTS = ["center_radius", "center_point", "diameter"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _r2_steps(steps, cx, cy, px, py):
        dx, dy = px - cx, py - cy
        steps.append(step("S", px, cx, dx))
        steps.append(step("S", py, cy, dy))
        steps.append(step("E", wrap(dx), 2, dx * dx))
        steps.append(step("E", wrap(dy), 2, dy * dy))
        steps.append(step("A", dx * dx, dy * dy, dx * dx + dy * dy))
        steps.append(step("EVAL", "r^2", dx * dx + dy * dy))
        return dx * dx + dy * dy

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        h = random.randint(-6, 6)
        k = random.randint(-6, 6)

        if variant == "center_radius":
            r = random.randint(1, 9)
            r2 = r * r
            steps = [
                step("CIRCLE_SETUP", f"center ({h}, {k}), radius {r}",
                     "equation of the circle"),
                step("E", r, 2, r2),
            ]
            problem = (f"Write the equation of the circle with center "
                       f"({h}, {k}) and radius {r}.")
        elif variant == "center_point":
            dx = random.choice([v for v in range(-6, 7) if v != 0])
            dy = random.choice([v for v in range(-6, 7) if v != 0])
            px, py = h + dx, k + dy
            steps = [step("CIRCLE_SETUP",
                          f"center ({h}, {k}), passes through "
                          f"({px}, {py})", "equation of the circle")]
            r2 = self._r2_steps(steps, h, k, px, py)
            problem = (f"Write the equation of the circle with center "
                       f"({h}, {k}) that passes through ({px}, {py}).")
        else:
            dx = random.choice([v for v in range(-5, 6) if v != 0])
            dy = random.choice([v for v in range(-5, 6) if v != 0])
            x1, y1 = h - dx, k - dy
            x2, y2 = h + dx, k + dy
            steps = [
                step("CIRCLE_SETUP",
                     f"diameter endpoints ({x1}, {y1}) and ({x2}, {y2})",
                     "equation of the circle"),
                step("MID_FORMULA", "center = midpoint of the diameter"),
                step("A", x1, x2, x1 + x2),
                step("D", x1 + x2, 2, h),
                step("A", y1, y2, y1 + y2),
                step("D", y1 + y2, 2, k),
                step("CENTER", f"({h}, {k})"),
            ]
            r2 = self._r2_steps(steps, h, k, x2, y2)
            problem = (f"Write the equation of the circle whose diameter "
                       f"has endpoints ({x1}, {y1}) and ({x2}, {y2}).")

        eq = f"{shift('x', h)}^2 + {shift('y', k)}^2 = {r2}"
        steps.append(step("REWRITE", eq))
        steps.append(step("Z", eq))

        return dict(
            problem_id=jid(),
            operation=f"circle_equation_{variant}",
            problem=problem,
            steps=steps,
            final_answer=eq,
        )
