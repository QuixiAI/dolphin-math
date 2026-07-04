import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


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

PYTHAGOREAN_STATES = [
    (3, 4, 5),
    (5, 12, 13),
    (8, 15, 17),
    (7, 24, 25),
    (20, 21, 29),
    (12, 35, 37),
    (9, 40, 41),
    (28, 45, 53),
    (11, 60, 61),
    (33, 56, 65),
    (16, 63, 65),
    (48, 55, 73),
]

EIGEN_CASES = [
    dict(axis="z", state="ket0", eigen=1,
         actions=[("sigma_z ket0", "ket0")], rewrites=[]),
    dict(axis="z", state="ket1", eigen=-1,
         actions=[("sigma_z ket1", "-ket1")], rewrites=[]),
    dict(axis="x", state="(ket0 + ket1)/sqrt(2)", eigen=1,
         actions=[("sigma_x ket0", "ket1"),
                  ("sigma_x ket1", "ket0")],
         rewrites=["sigma_x psi=(ket1 + ket0)/sqrt(2)",
                   "sigma_x psi=(ket0 + ket1)/sqrt(2)"]),
    dict(axis="x", state="(ket0 - ket1)/sqrt(2)", eigen=-1,
         actions=[("sigma_x ket0", "ket1"),
                  ("sigma_x -ket1", "-ket0")],
         rewrites=["sigma_x psi=(ket1 - ket0)/sqrt(2)",
                   "sigma_x psi=-(ket0 - ket1)/sqrt(2)"]),
    dict(axis="y", state="(ket0 + i ket1)/sqrt(2)", eigen=1,
         actions=[("sigma_y ket0", "i ket1"),
                  ("sigma_y i ket1", "ket0")],
         rewrites=["sigma_y psi=(i ket1 + ket0)/sqrt(2)",
                   "sigma_y psi=(ket0 + i ket1)/sqrt(2)"]),
    dict(axis="y", state="(ket0 - i ket1)/sqrt(2)", eigen=-1,
         actions=[("sigma_y ket0", "i ket1"),
                  ("sigma_y -i ket1", "-ket0")],
         rewrites=["sigma_y psi=(i ket1 - ket0)/sqrt(2)",
                   "sigma_y psi=-(ket0 - i ket1)/sqrt(2)"]),
]


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


def mul(u, v):
    return u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0]


def eigen_text(value):
    return "1" if value == 1 else "-1"


def random_real_state():
    a, b, denom = random.choice(PYTHAGOREAN_STATES)
    if random.choice([False, True]):
        a, b = b, a
    a *= random.choice([-1, 1])
    b *= random.choice([-1, 1])
    return [cx(Fraction(a, denom)), cx(Fraction(b, denom))]


