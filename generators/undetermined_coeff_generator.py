import random

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_terms(raw_terms):
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        text = body if body and abs(coeff) == 1 else (
            f"{abs(coeff)}{body}" if body else str(abs(coeff))
        )
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def ode_lhs(p, q):
    return fmt_terms([(1, "y''"), (p, "y'"), (q, "y")])


def char_poly(p, q):
    return fmt_terms([(1, "r^2"), (p, "r"), (q, "")])


def exp_txt(rate):
    if rate == 1:
        return "e^x"
    if rate == -1:
        return "e^(-x)"
    return f"e^({rate}x)"


def coeff_exp_txt(coeff, rate):
    if coeff == 1:
        return exp_txt(rate)
    if coeff == -1:
        return f"-{exp_txt(rate)}"
    return f"{coeff}{exp_txt(rate)}"


def factor_txt(root):
    return f"(r - {root})" if root > 0 else f"(r + {abs(root)})"


def signed_join(terms):
    return fmt_terms(terms)


def hom_symbolic(r1, r2):
    return f"C1{exp_txt(r1)} + C2{exp_txt(r2)}"


def solution_txt(c1, r1, c2, r2, particular_terms):
    terms = [(c1, exp_txt(r1)), (c2, exp_txt(r2))] + particular_terms
    return "y = " + signed_join(terms)


def constant_equation_terms(a, b):
    return signed_join([(a, "C1"), (b, "C2")])


def plus_value(value):
    return f"+ {value}" if value > 0 else f"- {abs(value)}"


def derivative_exp_terms(r1, r2):
    return signed_join([
        (r1, f"C1{exp_txt(r1)}"),
        (r2, f"C2{exp_txt(r2)}"),
    ])


