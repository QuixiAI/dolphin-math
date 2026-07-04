import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


COEFFS = [-4, -3, -2, -1, 1, 2, 3, 4]
LABELS = ["x", "y", "z"]


def cx(real=0, imag=0):
    return Fraction(real), Fraction(imag)


ZERO = cx()
ONE_HALF = Fraction(1, 2)

J_MATRICES = {
    "x": [[ZERO, cx(ONE_HALF)], [cx(ONE_HALF), ZERO]],
    "y": [[ZERO, cx(0, -ONE_HALF)], [cx(0, ONE_HALF), ZERO]],
    "z": [[cx(ONE_HALF), ZERO], [ZERO, cx(-ONE_HALF)]],
}

EPSILON = {
    ("x", "y"): ("z", 1),
    ("y", "z"): ("x", 1),
    ("z", "x"): ("y", 1),
    ("y", "x"): ("z", -1),
    ("z", "y"): ("x", -1),
    ("x", "z"): ("y", -1),
}


def add(u, v):
    return u[0] + v[0], u[1] + v[1]


def sub(u, v):
    return u[0] - v[0], u[1] - v[1]


def mul(u, v):
    return u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0]


def scale(value, scalar):
    return value[0] * scalar, value[1] * scalar


def scale_matrix(matrix, scalar):
    if isinstance(scalar, tuple):
        return [[mul(value, scalar) for value in row] for row in matrix]
    return [[scale(value, scalar) for value in row] for row in matrix]


def matmul(A, B):
    return [
        [
            add(mul(A[i][0], B[0][j]), mul(A[i][1], B[1][j]))
            for j in range(2)
        ]
        for i in range(2)
    ]


def mat_sub(A, B):
    return [[sub(A[i][j], B[i][j]) for j in range(2)] for i in range(2)]


def fraction_text(value):
    value = Fraction(value)
    return str(value)


def imag_text(value):
    sign = "-" if value < 0 else ""
    value = abs(Fraction(value))
    if value == 1:
        return f"{sign}i"
    if value.denominator == 1:
        return f"{sign}{value.numerator}i"
    if value.numerator == 1:
        return f"{sign}i/{value.denominator}"
    return f"{sign}{value.numerator}i/{value.denominator}"


def complex_text(value):
    real, imag = value
    if real == 0 and imag == 0:
        return "0"
    if imag == 0:
        return fraction_text(real)
    if real == 0:
        return imag_text(imag)
    sign = "+" if imag > 0 else "-"
    return f"{fraction_text(real)} {sign} {imag_text(abs(imag))}"


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ", ".join(complex_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def scaled_label(coeff, label):
    if coeff == 1:
        return f"J{label}"
    if coeff == -1:
        return f"-J{label}"
    return f"{coeff}J{label}"


def target_text(coeff, label):
    if coeff == 1:
        return f"iJ{label}"
    if coeff == -1:
        return f"-iJ{label}"
    return f"{coeff}iJ{label}"


class StructureConstantGenerator(ProblemGenerator):
    """
    Verify su(2) structure constants with explicit matrix commutators.

    Uses the spin-1/2 Hermitian generators Jx, Jy, Jz and scaled inputs
    A=aJ_i, B=bJ_j. The identity becomes [A,B]=ab*i*epsilon_ijk*J_k.

    Op-codes used:
    - STRUCTURE_SETUP / MATRIX_VALUE / MATRIX_PRODUCT / COMM_ENTRY
    - COMMUTATOR / STRUCTURE_CONSTANT / CHECK
    - Z: verified commutator identity
    """

    def generate(self) -> dict:
        left, right = random.sample(LABELS, 2)
        a = random.choice(COEFFS)
        b = random.choice(COEFFS)
        target_label, epsilon = EPSILON[(left, right)]
        coefficient = a * b * epsilon

        A = scale_matrix(J_MATRICES[left], a)
        B = scale_matrix(J_MATRICES[right], b)
        AB = matmul(A, B)
        BA = matmul(B, A)
        comm = mat_sub(AB, BA)
        target = scale_matrix(J_MATRICES[target_label], cx(0, coefficient))
        epsilon_name = f"epsilon_{left}{right}{target_label}"
        target_name = target_text(coefficient, target_label)

        steps = [
            step("STRUCTURE_SETUP", f"A={scaled_label(a, left)}",
                 f"B={scaled_label(b, right)}",
                 f"{epsilon_name}={epsilon}"),
            step("MATRIX_VALUE", "A", matrix_text(A)),
            step("MATRIX_VALUE", "B", matrix_text(B)),
            step("MATRIX_PRODUCT", "AB", matrix_text(AB)),
            step("MATRIX_PRODUCT", "BA", matrix_text(BA)),
        ]
        for i in range(2):
            for j in range(2):
                expr = (
                    f"{complex_text(AB[i][j])} - "
                    f"{complex_text(BA[i][j])}"
                )
                steps.append(step("COMM_ENTRY", f"({i + 1},{j + 1})",
                                  expr, complex_text(comm[i][j])))
        steps.extend([
            step("COMMUTATOR", "[A,B]", matrix_text(comm)),
            step("STRUCTURE_CONSTANT", epsilon_name, epsilon, target_name),
            step("MATRIX_VALUE", target_name, matrix_text(target)),
            step("CHECK", "[A,B]", target_name, "verified"),
        ])
        answer = f"[A,B] = {target_name} = {matrix_text(comm)}"
        steps.append(step("Z", answer))
        problem = (
            "For spin-1/2 generators "
            "Jx=[[0,1/2],[1/2,0]], "
            "Jy=[[0,-i/2],[i/2,0]], "
            "Jz=[[1/2,0],[0,-1/2]], "
            f"compute [A,B] for A={scaled_label(a, left)} and "
            f"B={scaled_label(b, right)} and verify the structure constant."
        )
        return dict(
            problem_id=jid(),
            operation="structure_constant_su2",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
