import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.pauli_algebra_generator import PauliAlgebraGenerator
from helpers import DELIM


PAULI_RE = re.compile(
    r"For Pauli matrices sigma_x, sigma_y, sigma_z, "
    r"(compute AB|compute the anticommutator \{A,B\}|compute Tr\(AB\)) "
    r"for A=([^ ]+) and B=([^ ]+)\."
)
GELLMANN_RE = re.compile(
    r"For Gell-Mann matrices lambda_1 through lambda_7, compute Tr\(AB\) "
    r"for A=([^ ]+) and B=([^ ]+)\."
)
SCALED_LABEL_RE = re.compile(r"(-?)(?:(\d+))?(sigma_[xyz]|lambda_[1-7]|I)")


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


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


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


def sum_complex(values):
    total = ZERO
    for value in values:
        total = add(total, value)
    return total


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


def parse_scaled_label(text):
    match = SCALED_LABEL_RE.fullmatch(text)
    assert match is not None, text
    sign, coeff, basis = match.groups()
    value = int(coeff) if coeff else 1
    if sign == "-":
        value = -value
    return value, basis


def parse_problem(problem):
    match = PAULI_RE.fullmatch(problem)
    if match:
        action, left_text, right_text = match.groups()
        a, left_basis = parse_scaled_label(left_text)
        b, right_basis = parse_scaled_label(right_text)
        left = left_basis.removeprefix("sigma_")
        right = right_basis.removeprefix("sigma_")
        variant = {
            "compute AB": "product",
            "compute the anticommutator {A,B}": "anticommutator",
            "compute Tr(AB)": "trace",
        }[action]
        return variant, a, left, b, right
    match = GELLMANN_RE.fullmatch(problem)
    assert match is not None, problem
    a, left_basis = parse_scaled_label(match.group(1))
    b, right_basis = parse_scaled_label(match.group(2))
    return "gellmann_trace", a, left_basis.removeprefix("lambda_"), b, (
        right_basis.removeprefix("lambda_")
    )


def pauli_prefix(variant, left, right, a, b, A, B):
    return [
        make_step("PAULI_SETUP", variant,
                  f"A={scaled_label(a, f'sigma_{left}')}",
                  f"B={scaled_label(b, f'sigma_{right}')}"),
        make_step("MATRIX_VALUE", "A", matrix_text(A)),
        make_step("MATRIX_VALUE", "B", matrix_text(B)),
    ]


