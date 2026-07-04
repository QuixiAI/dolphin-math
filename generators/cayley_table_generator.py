import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


D3_ELEMENTS = ["e", "r", "r2", "s", "rs", "r2s"]
D3_PAIRS = {
    "e": (0, 0),
    "r": (1, 0),
    "r2": (2, 0),
    "s": (0, 1),
    "rs": (1, 1),
    "r2s": (2, 1),
}
D3_NAMES = {value: key for key, value in D3_PAIRS.items()}


def list_text(values):
    return ", ".join(str(value) for value in values)


def units(n):
    return [value for value in range(1, n) if gcd(value, n) == 1]


def d3_multiply(left, right):
    i, j = D3_PAIRS[left]
    k, ell = D3_PAIRS[right]
    return D3_NAMES[((i + (-1 if j else 1) * k) % 3, (j + ell) % 2)]


class CayleyTableGenerator(ProblemGenerator):
    """
    Cayley tables and element orders for small finite groups.

    Variants:
    - zn: additive group Z_n
    - units: multiplicative unit group U(n)
    - d3: dihedral group of order 6

    Op-codes used:
    - GROUP_SETUP / CAYLEY_HEADER / CAYLEY_ROW: table construction
    - ORDER_START / ORDER_STEP / ELEMENT_ORDER: element order trace
    - A / M / MOD_REDUCE (established/shared): modular arithmetic
    - Z: requested element order
    """

    VARIANTS = ["zn", "units", "d3"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "zn":
            problem, steps, answer = self._generate_zn()
        elif variant == "units":
            problem, steps, answer = self._generate_units()
        else:
            problem, steps, answer = self._generate_d3()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"cayley_table_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_zn(self):
        n = random.randint(3, 16)
        elements = list(range(n))
        target = random.choice(elements[1:])
        steps = [
            step("GROUP_SETUP", f"Z_{n}", "addition mod n"),
            step("CAYLEY_HEADER", list_text(elements)),
        ]
        for row in elements:
            values = [(row + col) % n for col in elements]
            steps.append(step("CAYLEY_ROW", f"row {row}", list_text(values)))

        current = 0
        steps.append(step("ORDER_START", target, "identity 0"))
        for k in range(1, n + 1):
            previous = current
            total = previous + target
            current = total % n
            steps.append(step("A", previous, target, total))
            steps.append(step("MOD_REDUCE", total, f"mod {n}", current))
            steps.append(step("ORDER_STEP", f"k={k}", current))
            if current == 0:
                order = k
                break
        steps.append(step("ELEMENT_ORDER", target, order))
        answer = f"order({target}) = {order}"
        problem = (
            f"Build the Cayley table for Z_{n} under addition modulo {n} "
            f"and find the order of element {target}."
        )
        return problem, steps, answer

    def _generate_units(self):
        n = random.choice([8, 10, 12, 14, 15, 16, 18, 20, 21, 22,
                           24, 26, 28, 30])
        elements = units(n)
        target = random.choice([value for value in elements if value != 1])
        steps = [
            step("GROUP_SETUP", f"U({n})", "multiplication mod n"),
            step("CAYLEY_HEADER", list_text(elements)),
        ]
        for row in elements:
            values = [(row * col) % n for col in elements]
            steps.append(step("CAYLEY_ROW", f"row {row}", list_text(values)))

        current = 1
        steps.append(step("ORDER_START", target, "identity 1"))
        for k in range(1, len(elements) + 1):
            previous = current
            product = previous * target
            current = product % n
            steps.append(step("M", previous, target, product))
            steps.append(step("MOD_REDUCE", product, f"mod {n}", current))
            steps.append(step("ORDER_STEP", f"k={k}", current))
            if current == 1:
                order = k
                break
        steps.append(step("ELEMENT_ORDER", target, order))
        answer = f"order({target}) = {order}"
        problem = (
            f"Build the Cayley table for U({n}) under multiplication modulo "
            f"{n} and find the order of element {target}."
        )
        return problem, steps, answer

    def _generate_d3(self):
        target = random.choice([element for element in D3_ELEMENTS
                                if element != "e"])
        steps = [
            step("GROUP_SETUP", "D3", "symmetries of a triangle"),
            step("CAYLEY_HEADER", list_text(D3_ELEMENTS)),
        ]
        for row in D3_ELEMENTS:
            values = [d3_multiply(row, col) for col in D3_ELEMENTS]
            steps.append(step("CAYLEY_ROW", f"row {row}", list_text(values)))

        current = "e"
        steps.append(step("ORDER_START", target, "identity e"))
        for k in range(1, 7):
            current = d3_multiply(current, target)
            steps.append(step("ORDER_STEP", f"k={k}", current))
            if current == "e":
                order = k
                break
        steps.append(step("ELEMENT_ORDER", target, order))
        answer = f"order({target}) = {order}"
        problem = (
            "Build the Cayley table for D3 with elements e, r, r2, s, rs, "
            f"r2s and find the order of element {target}."
        )
        return problem, steps, answer
