import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def cx(real=0, imag=0):
    return Fraction(real), Fraction(imag)


COMPONENTS = [
    cx(0),
    cx(1),
    cx(-1),
    cx(2),
    cx(-2),
    cx(0, 1),
    cx(0, -1),
    cx(1, 1),
    cx(1, -1),
    cx(-1, 1),
    cx(-1, -1),
    cx(2, 1),
    cx(2, -1),
]

PHASES = [cx(1), cx(-1), cx(0, 1), cx(0, -1)]


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


def mul(u, v):
    return u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0]


def random_vector(dim):
    while True:
        values = [random.choice(COMPONENTS) for _ in range(dim)]
        if any(value != cx(0) for value in values):
            return values


class BraKetGenerator(ProblemGenerator):
    """
    Finite-dimensional bra-ket arithmetic with exact complex components.

    Variants:
    - inner_product: compute inner(phi,psi)=conj(phi) dot psi.
    - time_evolution: apply supplied diagonal time-evolution phases to a ket.

    Op-codes used:
    - BRAKET_SETUP / BRAKET_FORMULA / CONJ / INNER_PRODUCT
    - TIME_COMPONENT / TIME_EVOLVE
    - CX_M / CX_A: exact complex multiplication and addition
    - Z: inner product or evolved ket
    """

    VARIANTS = ["inner_product", "time_evolution"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "inner_product":
            problem, steps, answer = self._generate_inner_product()
        else:
            problem, steps, answer = self._generate_time_evolution()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"braket_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_inner_product(self):
        dim = random.choice([2, 3])
        phi = random_vector(dim)
        psi = random_vector(dim)
        steps = [
            step("BRAKET_SETUP", "inner_product",
                 f"phi={vector_text(phi)}", f"psi={vector_text(psi)}"),
            step("BRAKET_FORMULA", "inner(phi,psi)=sum conj(phi_k)*psi_k"),
        ]
        products = []
        for idx, (left, right) in enumerate(zip(phi, psi), start=1):
            left_conj = conj(left)
            product = mul(left_conj, right)
            products.append(product)
            steps.extend([
                step("CONJ", f"phi_{idx}={complex_text(left)}",
                     complex_text(left_conj)),
                step("CX_M", complex_text(left_conj), complex_text(right),
                     complex_text(product)),
            ])
        running = products[0]
        for product in products[1:]:
            new_running = add(running, product)
            steps.append(step("CX_A", complex_text(running),
                              complex_text(product),
                              complex_text(new_running)))
            running = new_running
        result = complex_text(running)
        steps.append(step("INNER_PRODUCT", "inner(phi,psi)", result))
        answer = f"inner(phi,psi)={result}"
        problem = (
            f"Given phi={vector_text(phi)} and psi={vector_text(psi)}, "
            "compute inner(phi,psi)=conj(phi) dot psi."
        )
        return problem, steps, answer

    def _generate_time_evolution(self):
        dim = random.choice([2, 3])
        psi = random_vector(dim)
        phases = [random.choice(PHASES) for _ in range(dim)]
        result = [mul(phase, value) for phase, value in zip(phases, psi)]
        steps = [
            step("BRAKET_SETUP", "time_evolution",
                 f"psi={vector_text(psi)}", f"phases={vector_text(phases)}"),
            step("BRAKET_FORMULA", "U=diag(phases)"),
        ]
        for idx, (phase, value, evolved) in enumerate(
                zip(phases, psi, result), start=1):
            steps.extend([
                step("CX_M", complex_text(phase), complex_text(value),
                     complex_text(evolved)),
                step("TIME_COMPONENT", f"k={idx}", complex_text(evolved)),
            ])
        result_text = vector_text(result)
        steps.append(step("TIME_EVOLVE", "U psi", result_text))
        answer = f"U psi={result_text}"
        problem = (
            "A diagonal Hamiltonian gives time-evolution phases "
            f"{vector_text(phases)} in its eigenbasis. For ket "
            f"psi={vector_text(psi)}, compute U psi."
        )
        return problem, steps, answer
