import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def random_probability():
    while True:
        numerator = random.randint(1, 19)
        denominator = random.randint(2, 20)
        if numerator < denominator and math.gcd(numerator, denominator) == 1:
            return Fraction(numerator, denominator)


class DensityMatrixGenerator(ProblemGenerator):
    """
    Build a diagonal density matrix from a two-state ensemble, then
    compute expectation Tr(rho A) and purity Tr(rho^2).

    Op-codes used:
    - DENSITY_SETUP / DENSITY_MATRIX / TRACE_EXPECT / PURITY
    - S / M / A / E (established/shared): exact arithmetic
    - Z: rho, expectation, and purity
    """

    def generate(self) -> dict:
        p = random_probability()
        q = 1 - p
        a = random.randint(-10, 10)
        b = random.randint(-10, 10)
        left = p * a
        right = q * b
        expectation = left + right
        p_sq = p ** 2
        q_sq = q ** 2
        purity = p_sq + q_sq
        rho = f"[[{fraction_text(p)},0],[0,{fraction_text(q)}]]"
        observable = f"diag({a},{b})"
        steps = [
            step("DENSITY_SETUP", f"p0={fraction_text(p)}",
                 f"p1=1-p0", f"A={observable}"),
            step("S", 1, fraction_text(p), fraction_text(q)),
            step("DENSITY_MATRIX", f"rho={rho}"),
            step("TRACE_EXPECT", "Tr(rho A)=p0*a+p1*b"),
            step("M", fraction_text(p), a, fraction_text(left)),
            step("M", fraction_text(q), b, fraction_text(right)),
            step("A", fraction_text(left), fraction_text(right),
                 fraction_text(expectation)),
            step("E", fraction_text(p), 2, fraction_text(p_sq)),
            step("E", fraction_text(q), 2, fraction_text(q_sq)),
            step("A", fraction_text(p_sq), fraction_text(q_sq),
                 fraction_text(purity)),
            step("PURITY", f"Tr(rho^2)={fraction_text(purity)}"),
        ]
        answer = (
            f"rho = {rho}; expectation = {fraction_text(expectation)}; "
            f"purity = {fraction_text(purity)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"An ensemble has probability {fraction_text(p)} of ket0 and "
            f"the remaining probability of ket1. For observable "
            f"A={observable}, build rho, compute Tr(rho A), and compute "
            f"Tr(rho^2)."
        )
        return dict(
            problem_id=jid(),
            operation="density_matrix_diagonal",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
