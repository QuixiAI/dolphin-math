import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.spin_half_generator import SpinHalfGenerator
from helpers import DELIM


APPLY_RE = re.compile(
    r"For spin state psi=\[([^,\]]+),([^,\]]+)\] in the z basis, "
    r"apply sigma_([xyz])\."
)
MEASURE_RE = re.compile(
    r"For normalized spin state psi=\[([^,\]]+),([^,\]]+)\] in the z "
    r"basis, measure spin along ([xz])\. Find P\(\+\3\) and P\(-\3\)\."
)
EIGEN_RE = re.compile(
    r"Show that psi=(.+) is an eigenstate of sigma_([xyz]) and find the "
    r"eigenvalue\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


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

PAULI_MATRIX_TEXT = {
    "x": "[[0,1],[1,0]]",
    "y": "[[0,-i],[i,0]]",
    "z": "[[1,0],[0,-1]]",
}

EIGEN_CASES = {
    ("z", "ket0"): dict(eigen=1,
                         actions=[("sigma_z ket0", "ket0")],
                         rewrites=[]),
    ("z", "ket1"): dict(eigen=-1,
                         actions=[("sigma_z ket1", "-ket1")],
                         rewrites=[]),
    ("x", "(ket0 + ket1)/sqrt(2)"): dict(
        eigen=1,
        actions=[("sigma_x ket0", "ket1"),
                 ("sigma_x ket1", "ket0")],
        rewrites=["sigma_x psi=(ket1 + ket0)/sqrt(2)",
                  "sigma_x psi=(ket0 + ket1)/sqrt(2)"],
    ),
    ("x", "(ket0 - ket1)/sqrt(2)"): dict(
        eigen=-1,
        actions=[("sigma_x ket0", "ket1"),
                 ("sigma_x -ket1", "-ket0")],
        rewrites=["sigma_x psi=(ket1 - ket0)/sqrt(2)",
                  "sigma_x psi=-(ket0 - ket1)/sqrt(2)"],
    ),
    ("y", "(ket0 + i ket1)/sqrt(2)"): dict(
        eigen=1,
        actions=[("sigma_y ket0", "i ket1"),
                 ("sigma_y i ket1", "ket0")],
        rewrites=["sigma_y psi=(i ket1 + ket0)/sqrt(2)",
                  "sigma_y psi=(ket0 + i ket1)/sqrt(2)"],
    ),
    ("y", "(ket0 - i ket1)/sqrt(2)"): dict(
        eigen=-1,
        actions=[("sigma_y ket0", "i ket1"),
                 ("sigma_y -i ket1", "-ket0")],
        rewrites=["sigma_y psi=(i ket1 - ket0)/sqrt(2)",
                  "sigma_y psi=-(ket0 - i ket1)/sqrt(2)"],
    ),
}


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


def vector_text(vector):
    return "[" + ",".join(complex_text(value) for value in vector) + "]"


def add(u, v):
    return u[0] + v[0], u[1] + v[1]


def sub(u, v):
    return u[0] - v[0], u[1] - v[1]


def mul(u, v):
    return u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0]


def parse_imag_coeff(text):
    if text in ("i", "+i"):
        return Fraction(1)
    if text == "-i":
        return Fraction(-1)
    if "i/" in text:
        coeff, denominator = text.split("i/")
        if coeff in ("", "+"):
            numerator = 1
        elif coeff == "-":
            numerator = -1
        else:
            numerator = int(coeff)
        return Fraction(numerator, int(denominator))
    coeff = text.removesuffix("i")
    if coeff in ("", "+"):
        return Fraction(1)
    if coeff == "-":
        return Fraction(-1)
    return Fraction(coeff)


def parse_complex(text):
    text = text.strip()
    if " + " in text:
        left, right = text.split(" + ", 1)
        return add(parse_complex(left), parse_complex(right))
    if " - " in text:
        left, right = text.split(" - ", 1)
        return sub(parse_complex(left), parse_complex(right))
    if "i" in text:
        return cx(0, parse_imag_coeff(text))
    return cx(Fraction(text))


def eigen_text(value):
    return "1" if value == 1 else "-1"


def expected_apply(problem):
    a_raw, b_raw, axis = APPLY_RE.fullmatch(problem).groups()
    psi = [cx(Fraction(a_raw)), cx(Fraction(b_raw))]
    steps = [
        make_step("SPIN_SETUP", "apply_pauli", f"operator=sigma_{axis}",
                  f"psi={vector_text(psi)}"),
        make_step("PAULI_MATRIX", f"sigma_{axis}", PAULI_MATRIX_TEXT[axis]),
    ]
    result = []
    for row_idx, row in enumerate(PAULI[axis], start=1):
        terms = []
        for col_idx, entry in enumerate(row):
            product = mul(entry, psi[col_idx])
            terms.append(product)
            steps.append(make_step("CX_M", complex_text(entry),
                                   complex_text(psi[col_idx]),
                                   complex_text(product)))
        row_value = add(terms[0], terms[1])
        result.append(row_value)
        steps.append(make_step("CX_A", complex_text(terms[0]),
                               complex_text(terms[1]),
                               complex_text(row_value)))
        steps.append(make_step("SPIN_COMPONENT", f"row={row_idx}",
                               complex_text(row_value)))
    result_text = vector_text(result)
    steps.append(make_step("APPLY_PAULI", f"sigma_{axis} psi", result_text))
    answer = f"sigma_{axis} psi={result_text}"
    return steps, answer


