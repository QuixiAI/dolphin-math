import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


H_VALUES = sorted({
    Fraction(n, d)
    for n in range(1, 41)
    for d in range(1, 13)
})


def fraction_text(value):
    return str(Fraction(value))


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ", ".join(fraction_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def diag(values):
    return [
        [values[i] if i == j else Fraction(0) for j in range(len(values))]
        for i in range(len(values))
    ]


def mat_add(A, B):
    return [
        [A[i][j] + B[i][j] for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def mat_scale(A, scalar):
    return [[scalar * value for value in row] for row in A]


class CasimirGenerator(ProblemGenerator):
    """
    Verify the spin-1 Casimir using ladder-operator products:
    J^2 = Jz^2 + (J+J- + J-J+)/2 = j(j+1) hbar^2 I.

    Op-codes used:
    - CASIMIR_SETUP / MATRIX_PRODUCT / MATRIX_ADD / MATRIX_SCALE / CHECK
    - E / A / M (established/shared): scalar arithmetic
    - Z: exact Casimir matrix
    """

    def generate(self) -> dict:
        hbar = random.choice(H_VALUES)
        hbar_sq = hbar ** 2
        two_hbar_sq = 2 * hbar_sq
        j_plus_j_minus = diag([2 * hbar_sq, 2 * hbar_sq, 0])
        j_minus_j_plus = diag([0, 2 * hbar_sq, 2 * hbar_sq])
        ladder_sum = mat_add(j_plus_j_minus, j_minus_j_plus)
        ladder_half = mat_scale(ladder_sum, Fraction(1, 2))
        jz_sq = diag([hbar_sq, 0, hbar_sq])
        casimir = mat_add(jz_sq, ladder_half)
        identity_target = diag([two_hbar_sq, two_hbar_sq, two_hbar_sq])

        steps = [
            step("CASIMIR_SETUP", "spin=1", f"hbar={fraction_text(hbar)}",
                 "J^2=Jz^2+(J+J-+J-J+)/2"),
            step("E", fraction_text(hbar), 2, fraction_text(hbar_sq)),
            step("MATRIX_PRODUCT", "Jz^2", matrix_text(jz_sq)),
            step("MATRIX_PRODUCT", "J+J-", matrix_text(j_plus_j_minus)),
            step("MATRIX_PRODUCT", "J-J+", matrix_text(j_minus_j_plus)),
            step("MATRIX_ADD", "J+J- + J-J+", matrix_text(ladder_sum)),
            step("MATRIX_SCALE", "1/2 ladder sum", matrix_text(ladder_half)),
            step("MATRIX_ADD", "Jz^2 + ladder half", matrix_text(casimir)),
            step("A", 1, 1, 2),
            step("M", 2, fraction_text(hbar_sq),
                 fraction_text(two_hbar_sq)),
            step("CHECK", "J^2", f"{fraction_text(two_hbar_sq)}I",
                 "verified"),
        ]
        answer = (
            f"J^2 = {fraction_text(two_hbar_sq)}I = "
            f"{matrix_text(identity_target)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Verify the spin-1 Casimir for hbar={fraction_text(hbar)} "
            "using Jplus=hbar*sqrt2[[0,1,0],[0,0,1],[0,0,0]], "
            "Jminus=hbar*sqrt2[[0,0,0],[1,0,0],[0,1,0]], and "
            "Jz=hbar*[[1,0,0],[0,0,0],[0,0,-1]]."
        )
        return dict(
            problem_id=jid(),
            operation="casimir_spin1",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
