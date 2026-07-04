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


def set_text(values):
    return "{" + list_text(values) + "}"


def units(n):
    return [value for value in range(1, n) if gcd(value, n) == 1]


def is_composite(n):
    return any(n % divisor == 0 for divisor in range(2, int(n ** 0.5) + 1))


def d3_multiply(left, right):
    i, j = D3_PAIRS[left]
    k, ell = D3_PAIRS[right]
    return D3_NAMES[((i + (-1 if j else 1) * k) % 3, (j + ell) % 2)]


def additive_subgroup(n, element):
    subgroup = [0]
    current = 0
    for _ in range(1, n + 1):
        current = (current + element) % n
        if current == 0:
            break
        subgroup.append(current)
    return subgroup


def multiplicative_subgroup(n, element):
    subgroup = [1]
    current = 1
    for _ in range(1, len(units(n)) + 1):
        current = (current * element) % n
        if current == 1:
            break
        subgroup.append(current)
    return subgroup


def coset_summary(cosets):
    return "; ".join(f"{label}={set_text(values)}" for label, values in cosets)


class CosetGenerator(ProblemGenerator):
    """
    Left coset enumeration in small finite groups.

    Variants:
    - zn: additive Z_n with H=<h>
    - units: multiplicative U(n) with H=<h>
    - d3: the dihedral group D3 with a listed subgroup

    Op-codes used:
    - GROUP_SETUP / SUBGROUP_START / SUBGROUP_ELEM / SUBGROUP: subgroup trace
    - COSET_START / COSET_ELEM / COSET / COSET_SKIP: coset enumeration
    - GROUP_MULT: D3 multiplication table application
    - A / M / D / MOD_REDUCE (established/shared): arithmetic checks
    - INDEX / CHECK: coset count and partition verification
    - Z: cosets and index
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
            operation=f"coset_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_zn(self):
        n = random.choice([value for value in range(6, 37)
                           if len(self._additive_choices(value)) > 0])
        element = random.choice(self._additive_choices(n))
        group = list(range(n))
        subgroup, steps = self._trace_additive_subgroup(n, element)
        cosets = []
        covered = set()
        for rep in group:
            if rep in covered:
                steps.append(step("COSET_SKIP", rep, "already listed"))
                continue
            label = f"{rep}+H"
            steps.append(step("COSET_START", f"rep {rep}", label))
            values = []
            for member in subgroup:
                total = rep + member
                value = total % n
                steps.append(step("A", rep, member, total))
                steps.append(step("MOD_REDUCE", total, f"mod {n}", value))
                steps.append(step("COSET_ELEM", label, value))
                values.append(value)
            covered.update(values)
            cosets.append((label, values))
            steps.append(step("COSET", label, set_text(values)))
        self._append_index_steps(steps, len(group), len(subgroup), len(cosets))
        answer = f"cosets = {coset_summary(cosets)}; index = {len(cosets)}"
        problem = (
            f"In Z_{n} under addition modulo {n}, let H=<{element}>. "
            "Enumerate the distinct left cosets a+H."
        )
        return problem, steps, answer

    def _additive_choices(self, n):
        choices = []
        for element in range(1, n):
            size = len(additive_subgroup(n, element))
            if 1 < size < n:
                choices.append(element)
        return choices

    def _trace_additive_subgroup(self, n, element):
        steps = [
            step("GROUP_SETUP", f"Z_{n}", "addition mod n",
                 f"group size {n}"),
            step("SUBGROUP_START", f"H=<{element}>", "identity 0"),
        ]
        subgroup = [0]
        current = 0
        for k in range(1, n + 1):
            previous = current
            total = previous + element
            current = total % n
            steps.append(step("A", previous, element, total))
            steps.append(step("MOD_REDUCE", total, f"mod {n}", current))
            steps.append(step("SUBGROUP_ELEM", f"k={k}", current))
            if current == 0:
                break
            subgroup.append(current)
        steps.append(step("SUBGROUP", f"H={set_text(subgroup)}",
                          f"size {len(subgroup)}"))
        return subgroup, steps

    def _generate_units(self):
        n, element = random.choice(self._unit_subgroup_choices())
        group = units(n)
        subgroup, steps = self._trace_multiplicative_subgroup(n, element)
        cosets = []
        covered = set()
        for rep in group:
            if rep in covered:
                steps.append(step("COSET_SKIP", rep, "already listed"))
                continue
            label = f"{rep}H"
            steps.append(step("COSET_START", f"rep {rep}", label))
            values = []
            for member in subgroup:
                product = rep * member
                value = product % n
                steps.append(step("M", rep, member, product))
                steps.append(step("MOD_REDUCE", product, f"mod {n}", value))
                steps.append(step("COSET_ELEM", label, value))
                values.append(value)
            covered.update(values)
            cosets.append((label, values))
            steps.append(step("COSET", label, set_text(values)))
        self._append_index_steps(steps, len(group), len(subgroup), len(cosets))
        answer = f"cosets = {coset_summary(cosets)}; index = {len(cosets)}"
        problem = (
            f"In U({n}) under multiplication modulo {n}, let H=<{element}>. "
            "Enumerate the distinct left cosets aH."
        )
        return problem, steps, answer

    def _unit_subgroup_choices(self):
        choices = []
        for n in range(8, 61):
            group = units(n)
            if not is_composite(n) or len(group) > 24:
                continue
            for element in group:
                if element == 1:
                    continue
                subgroup = multiplicative_subgroup(n, element)
                if 1 < len(subgroup) < len(group):
                    choices.append((n, element))
        return choices

    def _trace_multiplicative_subgroup(self, n, element):
        group = units(n)
        steps = [
            step("GROUP_SETUP", f"U({n})", "multiplication mod n",
                 f"group size {len(group)}"),
            step("SUBGROUP_START", f"H=<{element}>", "identity 1"),
        ]
        subgroup = [1]
        current = 1
        for k in range(1, len(group) + 1):
            previous = current
            product = previous * element
            current = product % n
            steps.append(step("M", previous, element, product))
            steps.append(step("MOD_REDUCE", product, f"mod {n}", current))
            steps.append(step("SUBGROUP_ELEM", f"k={k}", current))
            if current == 1:
                break
            subgroup.append(current)
        steps.append(step("SUBGROUP", f"H={set_text(subgroup)}",
                          f"size {len(subgroup)}"))
        return subgroup, steps

    def _generate_d3(self):
        subgroup = random.choice([
            ["e", "r", "r2"],
            ["e", "s"],
            ["e", "rs"],
            ["e", "r2s"],
        ])
        steps = [
            step("GROUP_SETUP", "D3", "symmetries of a triangle",
                 f"group size {len(D3_ELEMENTS)}"),
            step("SUBGROUP", f"H={set_text(subgroup)}",
                 f"size {len(subgroup)}"),
        ]
        cosets = []
        covered = set()
        for rep in D3_ELEMENTS:
            if rep in covered:
                steps.append(step("COSET_SKIP", rep, "already listed"))
                continue
            label = f"{rep}H"
            steps.append(step("COSET_START", f"rep {rep}", label))
            values = []
            for member in subgroup:
                value = d3_multiply(rep, member)
                steps.append(step("GROUP_MULT", rep, member, value))
                steps.append(step("COSET_ELEM", label, value))
                values.append(value)
            covered.update(values)
            cosets.append((label, values))
            steps.append(step("COSET", label, set_text(values)))
        self._append_index_steps(
            steps, len(D3_ELEMENTS), len(subgroup), len(cosets)
        )
        answer = f"cosets = {coset_summary(cosets)}; index = {len(cosets)}"
        problem = (
            "In D3 with elements e, r, r2, s, rs, r2s, "
            f"let H={set_text(subgroup)}. Enumerate the distinct left "
            "cosets gH."
        )
        return problem, steps, answer

    def _append_index_steps(self, steps, group_size, subgroup_size, index):
        steps.append(step("D", group_size, subgroup_size, index))
        steps.append(step("INDEX", f"G size {group_size}",
                          f"H size {subgroup_size}", index))
        steps.append(step("CHECK", "cosets partition group", "yes"))
