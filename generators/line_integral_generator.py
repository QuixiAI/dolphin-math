import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def fmt_linear(raw_terms):
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        if body:
            text = body if abs(coeff) == 1 else f"{abs(coeff)}*{body}"
        else:
            text = str(abs(coeff))
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def fmt_quadratic(a, b, c, d, e):
    return fmt_linear([
        (a, "x^2"),
        (b, "y^2"),
        (c, "x*y"),
        (d, "x"),
        (e, "y"),
    ])


def eval_phi(a, b, c, d, e, x, y):
    return a * x * x + b * y * y + c * x * y + d * x + e * y


def fmt_half_plus(coeff, const):
    first = f"{coeff}/2"
    if const == 0:
        return first
    return f"{first} {'+' if const > 0 else '-'} {abs(const)}"


def fmt_subtract(a, b):
    return f"{a} + {abs(b)}" if b < 0 else f"{a} - {b}"


class LineIntegralGenerator(ProblemGenerator):
    """
    Work line integrals and conservative-field potential functions.

    Variants:
    - segment_work: parameterize a line segment and integrate F(r(t))*r'(t)
    - potential_work: recover a potential and use endpoint subtraction

    Op-codes used:
    - LINE_SETUP: vector field and path/task
    - PARAM_PATH: path parameterization
    - PATH_DERIV: r'(t)
    - SUBST (established): substitute the path into F
    - DOT (established): F(r(t))*r'(t)
    - LINE_INTEGRAL: integrate the dot product over t
    - PARTIAL_RESULT / CHECK (established): conservative test
    - POTENTIAL_BUILD / POTENTIAL_RESULT: construct potential phi
    - EVAL / WORK_DIFF (established/new): endpoint subtraction
    - Z: final work, and potential when requested
    """

    VARIANTS = ["segment_work", "potential_work"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _points():
        while True:
            x0 = random.randint(-4, 4)
            y0 = random.randint(-4, 4)
            x1 = random.randint(-4, 4)
            y1 = random.randint(-4, 4)
            if (x0, y0) != (x1, y1):
                return x0, y0, x1, y1

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "segment_work":
            px = random.randint(-5, 5)
            py = random.randint(-5, 5)
            qx = random.randint(-5, 5)
            qy = random.randint(-5, 5)
            x0, y0, x1, y1 = self._points()
            dx = x1 - x0
            dy = y1 - y0
            p_txt = fmt_linear([(px, "x"), (py, "y")])
            q_txt = fmt_linear([(qx, "x"), (qy, "y")])
            x_t = fmt_linear([(dx, "t"), (x0, "")])
            y_t = fmt_linear([(dy, "t"), (y0, "")])
            p_t_coeff = px * dx + py * dy
            p_t_const = px * x0 + py * y0
            q_t_coeff = qx * dx + qy * dy
            q_t_const = qx * x0 + qy * y0
            p_t = fmt_linear([(p_t_coeff, "t"), (p_t_const, "")])
            q_t = fmt_linear([(q_t_coeff, "t"), (q_t_const, "")])
            dot_t_coeff = p_t_coeff * dx + q_t_coeff * dy
            dot_t_const = p_t_const * dx + q_t_const * dy
            dot_t = fmt_linear([(dot_t_coeff, "t"), (dot_t_const, "")])
            work = Fraction(dot_t_coeff, 2) + dot_t_const
            answer = f"work {fmt_frac(work)}"
            steps = [
                step("LINE_SETUP", f"F(x,y) = <{p_txt}, {q_txt}>",
                     f"from ({x0}, {y0}) to ({x1}, {y1})"),
                step("PARAM_PATH", "r(t)", f"({x_t}, {y_t})",
                     "0 <= t <= 1"),
                step("PATH_DERIV", "r'(t)", f"({dx}, {dy})"),
                step("SUBST", "F(r(t))", f"<{p_t}, {q_t}>"),
                step("DOT", "F(r(t))*r'(t)", dot_t),
                step("LINE_INTEGRAL", "int_0^1 dot dt",
                     fmt_half_plus(dot_t_coeff, dot_t_const),
                     fmt_frac(work)),
                step("Z", answer),
            ]
            problem = (
                f"Compute the work integral of F(x,y) = <{p_txt}, {q_txt}> "
                f"along the line segment from ({x0}, {y0}) to "
                f"({x1}, {y1})."
            )
        else:
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            c = random.randint(-5, 5)
            d = random.randint(-5, 5)
            e = random.randint(-5, 5)
            x0, y0, x1, y1 = self._points()
            p_txt = fmt_linear([(2 * a, "x"), (c, "y"), (d, "")])
            q_txt = fmt_linear([(2 * b, "y"), (c, "x"), (e, "")])
            phi = fmt_quadratic(a, b, c, d, e)
            start = eval_phi(a, b, c, d, e, x0, y0)
            end = eval_phi(a, b, c, d, e, x1, y1)
            work = end - start
            answer = f"potential {phi}; work {work}"
            steps = [
                step("LINE_SETUP", f"F(x,y) = <{p_txt}, {q_txt}>",
                     f"from ({x0}, {y0}) to ({x1}, {y1})"),
                step("PARTIAL_RESULT", "P_y", c),
                step("PARTIAL_RESULT", "Q_x", c),
                step("CHECK", "P_y = Q_x", f"{c} = {c}",
                     "conservative"),
                step("POTENTIAL_BUILD", "integrate P dx",
                     fmt_linear([(a, "x^2"), (c, "x*y"), (d, "x"),
                                 (1, "g(y)")]),
                     "g'(y) remains"),
                step("POTENTIAL_BUILD", "match Q",
                     f"g'(y) = {fmt_linear([(2 * b, 'y'), (e, '')])}",
                     fmt_linear([(b, "y^2"), (e, "y")])),
                step("POTENTIAL_RESULT", "phi(x,y)", phi),
                step("EVAL", f"phi({x1},{y1})", end),
                step("EVAL", f"phi({x0},{y0})", start),
                step("WORK_DIFF", "phi(end) - phi(start)",
                     fmt_subtract(end, start), work),
                step("Z", answer),
            ]
            problem = (
                f"For F(x,y) = <{p_txt}, {q_txt}>, find a potential "
                f"function and compute the work from ({x0}, {y0}) to "
                f"({x1}, {y1})."
            )

        return dict(
            problem_id=jid(),
            operation=f"line_integral_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
