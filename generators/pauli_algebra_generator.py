import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


COEFFS = [-4, -3, -2, -1, 1, 2, 3, 4]
PAULI_LABELS = ["x", "y", "z"]
GELLMANN_LABELS = ["1", "2", "3", "4", "5", "6", "7"]


def cx(real=0, imag=0):
    return Fraction(real), Fraction(imag)


ZERO = cx()
ONE = cx(1)
NEG_ONE = cx(-1)
I = cx(0, 1)
NEG_I = cx(0, -1)

PAULI = {
    "x": [[ZERO, ONE], [ONE, ZERO]],
    "y": [[ZERO, NEG_I], [I, ZERO]],
    "z": [[ONE, ZERO], [ZERO, NEG_ONE]],
}

GELLMANN = {
    "1": [[ZERO, ONE, ZERO], [ONE, ZERO, ZERO], [ZERO, ZERO, ZERO]],
    "2": [[ZERO, NEG_I, ZERO], [I, ZERO, ZERO], [ZERO, ZERO, ZERO]],
    "3": [[ONE, ZERO, ZERO], [ZERO, NEG_ONE, ZERO], [ZERO, ZERO, ZERO]],
    "4": [[ZERO, ZERO, ONE], [ZERO, ZERO, ZERO], [ONE, ZERO, ZERO]],
    "5": [[ZERO, ZERO, NEG_I], [ZERO, ZERO, ZERO], [I, ZERO, ZERO]],
    "6": [[ZERO, ZERO, ZERO], [ZERO, ZERO, ONE], [ZERO, ONE, ZERO]],
    "7": [[ZERO, ZERO, ZERO], [ZERO, ZERO, NEG_I], [ZERO, I, ZERO]],
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
    return [[scale(value, scalar) for value in row] for row in matrix]


def matmul(A, B):
    return [
        [
            sum_complex(mul(A[i][k], B[k][j]) for k in range(len(B)))
            for j in range(len(B[0]))
        ]
        for i in range(len(A))
    ]


def mat_add(A, B):
    return [
        [add(A[i][j], B[i][j]) for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def sum_complex(values):
    total = ZERO
    for value in values:
        total = add(total, value)
    return total


def trace(matrix):
    return sum_complex(matrix[i][i] for i in range(len(matrix)))


def fraction_text(value):
    return str(Fraction(value))


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


def add_expr(left, right):
    if right.startswith("-"):
        return f"{left} - {right[1:]}"
    return f"{left} + {right}"


def sum_expr(values):
    texts = [complex_text(value) for value in values]
    expression = texts[0]
    for text in texts[1:]:
        expression = add_expr(expression, text)
    return expression


def scaled_label(coeff, basis):
    if coeff == 1:
        return basis
    if coeff == -1:
        return f"-{basis}"
    return f"{coeff}{basis}"


def real_target_text(coeff, basis):
    if coeff == 0:
        return "0"
    return scaled_label(coeff, basis)


def imag_target_text(coeff, basis):
    if coeff == 1:
        return f"i{basis}"
    if coeff == -1:
        return f"-i{basis}"
    return f"{coeff}i{basis}"


def identity_matrix(size):
    return [[cx(1 if i == j else 0) for j in range(size)] for i in range(size)]


def zero_matrix(size):
    return [[ZERO for _ in range(size)] for _ in range(size)]


class PauliAlgebraGenerator(ProblemGenerator):
    """
    Pauli products, anticommutators, traces, and Gell-Mann trace identities.

    Variants:
    - product: sigma_i sigma_j = delta_ij I + i epsilon_ijk sigma_k.
    - anticommutator: {sigma_i, sigma_j} = 2 delta_ij I.
    - trace: Tr(sigma_i sigma_j) = 2 delta_ij.
    - gellmann_trace: Tr(lambda_a lambda_b) = 2 delta_ab.

    Op-codes used:
    - PAULI_SETUP / GELLMANN_SETUP / MATRIX_VALUE / MATRIX_PRODUCT
    - ANTICOMM_ENTRY / TRACE_ENTRY / TRACE_SUM / PAULI_IDENTITY
    - GELLMANN_IDENTITY / CHECK
    - Z: exact identity result
    """

    VARIANTS = ["product", "anticommutator", "trace", "gellmann_trace"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "product":
            problem, steps, answer = self._generate_product()
        elif variant == "anticommutator":
            problem, steps, answer = self._generate_anticommutator()
        elif variant == "trace":
            problem, steps, answer = self._generate_trace()
        else:
            problem, steps, answer = self._generate_gellmann_trace()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"pauli_algebra_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _scaled_pauli_pair(self):
        left = random.choice(PAULI_LABELS)
        right = random.choice(PAULI_LABELS)
        a = random.choice(COEFFS)
        b = random.choice(COEFFS)
        A = scale_matrix(PAULI[left], a)
        B = scale_matrix(PAULI[right], b)
        return left, right, a, b, A, B

    def _generate_product(self):
        left, right, a, b, A, B = self._scaled_pauli_pair()
        product = matmul(A, B)
        if left == right:
            target_name = real_target_text(a * b, "I")
            identity = scale_matrix(identity_matrix(2), a * b)
            identity_text = "delta_ij I"
        else:
            target_label, epsilon = EPSILON[(left, right)]
            target_name = imag_target_text(a * b * epsilon,
                                           f"sigma_{target_label}")
            identity = product
            identity_text = "i epsilon_ijk sigma_k"
        steps = self._pauli_prefix("product", left, right, a, b, A, B)
        steps.extend([
            step("MATRIX_PRODUCT", "AB", matrix_text(product)),
            step("PAULI_IDENTITY", f"sigma_{left} sigma_{right}",
                 identity_text, target_name),
            step("MATRIX_VALUE", target_name, matrix_text(identity)),
            step("CHECK", "AB", target_name, "verified"),
        ])
        answer = f"AB = {target_name} = {matrix_text(product)}"
        problem = self._pauli_problem("compute AB", a, left, b, right)
        return problem, steps, answer

    def _generate_anticommutator(self):
        left, right, a, b, A, B = self._scaled_pauli_pair()
        AB = matmul(A, B)
        BA = matmul(B, A)
        anticommutator = mat_add(AB, BA)
        if left == right:
            target_name = real_target_text(2 * a * b, "I")
            target = scale_matrix(identity_matrix(2), 2 * a * b)
        else:
            target_name = "0"
            target = zero_matrix(2)
        steps = self._pauli_prefix("anticommutator", left, right, a, b, A, B)
        steps.extend([
            step("MATRIX_PRODUCT", "AB", matrix_text(AB)),
            step("MATRIX_PRODUCT", "BA", matrix_text(BA)),
        ])
        for i in range(2):
            for j in range(2):
                expr = (
                    add_expr(complex_text(AB[i][j]),
                             complex_text(BA[i][j]))
                )
                steps.append(step("ANTICOMM_ENTRY", f"({i + 1},{j + 1})",
                                  expr, complex_text(anticommutator[i][j])))
        steps.extend([
            step("PAULI_IDENTITY", f"{{sigma_{left},sigma_{right}}}",
                 "2 delta_ij I", target_name),
            step("MATRIX_VALUE", target_name, matrix_text(target)),
            step("CHECK", "{A,B}", target_name, "verified"),
        ])
        answer = f"{{A,B}} = {target_name} = {matrix_text(anticommutator)}"
        problem = self._pauli_problem("compute the anticommutator {A,B}",
                                      a, left, b, right)
        return problem, steps, answer

    def _generate_trace(self):
        left, right, a, b, A, B = self._scaled_pauli_pair()
        product = matmul(A, B)
        trace_value = trace(product)
        target_value = cx(2 * a * b if left == right else 0)
        steps = self._pauli_prefix("trace", left, right, a, b, A, B)
        steps.append(step("MATRIX_PRODUCT", "AB", matrix_text(product)))
        for i in range(2):
            steps.append(step("TRACE_ENTRY", f"({i + 1},{i + 1})",
                              complex_text(product[i][i])))
        steps.extend([
            step("TRACE_SUM", sum_expr([product[i][i] for i in range(2)]),
                 complex_text(trace_value)),
            step("PAULI_IDENTITY", f"Tr(sigma_{left} sigma_{right})",
                 "2 delta_ij", complex_text(target_value)),
            step("CHECK", "Tr(AB)", complex_text(target_value), "verified"),
        ])
        answer = f"Tr(AB) = {complex_text(trace_value)}"
        problem = self._pauli_problem("compute Tr(AB)", a, left, b, right)
        return problem, steps, answer

    def _generate_gellmann_trace(self):
        left = random.choice(GELLMANN_LABELS)
        right = random.choice(GELLMANN_LABELS)
        a = random.choice(COEFFS)
        b = random.choice(COEFFS)
        A = scale_matrix(GELLMANN[left], a)
        B = scale_matrix(GELLMANN[right], b)
        product = matmul(A, B)
        trace_value = trace(product)
        target_value = cx(2 * a * b if left == right else 0)
        steps = [
            step("GELLMANN_SETUP", "trace",
                 f"A={scaled_label(a, f'lambda_{left}')}",
                 f"B={scaled_label(b, f'lambda_{right}')}"),
            step("MATRIX_VALUE", "A", matrix_text(A)),
            step("MATRIX_VALUE", "B", matrix_text(B)),
            step("MATRIX_PRODUCT", "AB", matrix_text(product)),
        ]
        for i in range(3):
            steps.append(step("TRACE_ENTRY", f"({i + 1},{i + 1})",
                              complex_text(product[i][i])))
        steps.extend([
            step("TRACE_SUM", sum_expr([product[i][i] for i in range(3)]),
                 complex_text(trace_value)),
            step("GELLMANN_IDENTITY", f"Tr(lambda_{left} lambda_{right})",
                 "2 delta_ab", complex_text(target_value)),
            step("CHECK", "Tr(AB)", complex_text(target_value), "verified"),
        ])
        answer = f"Tr(AB) = {complex_text(trace_value)}"
        problem = (
            "For Gell-Mann matrices lambda_1 through lambda_7, "
            f"compute Tr(AB) for A={scaled_label(a, f'lambda_{left}')} "
            f"and B={scaled_label(b, f'lambda_{right}')}."
        )
        return problem, steps, answer

    def _pauli_prefix(self, variant, left, right, a, b, A, B):
        return [
            step("PAULI_SETUP", variant,
                 f"A={scaled_label(a, f'sigma_{left}')}",
                 f"B={scaled_label(b, f'sigma_{right}')}"),
            step("MATRIX_VALUE", "A", matrix_text(A)),
            step("MATRIX_VALUE", "B", matrix_text(B)),
        ]

    def _pauli_problem(self, action, a, left, b, right):
        return (
            "For Pauli matrices sigma_x, sigma_y, sigma_z, "
            f"{action} for A={scaled_label(a, f'sigma_{left}')} "
            f"and B={scaled_label(b, f'sigma_{right}')}."
        )
