import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def point_text(x_value, y_value):
    return f"({fraction_text(x_value)},{fraction_text(y_value)})"


class GradientDescentGenerator(ProblemGenerator):
    """
    Fixed-step gradient descent on diagonal quadratic bowls.

    Op-codes used:
    - GD_SETUP: function, start point, step size, iteration count
    - GRADIENT_FORMULA: gradient for the quadratic
    - ITERATE: new point after an update
    - A / S / M / D / E (established/shared): exact arithmetic
    - Z: final point and objective value
    """

    STEPS = 3

    def generate(self) -> dict:
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        eta_den = max(a, b) + random.randint(2, 8)
        eta = Fraction(1, eta_den)
        x = Fraction(random.choice([v for v in range(-10, 11) if v != 0]))
        y = Fraction(random.choice([v for v in range(-10, 11) if v != 0]))
        start_x = x
        start_y = y

        steps = [
            step("GD_SETUP", f"f(x,y)=1/2*({a}x^2+{b}y^2)",
                 f"start={point_text(x, y)}", f"eta={fraction_text(eta)}"),
            step("GRADIENT_FORMULA", f"grad=({a}x,{b}y)"),
        ]
        for index in range(1, self.STEPS + 1):
            grad_x = a * x
            grad_y = b * y
            update_x = eta * grad_x
            update_y = eta * grad_y
            new_x = x - update_x
            new_y = y - update_y
            steps += [
                step("M", a, fraction_text(x), fraction_text(grad_x)),
                step("M", b, fraction_text(y), fraction_text(grad_y)),
                step("M", fraction_text(eta), fraction_text(grad_x),
                     fraction_text(update_x)),
                step("S", fraction_text(x), fraction_text(update_x),
                     fraction_text(new_x)),
                step("M", fraction_text(eta), fraction_text(grad_y),
                     fraction_text(update_y)),
                step("S", fraction_text(y), fraction_text(update_y),
                     fraction_text(new_y)),
                step("ITERATE", f"k={index}", point_text(new_x, new_y)),
            ]
            x, y = new_x, new_y

        x_sq = x ** 2
        y_sq = y ** 2
        ax_sq = a * x_sq
        by_sq = b * y_sq
        doubled_value = ax_sq + by_sq
        value = doubled_value / 2
        steps += [
            step("E", fraction_text(x), 2, fraction_text(x_sq)),
            step("M", a, fraction_text(x_sq), fraction_text(ax_sq)),
            step("E", fraction_text(y), 2, fraction_text(y_sq)),
            step("M", b, fraction_text(y_sq), fraction_text(by_sq)),
            step("A", fraction_text(ax_sq), fraction_text(by_sq),
                 fraction_text(doubled_value)),
            step("D", fraction_text(doubled_value), 2, fraction_text(value)),
        ]
        answer = (
            f"x_3={fraction_text(x)}, y_3={fraction_text(y)}, "
            f"f(x_3,y_3)={fraction_text(value)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Starting at {point_text(start_x, start_y)} "
            f"for f(x,y)=1/2*({a}x^2+{b}y^2), run 3 gradient-descent "
            f"steps with step size eta={fraction_text(eta)}."
        )
        return dict(
            problem_id=jid(),
            operation="gradient_descent_quadratic",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
