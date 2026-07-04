import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def list_text(values):
    return "[" + ", ".join(fraction_text(v) for v in values) + "]"


class FiniteDifferenceGenerator(ProblemGenerator):
    """
    Finite-difference tables and derivative estimates.

    Values are sampled from small quadratics, then the prompt supplies only
    the tabular values needed for the requested difference computation.

    Op-codes used:
    - FINITE_DIFF_SETUP: method and supplied values
    - DIFF_ROW: completed finite-difference row
    - M / S / D (established/shared): exact differences and quotients
    - Z: difference row or derivative estimate
    """

    VARIANTS = ["table", "forward_derivative", "central_derivative"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "table":
            problem, steps, answer = self._generate_table()
        elif variant == "forward_derivative":
            problem, steps, answer = self._generate_forward_derivative()
        else:
            problem, steps, answer = self._generate_central_derivative()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"finite_difference_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _quadratic(self):
        a = random.randint(-3, 3)
        b = random.randint(-5, 5)
        c = random.randint(-8, 8)
        if a == 0 and b == 0:
            a = 1
        return lambda x: a * x * x + b * x + c

    def _generate_table(self):
        f = self._quadratic()
        start = random.randint(-4, 2)
        h = random.randint(1, 3)
        xs = [start + i * h for i in range(4)]
        ys = [f(x) for x in xs]
        first = [ys[i + 1] - ys[i] for i in range(3)]
        second = [first[i + 1] - first[i] for i in range(2)]
        steps = [
            step("FINITE_DIFF_SETUP", "table", f"x={list_text(xs)}",
                 f"y={list_text(ys)}"),
        ]
        for i in range(3):
            steps.append(step("S", ys[i + 1], ys[i], first[i]))
        steps.append(step("DIFF_ROW", "Delta y", list_text(first)))
        for i in range(2):
            steps.append(step("S", first[i + 1], first[i], second[i]))
        steps.append(step("DIFF_ROW", "Delta2 y", list_text(second)))
        answer = f"Delta y = {list_text(first)}; Delta2 y = {list_text(second)}"
        problem = (
            f"Build the forward-difference table for x={list_text(xs)} "
            f"and y={list_text(ys)} through second differences."
        )
        return problem, steps, answer

    def _generate_forward_derivative(self):
        f = self._quadratic()
        x0 = random.randint(-5, 5)
        h = random.randint(1, 4)
        y0 = f(x0)
        y1 = f(x0 + h)
        numerator = y1 - y0
        derivative = Fraction(numerator, h)
        steps = [
            step("FINITE_DIFF_SETUP", "forward_derivative",
                 f"x0={x0},h={h}", f"f0={y0},f1={y1}"),
            step("S", y1, y0, numerator),
            step("D", numerator, h, fraction_text(derivative)),
        ]
        answer = f"forward f'({x0}) = {fraction_text(derivative)}"
        problem = (
            f"Use the forward difference with h={h}, f({x0})={y0}, "
            f"and f({x0 + h})={y1} to estimate f'({x0})."
        )
        return problem, steps, answer

    def _generate_central_derivative(self):
        f = self._quadratic()
        x0 = random.randint(-5, 5)
        h = random.randint(1, 4)
        left_x = x0 - h
        right_x = x0 + h
        left_y = f(left_x)
        right_y = f(right_x)
        numerator = right_y - left_y
        denominator = 2 * h
        derivative = Fraction(numerator, denominator)
        steps = [
            step("FINITE_DIFF_SETUP", "central_derivative",
                 f"x0={x0},h={h}", f"f-={left_y},f+={right_y}"),
            step("S", right_y, left_y, numerator),
            step("M", 2, h, denominator),
            step("D", numerator, denominator, fraction_text(derivative)),
        ]
        answer = f"central f'({x0}) = {fraction_text(derivative)}"
        problem = (
            f"Use the central difference with h={h}, f({left_x})={left_y}, "
            f"and f({right_x})={right_y} to estimate f'({x0})."
        )
        return problem, steps, answer
