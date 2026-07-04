import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def frac_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def point_text(z):
    return f"({frac_text(z[0])},{frac_text(z[1])})"


def random_half():
    return Fraction(random.randint(-3, 3), 2)


def square_plus_c(z, c):
    x, y = z
    return (x * x - y * y + c[0], 2 * x * y + c[1])


def norm_squared(z):
    return z[0] * z[0] + z[1] * z[1]


class FractalIterationGenerator(ProblemGenerator):
    """
    Mandelbrot/Julia escape iteration z <- z^2 + c with exact rational
    arithmetic and |z| > 2 checks.

    Variants:
    - mandelbrot: z0=0, varied c
    - julia: varied z0 and c

    Op-codes used:
    - FRACTAL_SETUP / ITERATE / ESCAPE_CHECK: iteration trace
    - E / M / A / S (established/shared): exact complex arithmetic
    - Z: first escape step or bounded-through-N verdict
    """

    VARIANTS = ["mandelbrot", "julia"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        iterations = random.randint(4, 6)
        if variant == "mandelbrot":
            z0 = (Fraction(0), Fraction(0))
            c = (random_half(), random_half())
        else:
            z0 = (random_half(), random_half())
            c = (random_half(), random_half())
        problem, steps, answer = self._build_problem(variant, z0, c,
                                                     iterations)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"fractal_iteration_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _build_problem(self, variant, z0, c, iterations):
        steps = [
            step("FRACTAL_SETUP", variant, f"z0={point_text(z0)}",
                 f"c={point_text(c)}", f"N={iterations}"),
        ]
        z = z0
        escaped_at = None
        for n in range(1, iterations + 1):
            z = self._trace_iteration(steps, n, z, c)
            norm2 = self._trace_norm(steps, n, z)
            verdict = "escaped" if norm2 > 4 else "bounded"
            steps.append(step("ESCAPE_CHECK", f"n={n}",
                              f"norm2={frac_text(norm2)}", verdict))
            if escaped_at is None and norm2 > 4:
                escaped_at = n
                break
        if escaped_at is None:
            answer = f"not escaped after {iterations} steps"
        else:
            answer = f"escaped at step {escaped_at}"
        problem = (
            f"Trace the {variant} iteration z <- z^2 + c for {iterations} "
            f"iterations from "
            f"z0={point_text(z0)} with c={point_text(c)}. Report the first "
            "step with |z| > 2, if any."
        )
        return problem, steps, answer

    def _trace_iteration(self, steps, n, z, c):
        x, y = z
        x2 = x * x
        y2 = y * y
        real_square = x2 - y2
        two_x = 2 * x
        imag_square = two_x * y
        real = real_square + c[0]
        imag = imag_square + c[1]
        steps.extend([
            step("E", frac_text(x), 2, frac_text(x2)),
            step("E", frac_text(y), 2, frac_text(y2)),
            step("S", frac_text(x2), frac_text(y2), frac_text(real_square)),
            step("M", 2, frac_text(x), frac_text(two_x)),
            step("M", frac_text(two_x), frac_text(y), frac_text(imag_square)),
            step("A", frac_text(real_square), frac_text(c[0]),
                 frac_text(real)),
            step("A", frac_text(imag_square), frac_text(c[1]),
                 frac_text(imag)),
            step("ITERATE", f"n={n}", f"z={point_text((real, imag))}"),
        ])
        return real, imag

    def _trace_norm(self, steps, n, z):
        x, y = z
        x2 = x * x
        y2 = y * y
        total = x2 + y2
        steps.extend([
            step("E", frac_text(x), 2, frac_text(x2)),
            step("E", frac_text(y), 2, frac_text(y2)),
            step("A", frac_text(x2), frac_text(y2), frac_text(total)),
        ])
        return total
