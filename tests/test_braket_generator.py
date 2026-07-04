import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.braket_generator import BraKetGenerator
from helpers import DELIM


INNER_RE = re.compile(
    r"Given phi=\[([^\]]+)\] and psi=\[([^\]]+)\], compute "
    r"inner\(phi,psi\)=conj\(phi\) dot psi\."
)
TIME_RE = re.compile(
    r"A diagonal Hamiltonian gives time-evolution phases \[([^\]]+)\] in "
    r"its eigenbasis\. For ket psi=\[([^\]]+)\], compute U psi\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def cx(real=0, imag=0):
    return Fraction(real), Fraction(imag)


def fraction_text(value):
    return str(Fraction(value))


def imag_unit_text(value):
    value = Fraction(value)
    if value == 1:
        return "i"
    if value == -1:
        return "-i"
    return f"{fraction_text(value)}i"


def imag_abs_text(value):
    value = abs(Fraction(value))
    if value == 1:
        return "i"
    return f"{fraction_text(value)}i"


def complex_text(value):
    real, imag = value
    if real == 0 and imag == 0:
        return "0"
    if imag == 0:
        return fraction_text(real)
    if real == 0:
        return imag_unit_text(imag)
    sign = "+" if imag > 0 else "-"
    return f"{fraction_text(real)}{sign}{imag_abs_text(imag)}"


def vector_text(values):
    return "[" + ",".join(complex_text(value) for value in values) + "]"


def conj(value):
    return value[0], -value[1]


def add(u, v):
    return u[0] + v[0], u[1] + v[1]


def sub(u, v):
    return u[0] - v[0], u[1] - v[1]


def mul(u, v):
    return u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0]


def split_signed_complex(text):
    for idx in range(1, len(text)):
        if text[idx] in "+-":
            return text[:idx], text[idx:]
    return None, text


def parse_imag(text):
    sign = 1
    if text.startswith("+"):
        text = text[1:]
    elif text.startswith("-"):
        sign = -1
        text = text[1:]
    coeff = text[:-1]
    if coeff == "":
        return Fraction(sign)
    return sign * Fraction(coeff)


def parse_complex(text):
    text = text.strip()
    if "i" not in text:
        return cx(Fraction(text))
    real_part, imag_part = split_signed_complex(text)
    if real_part is None:
        return cx(0, parse_imag(imag_part))
    return cx(Fraction(real_part), parse_imag(imag_part))


def parse_vector(text):
    return [parse_complex(part) for part in text.split(",")]


def expected_inner(problem):
    phi_raw, psi_raw = INNER_RE.fullmatch(problem).groups()
    phi = parse_vector(phi_raw)
    psi = parse_vector(psi_raw)
    steps = [
        make_step("BRAKET_SETUP", "inner_product",
                  f"phi={vector_text(phi)}", f"psi={vector_text(psi)}"),
        make_step("BRAKET_FORMULA",
                  "inner(phi,psi)=sum conj(phi_k)*psi_k"),
    ]
    products = []
    for idx, (left, right) in enumerate(zip(phi, psi), start=1):
        left_conj = conj(left)
        product = mul(left_conj, right)
        products.append(product)
        steps.extend([
            make_step("CONJ", f"phi_{idx}={complex_text(left)}",
                      complex_text(left_conj)),
            make_step("CX_M", complex_text(left_conj), complex_text(right),
                      complex_text(product)),
        ])
    running = products[0]
    for product in products[1:]:
        new_running = add(running, product)
        steps.append(make_step("CX_A", complex_text(running),
                               complex_text(product),
                               complex_text(new_running)))
        running = new_running
    result = complex_text(running)
    steps.append(make_step("INNER_PRODUCT", "inner(phi,psi)", result))
    answer = f"inner(phi,psi)={result}"
    return steps, answer


def expected_time(problem):
    phases_raw, psi_raw = TIME_RE.fullmatch(problem).groups()
    phases = parse_vector(phases_raw)
    psi = parse_vector(psi_raw)
    result = [mul(phase, value) for phase, value in zip(phases, psi)]
    steps = [
        make_step("BRAKET_SETUP", "time_evolution",
                  f"psi={vector_text(psi)}", f"phases={vector_text(phases)}"),
        make_step("BRAKET_FORMULA", "U=diag(phases)"),
    ]
    for idx, (phase, value, evolved) in enumerate(
            zip(phases, psi, result), start=1):
        steps.extend([
            make_step("CX_M", complex_text(phase), complex_text(value),
                      complex_text(evolved)),
            make_step("TIME_COMPONENT", f"k={idx}", complex_text(evolved)),
        ])
    result_text = vector_text(result)
    steps.append(make_step("TIME_EVOLVE", "U psi", result_text))
    answer = f"U psi={result_text}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if INNER_RE.fullmatch(problem):
        steps, answer = expected_inner(problem)
    else:
        steps, answer = expected_time(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestBraKetGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = BraKetGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(600):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_complex_arithmetic_steps(self):
        for _ in range(400):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "CX_M":
                    self.assertEqual(mul(parse_complex(fields[1]),
                                         parse_complex(fields[2])),
                                     parse_complex(fields[3]), raw_step)
                elif fields[0] == "CX_A":
                    self.assertEqual(add(parse_complex(fields[1]),
                                         parse_complex(fields[2])),
                                     parse_complex(fields[3]), raw_step)
                elif fields[0] == "CONJ":
                    left = parse_complex(fields[1].split("=", 1)[1])
                    self.assertEqual(conj(left), parse_complex(fields[2]),
                                     raw_step)

    def test_variants_are_available(self):
        for variant in BraKetGenerator.VARIANTS:
            result = BraKetGenerator(variant).generate()
            self.assertEqual(result["operation"], f"braket_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            BraKetGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