class UndeterminedCoeffGenerator(ProblemGenerator):
    """
    Undetermined coefficients for nonhomogeneous constant-coefficient ODEs.

    Variants:
    - constant_forcing:    y_p = A for constant right-hand side
    - exponential_forcing: y_p = A e^(kx) for exponential right-hand side

    Op-codes used:
    - ODE_SETUP (established): equation and initial conditions
    - CHAR_EQ / FACTOR / CHAR_ROOTS: complementary solution
    - HOM_SOL: homogeneous solution
    - UC_GUESS / APPLY_OPERATOR / PARTICULAR: coefficient matching
    - M / A / S / D (established): arithmetic for A, C1, C2
    - SOL_FORM / DERIV_FORM / SOLVE_CONST (established locally)
    - Z: explicit solution
    """

    VARIANTS = ["constant_forcing", "exponential_forcing"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _roots():
        nonzero = [-4, -3, -2, -1, 1, 2, 3, 4]
        return sorted(random.sample(nonzero, 2))

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        nonzero = [-4, -3, -2, -1, 1, 2, 3, 4]
        r1, r2 = self._roots()
        c1 = random.choice(nonzero)
        c2 = random.choice(nonzero)
        p = -(r1 + r2)
        q = r1 * r2
        hom_sum = c1 + c2
        hom_deriv = c1 * r1 + c2 * r2

        base_steps = [
            step("CHAR_EQ", "assume y=e^(rx)", f"{char_poly(p, q)} = 0"),
            step("FACTOR", char_poly(p, q),
                 f"{factor_txt(r1)}{factor_txt(r2)} = 0"),
            step("CHAR_ROOTS", f"r1 = {r1}, r2 = {r2}",
                 "complementary"),
            step("HOM_SOL", "y_h", f"y_h = {hom_symbolic(r1, r2)}"),
        ]

        if variant == "constant_forcing":
            A_part = random.choice(nonzero)
            rhs = q * A_part
            y0 = hom_sum + A_part
            v0 = hom_deriv
            prod = r2 * hom_sum
            num = hom_deriv - prod
            den = r1 - r2
            answer = solution_txt(c1, r1, c2, r2, [(A_part, "")])
            steps = [
                step("ODE_SETUP", f"{ode_lhs(p, q)} = {rhs}",
                     f"y(0) = {y0}, y'(0) = {v0}"),
                *base_steps,
                step("UC_GUESS", "constant forcing", "y_p = A"),
                step("APPLY_OPERATOR", "L[A]", f"{q}A = {rhs}"),
                step("D", rhs, q, A_part),
                step("PARTICULAR", "y_p", A_part),
                step("SOL_FORM",
                     f"y = {hom_symbolic(r1, r2)} "
                     f"{plus_value(A_part)}"),
                step("SUBST", "x=0",
                     f"C1 + C2 {plus_value(A_part)} = {y0}"),
                step("S", y0, A_part, hom_sum),
                step("DERIV_FORM", "y_h'",
                     derivative_exp_terms(r1, r2)),
                step("SUBST", "x=0",
                     f"{constant_equation_terms(r1, r2)} = {hom_deriv}"),
                step("M", r2, hom_sum, prod),
                step("S", hom_deriv, prod, num),
                step("S", r1, r2, den),
                step("D", num, den, c1),
                step("S", hom_sum, c1, c2),
                step("SOLVE_CONST", f"C1 = {c1}", f"C2 = {c2}"),
            ]
            rhs_txt = str(rhs)
        else:
            k_choices = [v for v in nonzero if v not in (r1, r2)]
            k = random.choice(k_choices)
            A_part = random.choice(nonzero)
            k2 = k * k
            pk = p * k
            first_sum = k2 + pk
            denom = first_sum + q
            rhs_coeff = A_part * denom
            y0 = hom_sum + A_part
            particular_deriv = k * A_part
            v0 = hom_deriv + particular_deriv
            adjusted_deriv = v0 - particular_deriv
            prod = r2 * hom_sum
            num = adjusted_deriv - prod
            den = r1 - r2
            rhs_txt = coeff_exp_txt(rhs_coeff, k)
            answer = solution_txt(c1, r1, c2, r2,
                                  [(A_part, exp_txt(k))])
            steps = [
                step("ODE_SETUP", f"{ode_lhs(p, q)} = {rhs_txt}",
                     f"y(0) = {y0}, y'(0) = {v0}"),
                *base_steps,
                step("UC_GUESS", "exponential forcing",
                     f"y_p = A{exp_txt(k)}"),
                step("APPLY_OPERATOR", f"L[A{exp_txt(k)}]",
                     f"A({fmt_terms([(k2, ''), (pk, ''), (q, '')])})"
                     f"{exp_txt(k)}"),
                step("M", k, k, k2),
                step("M", p, k, pk),
                step("A", k2, pk, first_sum),
                step("A", first_sum, q, denom),
                step("D", rhs_coeff, denom, A_part),
                step("PARTICULAR", "y_p", coeff_exp_txt(A_part, k)),
                step("SOL_FORM",
                     "y = " + signed_join([
                         (1, f"C1{exp_txt(r1)}"),
                         (1, f"C2{exp_txt(r2)}"),
                         (A_part, exp_txt(k)),
                     ])),
                step("SUBST", "x=0",
                     f"C1 + C2 {plus_value(A_part)} = {y0}"),
                step("S", y0, A_part, hom_sum),
                step("DERIV_FORM", "y'",
                     signed_join([
                         (r1, f"C1{exp_txt(r1)}"),
                         (r2, f"C2{exp_txt(r2)}"),
                         (k * A_part, exp_txt(k)),
                     ])),
                step("M", k, A_part, particular_deriv),
                step("S", v0, particular_deriv, adjusted_deriv),
                step("SUBST", "x=0",
                     f"{constant_equation_terms(r1, r2)} = "
                     f"{adjusted_deriv}"),
                step("M", r2, hom_sum, prod),
                step("S", adjusted_deriv, prod, num),
                step("S", r1, r2, den),
                step("D", num, den, c1),
                step("S", hom_sum, c1, c2),
                step("SOLVE_CONST", f"C1 = {c1}", f"C2 = {c2}"),
            ]

        steps.append(step("Z", answer))
        problem = (
            f"Solve {ode_lhs(p, q)} = {rhs_txt} with y(0) = {y0} and "
            f"y'(0) = {v0} by undetermined coefficients."
        )
        return dict(
            problem_id=jid(),
            operation=f"undetermined_coeff_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
