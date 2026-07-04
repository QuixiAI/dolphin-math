import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.structure_constant_generator import StructureConstantGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For spin-1/2 generators .* compute \[A,B\] for A=([^ ]+) "
    r"and B=([^ ]+) and verify the structure constant\."
)
SCALED_LABEL_RE = re.compile(r"(-?)(?:(\d+))?J([xyz])")


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


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return (*parse_scaled_label(match.group(1)),
            *parse_scaled_label(match.group(2)))


def parse_scaled_label(text):
    match = SCALED_LABEL_RE.fullmatch(text)
    assert match is not None, text
    sign, coeff, label = match.groups()
    value = int(coeff) if coeff else 1
    if sign == "-":
        value = -value
    return value, label


def expected_flow(example):
    a, left, b, right = parse_problem(example["problem"])
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
        make_step("STRUCTURE_SETUP", f"A={scaled_label(a, left)}",
                  f"B={scaled_label(b, right)}",
                  f"{epsilon_name}={epsilon}"),
        make_step("MATRIX_VALUE", "A", matrix_text(A)),
        make_step("MATRIX_VALUE", "B", matrix_text(B)),
        make_step("MATRIX_PRODUCT", "AB", matrix_text(AB)),
        make_step("MATRIX_PRODUCT", "BA", matrix_text(BA)),
    ]
    for i in range(2):
        for j in range(2):
            expr = (
                f"{complex_text(AB[i][j])} - "
                f"{complex_text(BA[i][j])}"
            )
            steps.append(make_step("COMM_ENTRY", f"({i + 1},{j + 1})",
                                   expr, complex_text(comm[i][j])))
    steps.extend([
        make_step("COMMUTATOR", "[A,B]", matrix_text(comm)),
        make_step("STRUCTURE_CONSTANT", epsilon_name, epsilon, target_name),
        make_step("MATRIX_VALUE", target_name, matrix_text(target)),
        make_step("CHECK", "[A,B]", target_name, "verified"),
    ])
    answer = f"[A,B] = {target_name} = {matrix_text(comm)}"
    steps.append(make_step("Z", answer))
    return steps, answer


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


class TestStructureConstantGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = StructureConstantGenerator()

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

    def test_commutator_entry_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                parts = raw_step.split(DELIM)
                if parts[0] != "COMM_ENTRY":
                    continue
                left, right = parts[2].split(" - ")
                self.assertEqual(sub(parse_complex(left),
                                     parse_complex(right)),
                                 parse_complex(parts[3]), raw_step)

    def test_ordered_pairs_are_reachable(self):
        random.seed(7)
        seen = set()
        gen = StructureConstantGenerator()
        for _ in range(500):
            _, left, _, right = parse_problem(gen.generate()["problem"])
            seen.add((left, right))
        self.assertEqual(seen, set(EPSILON))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