class SpinHalfGenerator(ProblemGenerator):
    """
    Spin-1/2 calculations with Pauli matrices and exact probabilities.

    Variants:
    - apply_pauli: multiply sigma_x, sigma_y, or sigma_z by a normalized spinor.
    - eigenvalue: verify a Pauli eigenstate and read the eigenvalue.
    - measurement_probability: compute z- or x-axis measurement probabilities.

    Op-codes used:
    - SPIN_SETUP / PAULI_MATRIX / MEASURE_BASIS / APPLY_PAULI
    - CX_M / CX_A: exact complex multiplication and addition
    - PROBABILITY / NORM_CHECK / EIGEN_CHECK
    - A / S / D / E (established/shared): exact probability arithmetic
    - Z: transformed spinor, eigenvalue, or measurement probabilities
    """

    VARIANTS = ["apply_pauli", "eigenvalue", "measurement_probability"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "apply_pauli":
            problem, steps, answer = self._generate_apply_pauli()
        elif variant == "eigenvalue":
            problem, steps, answer = self._generate_eigenvalue()
        else:
            problem, steps, answer = self._generate_measurement()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"spin_half_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_apply_pauli(self):
        axis = random.choice(["x", "y", "z"])
        psi = random_real_state()
        matrix = PAULI[axis]
        result = []
        steps = [
            step("SPIN_SETUP", "apply_pauli", f"operator=sigma_{axis}",
                 f"psi={vector_text(psi)}"),
            step("PAULI_MATRIX", f"sigma_{axis}", PAULI_MATRIX_TEXT[axis]),
        ]
        for row_idx, row in enumerate(matrix, start=1):
            terms = []
            for col_idx, entry in enumerate(row):
                product = mul(entry, psi[col_idx])
                terms.append(product)
                steps.append(step("CX_M", complex_text(entry),
                                  complex_text(psi[col_idx]),
                                  complex_text(product)))
            row_value = add(terms[0], terms[1])
            result.append(row_value)
            steps.append(step("CX_A", complex_text(terms[0]),
                              complex_text(terms[1]),
                              complex_text(row_value)))
            steps.append(step("SPIN_COMPONENT", f"row={row_idx}",
                              complex_text(row_value)))
        result_text = vector_text(result)
        steps.append(step("APPLY_PAULI", f"sigma_{axis} psi", result_text))
        answer = f"sigma_{axis} psi={result_text}"
        problem = (
            f"For spin state psi={vector_text(psi)} in the z basis, apply "
            f"sigma_{axis}."
        )
        return problem, steps, answer

    def _generate_eigenvalue(self):
        case = random.choice(EIGEN_CASES)
        axis = case["axis"]
        lam = eigen_text(case["eigen"])
        steps = [
            step("SPIN_SETUP", "eigenvalue", f"operator=sigma_{axis}",
                 f"psi={case['state']}"),
            step("PAULI_MATRIX", f"sigma_{axis}", PAULI_MATRIX_TEXT[axis]),
        ]
        for source, target in case["actions"]:
            steps.append(step("APPLY_PAULI", source, target))
        for rewrite in case["rewrites"]:
            steps.append(step("REWRITE", rewrite))
        steps.append(step("EIGEN_CHECK", f"sigma_{axis} psi",
                          f"{lam}*psi", f"lambda={lam}"))
        answer = f"sigma_{axis} psi={lam}*psi; lambda={lam}"
        problem = (
            f"Show that psi={case['state']} is an eigenstate of sigma_{axis} "
            "and find the eigenvalue."
        )
        return problem, steps, answer

    def _generate_measurement(self):
        axis = random.choice(["x", "z"])
        psi = random_real_state()
        a = psi[0][0]
        b = psi[1][0]
        steps = [
            step("SPIN_SETUP", "measurement_probability", f"axis={axis}",
                 f"psi={vector_text(psi)}"),
        ]
        if axis == "z":
            p_plus = a ** 2
            p_minus = b ** 2
            steps.extend([
                step("MEASURE_BASIS", "z", "ket+z=ket0", "ket-z=ket1"),
                step("E", fraction_text(a), 2, fraction_text(p_plus)),
                step("PROBABILITY", "P(+z)", fraction_text(p_plus)),
                step("E", fraction_text(b), 2, fraction_text(p_minus)),
                step("PROBABILITY", "P(-z)", fraction_text(p_minus)),
            ])
        else:
            plus_sum = a + b
            minus_diff = a - b
            plus_sq = plus_sum ** 2
            minus_sq = minus_diff ** 2
            p_plus = Fraction(plus_sq, 2)
            p_minus = Fraction(minus_sq, 2)
            steps.extend([
                step("MEASURE_BASIS", "x",
                     "ket+x=(ket0+ket1)/sqrt(2)",
                     "ket-x=(ket0-ket1)/sqrt(2)"),
                step("A", fraction_text(a), fraction_text(b),
                     fraction_text(plus_sum)),
                step("E", fraction_text(plus_sum), 2,
                     fraction_text(plus_sq)),
                step("D", fraction_text(plus_sq), 2, fraction_text(p_plus)),
                step("PROBABILITY", "P(+x)", fraction_text(p_plus)),
                step("S", fraction_text(a), fraction_text(b),
                     fraction_text(minus_diff)),
                step("E", fraction_text(minus_diff), 2,
                     fraction_text(minus_sq)),
                step("D", fraction_text(minus_sq), 2,
                     fraction_text(p_minus)),
                step("PROBABILITY", "P(-x)", fraction_text(p_minus)),
            ])
        total = p_plus + p_minus
        steps.extend([
            step("A", fraction_text(p_plus), fraction_text(p_minus),
                 fraction_text(total)),
            step("NORM_CHECK", f"P(+{axis})+P(-{axis})",
                 fraction_text(total)),
        ])
        answer = (
            f"P(+{axis})={fraction_text(p_plus)}; "
            f"P(-{axis})={fraction_text(p_minus)}"
        )
        problem = (
            f"For normalized spin state psi={vector_text(psi)} in the z "
            f"basis, measure spin along {axis}. Find P(+{axis}) and "
            f"P(-{axis})."
        )
        return problem, steps, answer
