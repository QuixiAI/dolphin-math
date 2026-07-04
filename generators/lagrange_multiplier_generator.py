import random

from base_generator import ProblemGenerator
from helpers import step, jid


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


def fmt_power(var, exp):
    if exp == 0:
        return ""
    return var if exp == 1 else f"{var}^{exp}"


def fmt_monomial(coeff, powers):
    factors = []
    if coeff != 1:
        factors.append(str(coeff))
    for var, exp in powers:
        rendered = fmt_power(var, exp)
        if rendered:
            factors.append(rendered)
    return "*".join(factors) if factors else str(coeff)


def quadratic_objective(a, b):
    return fmt_linear([(a, "x^2"), (b, "y^2")])


def scaled_value(coeff, value):
    return str(value) if coeff == 1 else f"{coeff}*{value}"


def ratio_value(coeff, total, denom):
    top = str(total) if coeff == 1 else f"{coeff}*{total}"
    return f"{top}/{denom}"


def lambda_ratio(lam, coeff, denom):
    top = str(lam) if coeff == 1 else f"{lam}*{coeff}"
    return f"{top}/{denom}"


def lambda_symbol_ratio(coeff, denom):
    top = "lambda" if coeff == 1 else f"lambda*{coeff}"
    return f"{top}/{denom}"


def power_value(value, exp):
    return str(value) if exp == 1 else f"{value}^{exp}"


def product_eval(x0, m, y0, n):
    return f"{power_value(x0, m)}*{power_value(y0, n)}"


def product_objective(m, n):
    return fmt_monomial(1, [("x", m), ("y", n)])


class LagrangeMultiplierGenerator(ProblemGenerator):
    """
    One-constraint Lagrange multiplier computations with exact integer
    optimizers.

    Variants:
    - quadratic_line: minimize a*x^2 + b*y^2 subject to p*x + q*y = r
    - product_sum:    maximize x^m*y^n subject to x + y = S, x,y > 0

    Op-codes used:
    - LAGRANGE_SETUP: objective, constraint, and goal
    - PARTIAL_RESULT / GRAD_RESULT (established): objective and constraint
      gradients
    - LAGRANGE_EQ: multiplier equations and rearrangements
    - CONSTRAINT_SUBST: substitute multiplier relations into the constraint
    - POINT_FROM_LAMBDA: compute coordinates from lambda
    - ELIMINATE_LAMBDA: equate multiplier equations
    - RATIO: solve the coordinate ratio
    - EVAL / CHECK (established): objective value and constraint check
    - Z: optimizer and optimum value
    """

    VARIANTS = ["quadratic_line", "product_sum"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "quadratic_line":
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            p = random.randint(1, 5)
            q = random.randint(1, 5)
            k = random.randint(1, 5)
            lam = 2 * a * b * k
            x0 = lam * p // (2 * a)
            y0 = lam * q // (2 * b)
            r = p * x0 + q * y0
            value = a * x0 * x0 + b * y0 * y0
            f_txt = quadratic_objective(a, b)
            g_txt = f"{fmt_linear([(p, 'x'), (q, 'y')])} = {r}"
            answer = f"minimum at ({x0}, {y0}); value {value}"
            steps = [
                step("LAGRANGE_SETUP", f"f(x,y) = {f_txt}",
                     f"constraint {g_txt}", "minimize"),
                step("PARTIAL_RESULT", "f_x", f"{2 * a}*x"),
                step("PARTIAL_RESULT", "f_y", f"{2 * b}*y"),
                step("GRAD_RESULT", "grad g", f"({p}, {q})"),
                step("LAGRANGE_EQ", f"{2 * a}*x = lambda*{p}",
                     f"x = {lambda_symbol_ratio(p, 2 * a)}"),
                step("LAGRANGE_EQ", f"{2 * b}*y = lambda*{q}",
                     f"y = {lambda_symbol_ratio(q, 2 * b)}"),
                step("CONSTRAINT_SUBST", g_txt,
                     f"lambda*({p * p}/{2 * a} + {q * q}/{2 * b}) = {r}",
                     f"lambda = {lam}"),
                step("POINT_FROM_LAMBDA", "x",
                     lambda_ratio(lam, p, 2 * a), x0),
                step("POINT_FROM_LAMBDA", "y",
                     lambda_ratio(lam, q, 2 * b), y0),
                step("EVAL", f"f({x0},{y0})",
                     f"{scaled_value(a, f'{x0}^2')} + "
                     f"{scaled_value(b, f'{y0}^2')}", value),
                step("CHECK", "constraint",
                     f"{scaled_value(p, x0)} + {scaled_value(q, y0)} = {r}",
                     "satisfied"),
                step("Z", answer),
            ]
            problem = (
                f"Minimize f(x,y) = {f_txt} subject to {g_txt} using "
                f"Lagrange multipliers."
            )
        else:
            m = random.randint(1, 3)
            n = random.randint(1, 3)
            scale = random.randint(2, 7)
            total = (m + n) * scale
            x0 = m * scale
            y0 = n * scale
            value = (x0 ** m) * (y0 ** n)
            f_txt = product_objective(m, n)
            fx_txt = fmt_monomial(m, [("x", m - 1), ("y", n)])
            fy_txt = fmt_monomial(n, [("x", m), ("y", n - 1)])
            left = fmt_linear([(m, "y")])
            right = fmt_linear([(n, "x")])
            if m == n:
                ratio = "y = x"
            elif m == 1:
                ratio = f"y = {fmt_linear([(n, 'x')])}"
            elif n == 1:
                ratio = f"y = x/{m}"
            else:
                ratio = f"y = {n}/{m}*x"
            answer = f"maximum at ({x0}, {y0}); value {value}"
            steps = [
                step("LAGRANGE_SETUP", f"f(x,y) = {f_txt}",
                     f"constraint x + y = {total}", "maximize"),
                step("PARTIAL_RESULT", "f_x", fx_txt),
                step("PARTIAL_RESULT", "f_y", fy_txt),
                step("GRAD_RESULT", "grad g", "(1, 1)"),
                step("LAGRANGE_EQ", "f_x = lambda", fx_txt),
                step("LAGRANGE_EQ", "f_y = lambda", fy_txt),
                step("ELIMINATE_LAMBDA", "f_x = f_y",
                     f"{left} = {right}"),
                step("RATIO", f"{left} = {right}", ratio),
                step("CONSTRAINT_SUBST", f"x + y = {total}",
                     f"x = {ratio_value(m, total, m + n)}", x0),
                step("CONSTRAINT_SUBST", f"x + y = {total}",
                     f"y = {ratio_value(n, total, m + n)}", y0),
                step("EVAL", f"f({x0},{y0})",
                     product_eval(x0, m, y0, n), value),
                step("CHECK", "boundary",
                     "product is 0 at x = 0 or y = 0",
                     "interior maximum"),
                step("Z", answer),
            ]
            problem = (
                f"Maximize f(x,y) = {f_txt} subject to x + y = {total}, "
                f"with x > 0 and y > 0, using Lagrange multipliers."
            )

        return dict(
            problem_id=jid(),
            operation=f"lagrange_multiplier_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