def expected_measurement(problem):
    a_raw, b_raw, axis = MEASURE_RE.fullmatch(problem).groups()
    a = Fraction(a_raw)
    b = Fraction(b_raw)
    psi = [cx(a), cx(b)]
    steps = [
        make_step("SPIN_SETUP", "measurement_probability", f"axis={axis}",
                  f"psi={vector_text(psi)}"),
    ]
    if axis == "z":
        p_plus = a ** 2
        p_minus = b ** 2
        steps.extend([
            make_step("MEASURE_BASIS", "z", "ket+z=ket0", "ket-z=ket1"),
            make_step("E", fraction_text(a), 2, fraction_text(p_plus)),
            make_step("PROBABILITY", "P(+z)", fraction_text(p_plus)),
            make_step("E", fraction_text(b), 2, fraction_text(p_minus)),
            make_step("PROBABILITY", "P(-z)", fraction_text(p_minus)),
        ])
    else:
        plus_sum = a + b
        minus_diff = a - b
        plus_sq = plus_sum ** 2
        minus_sq = minus_diff ** 2
        p_plus = Fraction(plus_sq, 2)
        p_minus = Fraction(minus_sq, 2)
        steps.extend([
            make_step("MEASURE_BASIS", "x",
                      "ket+x=(ket0+ket1)/sqrt(2)",
                      "ket-x=(ket0-ket1)/sqrt(2)"),
            make_step("A", fraction_text(a), fraction_text(b),
                      fraction_text(plus_sum)),
            make_step("E", fraction_text(plus_sum), 2,
                      fraction_text(plus_sq)),
            make_step("D", fraction_text(plus_sq), 2,
                      fraction_text(p_plus)),
            make_step("PROBABILITY", "P(+x)", fraction_text(p_plus)),
            make_step("S", fraction_text(a), fraction_text(b),
                      fraction_text(minus_diff)),
            make_step("E", fraction_text(minus_diff), 2,
                      fraction_text(minus_sq)),
            make_step("D", fraction_text(minus_sq), 2,
                      fraction_text(p_minus)),
            make_step("PROBABILITY", "P(-x)", fraction_text(p_minus)),
        ])
    total = p_plus + p_minus
    steps.extend([
        make_step("A", fraction_text(p_plus), fraction_text(p_minus),
                  fraction_text(total)),
        make_step("NORM_CHECK", f"P(+{axis})+P(-{axis})",
                  fraction_text(total)),
    ])
    answer = f"P(+{axis})={fraction_text(p_plus)}; P(-{axis})={fraction_text(p_minus)}"
    return steps, answer


def expected_eigenvalue(problem):
    state, axis = EIGEN_RE.fullmatch(problem).groups()
    case = EIGEN_CASES[(axis, state)]
    lam = eigen_text(case["eigen"])
    steps = [
        make_step("SPIN_SETUP", "eigenvalue", f"operator=sigma_{axis}",
                  f"psi={state}"),
        make_step("PAULI_MATRIX", f"sigma_{axis}", PAULI_MATRIX_TEXT[axis]),
    ]
    for source, target in case["actions"]:
        steps.append(make_step("APPLY_PAULI", source, target))
    for rewrite in case["rewrites"]:
        steps.append(make_step("REWRITE", rewrite))
    steps.append(make_step("EIGEN_CHECK", f"sigma_{axis} psi",
                           f"{lam}*psi", f"lambda={lam}"))
    answer = f"sigma_{axis} psi={lam}*psi; lambda={lam}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if APPLY_RE.fullmatch(problem):
        steps, answer = expected_apply(problem)
    elif MEASURE_RE.fullmatch(problem):
        steps, answer = expected_measurement(problem)
    else:
        steps, answer = expected_eigenvalue(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestSpinHalfGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SpinHalfGenerator()

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

    def test_arithmetic_steps(self):
        for _ in range(400):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "CX_M":
                    self.assertEqual(mul(parse_complex(fields[1]),
                                         parse_complex(fields[2])),
                                     parse_complex(fields[3]), raw_step)
                elif fields[0] == "CX_A":
                    self.assertEqual(add(parse_complex(fields[1]),
                                         parse_complex(fields[2])),
                                     parse_complex(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in SpinHalfGenerator.VARIANTS:
            result = SpinHalfGenerator(variant).generate()
            self.assertEqual(result["operation"], f"spin_half_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SpinHalfGenerator("bogus")

    def test_measurement_probabilities_sum_to_one(self):
        gen = SpinHalfGenerator("measurement_probability")
        for _ in range(300):
            result = gen.generate()
            parts = dict(
                item.split("=") for item in result["final_answer"].split("; ")
            )
            self.assertEqual(sum(Fraction(value) for value in parts.values()),
                             Fraction(1), result["problem"])

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
