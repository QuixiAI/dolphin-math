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


def fmt_quadratic(a, b, c, d, e):
    return fmt_linear([
        (a, "x^2"),
        (b, "y^2"),
        (c, "x*y"),
        (d, "x"),
        (e, "y"),
    ])


def fmt_equation(M, N):
    return f"({M}) dx + ({N}) dy = 0"


def eval_potential(a, b, c, d, e, x, y):
    return a * x * x + b * y * y + c * x * y + d * x + e * y


def fmt_eval_y_terms(b, e, y):
    return fmt_linear([(b, f"({y})^2"), (e, f"({y})")])


class ExactODEGenerator(ProblemGenerator):
    """
    Exact first-order differential equations M dx + N dy = 0.

    Variants:
    - exact_test:     compare M_y and N_x for an exact equation
    - not_exact_test: compare M_y and N_x for a non-exact equation
    - solve_exact:    recover a potential F(x,y) and use an initial condition

    Op-codes used:
    - ODE_SETUP (established): equation and task
    - PARTIAL_RESULT (established): M_y and N_x
    - CHECK (established): exact/not exact decision
    - POTENTIAL_BUILD / POTENTIAL_RESULT (established): construct F(x,y)
    - EXACT_MATCH: match F_y against N to determine g'(y)
    - D / EVAL (established): coefficient and constant arithmetic
    - Z: exactness result or implicit solution
    """

    VARIANTS = ["exact_test", "not_exact_test", "solve_exact"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _potential_params():
        return (
            random.randint(1, 5),
            random.randint(1, 5),
            random.randint(-5, 5),
            random.randint(-5, 5),
            random.randint(-5, 5),
        )

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant in {"exact_test", "solve_exact"}:
            a, b, c, d, e = self._potential_params()
            M = fmt_linear([(2 * a, "x"), (c, "y"), (d, "")])
            N = fmt_linear([(c, "x"), (2 * b, "y"), (e, "")])
            equation = fmt_equation(M, N)
            if variant == "exact_test":
                answer = f"exact because M_y = N_x = {c}"
                steps = [
                    step("ODE_SETUP", equation, "test exactness"),
                    step("PARTIAL_RESULT", "M_y", c),
                    step("PARTIAL_RESULT", "N_x", c),
                    step("CHECK", "M_y = N_x", f"{c} = {c}", "exact"),
                    step("Z", answer),
                ]
                problem = f"Test whether {equation} is exact."
            else:
                y0 = random.randint(-4, 4)
                phi = fmt_quadratic(a, b, c, d, e)
                constant = eval_potential(a, b, c, d, e, 0, y0)
                partial_F_y = fmt_linear([(c, "x"), (1, "g'(y)")])
                g_prime = fmt_linear([(2 * b, "y"), (e, "")])
                g_y = fmt_linear([(b, "y^2"), (e, "y")])
                answer = f"{phi} = {constant}"
                steps = [
                    step("ODE_SETUP", equation, f"y(0) = {y0}; solve"),
                    step("PARTIAL_RESULT", "M_y", c),
                    step("PARTIAL_RESULT", "N_x", c),
                    step("CHECK", "M_y = N_x", f"{c} = {c}", "exact"),
                    step("D", 2 * a, 2, a),
                    step("POTENTIAL_BUILD", "integrate M dx",
                         fmt_linear([(a, "x^2"), (c, "x*y"), (d, "x"),
                                     (1, "g(y)")]),
                         "g(y) remains"),
                    step("PARTIAL_RESULT", "F_y", partial_F_y),
                    step("EXACT_MATCH", "F_y = N",
                         f"{partial_F_y} = {N}"),
                    step("D", 2 * b, 2, b),
                    step("POTENTIAL_BUILD", "solve g'(y)",
                         f"g'(y) = {g_prime}", f"g(y) = {g_y}"),
                    step("POTENTIAL_RESULT", "F(x,y)", phi),
                    step("EVAL", f"F(0,{y0})", fmt_eval_y_terms(b, e, y0),
                         constant),
                    step("Z", answer),
                ]
                problem = f"Solve {equation} with y(0) = {y0}."
        else:
            ax = random.randint(1, 5)
            by = random.randint(1, 5)
            my = random.randint(-5, 5)
            nx_choices = [v for v in range(-5, 6) if v != my]
            nx = random.choice(nx_choices)
            d = random.randint(-5, 5)
            e = random.randint(-5, 5)
            M = fmt_linear([(ax, "x"), (my, "y"), (d, "")])
            N = fmt_linear([(nx, "x"), (by, "y"), (e, "")])
            equation = fmt_equation(M, N)
            answer = f"not exact because M_y = {my} and N_x = {nx}"
            steps = [
                step("ODE_SETUP", equation, "test exactness"),
                step("PARTIAL_RESULT", "M_y", my),
                step("PARTIAL_RESULT", "N_x", nx),
                step("CHECK", "M_y != N_x", f"{my} != {nx}",
                     "not exact"),
                step("Z", answer),
            ]
            problem = f"Test whether {equation} is exact."

        return dict(
            problem_id=jid(),
            operation=f"exact_ode_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
