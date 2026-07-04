import random

from base_generator import ProblemGenerator
from helpers import step, jid


def exp_t(rate):
    if rate == 1:
        return "e^t"
    if rate == -1:
        return "e^(-t)"
    return f"e^({rate}t)"


def coeff_exp_t(coeff, rate):
    if coeff == 1:
        return exp_t(rate)
    if coeff == -1:
        return f"-{exp_t(rate)}"
    return f"{coeff}{exp_t(rate)}"


def left_txt(a):
    return "y' + y" if a == 1 else f"y' + {a}y"


def signed_join(terms):
    pieces = []
    for coeff, body in terms:
        if coeff == 0:
            continue
        text = body if abs(coeff) == 1 else f"{abs(coeff)}{body}"
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def solution_txt(C, a, m, c):
    return "y = " + signed_join([(C, exp_t(-a)), (m, exp_t(c))])


def denom_a(a):
    return f"(s + {a})"


def denom_c(c):
    return f"(s - {c})"


def frac_piece(coeff, denom):
    return f"1/{denom}" if abs(coeff) == 1 else f"{abs(coeff)}/{denom}"


def partial_frac_txt(C, a, m, c):
    pieces = []
    for coeff, body in ((C, frac_piece(C, denom_a(a))),
                        (m, frac_piece(m, denom_c(c)))):
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return " ".join(pieces)


def subtract_value_text(left, value):
    return f"{left} - {value}" if value >= 0 else f"{left} + {abs(value)}"


def plus_y_term(coeff):
    return "+ Y" if coeff == 1 else f"+ {coeff}Y"


def signed_number(value):
    return f"+ {value}" if value > 0 else f"- {abs(value)}"


def combined_numerator(y0, c, b):
    factor = f"(s - {c})" if abs(y0) == 1 else f"{abs(y0)}(s - {c})"
    first = factor if y0 > 0 else f"-{factor}"
    return f"{first} {signed_number(b)}"


class LaplaceIVPGenerator(ProblemGenerator):
    """
    Laplace-transform IVPs with the transform table supplied in the problem.

    Variant:
    - first_order_exp: y' + ay = b e^(ct), y(0)=y0

    Op-codes used:
    - ODE_SETUP (established): equation, initial value, method
    - LAPLACE_TABLE: provided transform identities
    - LAPLACE: transform each side
    - SOLVE_Y / REWRITE: isolate Y(s)
    - PARTIAL_FRAC: decompose Y(s)
    - A / M / D (established): cover-up arithmetic
    - INVERSE_LAPLACE: invert each table term
    - Z: explicit solution
    """

    VARIANTS = ["first_order_exp"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        a = random.randint(1, 5)
        c = random.randint(1, 4)
        m = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        C_choices = [v for v in [-4, -3, -2, -1, 1, 2, 3, 4]
                     if v + m != 0]
        C = random.choice(C_choices)
        b = (a + c) * m
        y0 = C + m
        rhs = coeff_exp_t(b, c)
        answer = solution_txt(C, a, m, c)
        den_sum = a + c
        cover_a_num = y0 * (-a - c) + b
        cover_a_den = -a - c
        combined_num = combined_numerator(y0, c, b)
        Y_combined = f"({combined_num})/({denom_a(a)}{denom_c(c)})"
        pf = partial_frac_txt(C, a, m, c)
        table = ("L{y'} = sY - y(0); L{e^(kt)} = 1/(s-k); "
                 "L^-1{1/(s-k)} = e^(kt)")
        steps = [
            step("ODE_SETUP", f"{left_txt(a)} = {rhs}, y(0) = {y0}",
                 "Laplace transform"),
            step("LAPLACE_TABLE", table),
            step("LAPLACE", f"L[{left_txt(a)}]",
                 f"({subtract_value_text('sY', y0)}) {plus_y_term(a)}"),
            step("LAPLACE", f"L[{rhs}]", f"{b}/{denom_c(c)}"),
            step("SOLVE_Y",
                 f"{subtract_value_text(f'(s + {a})Y', y0)} = "
                 f"{b}/{denom_c(c)}",
                 f"Y = {Y_combined}"),
            step("PARTIAL_FRAC", "Y(s)", pf),
            step("A", a, c, den_sum),
            step("M", y0, -den_sum, cover_a_num - b),
            step("A", cover_a_num - b, b, cover_a_num),
            step("D", cover_a_num, cover_a_den, C),
            step("D", b, den_sum, m),
            step("INVERSE_LAPLACE", f"{C}/{denom_a(a)}",
                 coeff_exp_t(C, -a)),
            step("INVERSE_LAPLACE", f"{m}/{denom_c(c)}",
                 coeff_exp_t(m, c)),
            step("Z", answer),
        ]
        problem = (
            f"Use Laplace transforms to solve {left_txt(a)} = {rhs}, "
            f"y(0) = {y0}. Table: {table}."
        )
        return dict(
            problem_id=jid(),
            operation="laplace_ivp_first_order_exp",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