def expected_product(a, left, b, right):
    A = scale_matrix(PAULI[left], a)
    B = scale_matrix(PAULI[right], b)
    product = matmul(A, B)
    if left == right:
        target_name = real_target_text(a * b, "I")
        target = scale_matrix(identity_matrix(2), a * b)
        identity_text = "delta_ij I"
    else:
        target_label, epsilon = EPSILON[(left, right)]
        target_name = imag_target_text(a * b * epsilon,
                                       f"sigma_{target_label}")
        target = product
        identity_text = "i epsilon_ijk sigma_k"
    steps = pauli_prefix("product", left, right, a, b, A, B)
    steps.extend([
        make_step("MATRIX_PRODUCT", "AB", matrix_text(product)),
        make_step("PAULI_IDENTITY", f"sigma_{left} sigma_{right}",
                  identity_text, target_name),
        make_step("MATRIX_VALUE", target_name, matrix_text(target)),
        make_step("CHECK", "AB", target_name, "verified"),
    ])
    answer = f"AB = {target_name} = {matrix_text(product)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_anticommutator(a, left, b, right):
    A = scale_matrix(PAULI[left], a)
    B = scale_matrix(PAULI[right], b)
    AB = matmul(A, B)
    BA = matmul(B, A)
    anticommutator = mat_add(AB, BA)
    if left == right:
        target_name = real_target_text(2 * a * b, "I")
        target = scale_matrix(identity_matrix(2), 2 * a * b)
    else:
        target_name = "0"
        target = zero_matrix(2)
    steps = pauli_prefix("anticommutator", left, right, a, b, A, B)
    steps.extend([
        make_step("MATRIX_PRODUCT", "AB", matrix_text(AB)),
        make_step("MATRIX_PRODUCT", "BA", matrix_text(BA)),
    ])
    for i in range(2):
        for j in range(2):
            expr = add_expr(complex_text(AB[i][j]), complex_text(BA[i][j]))
            steps.append(make_step("ANTICOMM_ENTRY", f"({i + 1},{j + 1})",
                                   expr, complex_text(anticommutator[i][j])))
    steps.extend([
        make_step("PAULI_IDENTITY", f"{{sigma_{left},sigma_{right}}}",
                  "2 delta_ij I", target_name),
        make_step("MATRIX_VALUE", target_name, matrix_text(target)),
        make_step("CHECK", "{A,B}", target_name, "verified"),
    ])
    answer = f"{{A,B}} = {target_name} = {matrix_text(anticommutator)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_trace(a, left, b, right):
    A = scale_matrix(PAULI[left], a)
    B = scale_matrix(PAULI[right], b)
    product = matmul(A, B)
    trace_value = trace(product)
    target_value = cx(2 * a * b if left == right else 0)
    steps = pauli_prefix("trace", left, right, a, b, A, B)
    steps.append(make_step("MATRIX_PRODUCT", "AB", matrix_text(product)))
    for i in range(2):
        steps.append(make_step("TRACE_ENTRY", f"({i + 1},{i + 1})",
                               complex_text(product[i][i])))
    steps.extend([
        make_step("TRACE_SUM", sum_expr([product[i][i] for i in range(2)]),
                  complex_text(trace_value)),
        make_step("PAULI_IDENTITY", f"Tr(sigma_{left} sigma_{right})",
                  "2 delta_ij", complex_text(target_value)),
        make_step("CHECK", "Tr(AB)", complex_text(target_value), "verified"),
    ])
    answer = f"Tr(AB) = {complex_text(trace_value)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_gellmann_trace(a, left, b, right):
    A = scale_matrix(GELLMANN[left], a)
    B = scale_matrix(GELLMANN[right], b)
    product = matmul(A, B)
    trace_value = trace(product)
    target_value = cx(2 * a * b if left == right else 0)
    steps = [
        make_step("GELLMANN_SETUP", "trace",
                  f"A={scaled_label(a, f'lambda_{left}')}",
                  f"B={scaled_label(b, f'lambda_{right}')}"),
        make_step("MATRIX_VALUE", "A", matrix_text(A)),
        make_step("MATRIX_VALUE", "B", matrix_text(B)),
        make_step("MATRIX_PRODUCT", "AB", matrix_text(product)),
    ]
    for i in range(3):
        steps.append(make_step("TRACE_ENTRY", f"({i + 1},{i + 1})",
                               complex_text(product[i][i])))
    steps.extend([
        make_step("TRACE_SUM", sum_expr([product[i][i] for i in range(3)]),
                  complex_text(trace_value)),
        make_step("GELLMANN_IDENTITY", f"Tr(lambda_{left} lambda_{right})",
                  "2 delta_ab", complex_text(target_value)),
        make_step("CHECK", "Tr(AB)", complex_text(target_value), "verified"),
    ])
    answer = f"Tr(AB) = {complex_text(trace_value)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    variant, a, left, b, right = parse_problem(example["problem"])
    if variant == "product":
        return expected_product(a, left, b, right)
    if variant == "anticommutator":
        return expected_anticommutator(a, left, b, right)
    if variant == "trace":
        return expected_trace(a, left, b, right)
    return expected_gellmann_trace(a, left, b, right)


def parse_complex(text):
    if text == "0":
        return ZERO
    if " + " in text:
        real, imag = text.split(" + ")
        return Fraction(real), parse_complex(imag)[1]
    if " - " in text:
        real, imag = text.split(" - ")
        return Fraction(real), -parse_complex(imag)[1]
    if "i" not in text:
        return Fraction(text), Fraction(0)
    sign = -1 if text.startswith("-") else 1
    body = text.lstrip("-")
    coeff = body.replace("i", "")
    if coeff == "":
        return Fraction(0), Fraction(sign)
    if coeff.startswith("/"):
        return Fraction(0), sign * Fraction(1, int(coeff[1:]))
    if "/" in coeff:
        numerator, denominator = coeff.split("/")
        return Fraction(0), sign * Fraction(int(numerator), int(denominator))
    return Fraction(0), sign * Fraction(int(coeff), 1)


def sum_expression(expr):
    normalized = expr.replace(" - ", " + -")
    total = ZERO
    for term in normalized.split(" + "):
        total = add(total, parse_complex(term))
    return total


class TestPauliAlgebraGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PauliAlgebraGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_entry_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                parts = raw_step.split(DELIM)
                if parts[0] == "ANTICOMM_ENTRY":
                    self.assertEqual(sum_expression(parts[2]),
                                     parse_complex(parts[3]), raw_step)
                elif parts[0] == "TRACE_SUM":
                    self.assertEqual(sum_expression(parts[1]),
                                     parse_complex(parts[2]), raw_step)

    def test_variants_are_available(self):
        for variant in PauliAlgebraGenerator.VARIANTS:
            result = PauliAlgebraGenerator(variant).generate()
            self.assertEqual(result["operation"], f"pauli_algebra_{variant}")
            self.assertEqual(parse_problem(result["problem"])[0], variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PauliAlgebraGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
