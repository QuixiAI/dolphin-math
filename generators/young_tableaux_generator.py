import math
import random

from base_generator import ProblemGenerator
from helpers import step, jid


def partitions(n, max_part=None):
    max_part = n if max_part is None else min(max_part, n)
    if n == 0:
        return [[]]
    result = []
    for first in range(max_part, 0, -1):
        for rest in partitions(n - first, first):
            result.append([first] + rest)
    return result


PARTITIONS = [
    part
    for n in range(4, 13)
    for part in partitions(n)
]

SU3_DECOMPS = [
    ("3", 3, "3bar", 3, [("8", 8), ("1", 1)],
     "box plus antibox gives adjoint plus singlet"),
    ("3", 3, "3", 3, [("6", 6), ("3bar", 3)],
     "two boxes split into symmetric plus antisymmetric"),
    ("3bar", 3, "3bar", 3, [("6bar", 6), ("3", 3)],
     "two antiboxes split into symmetric plus antisymmetric"),
    ("8", 8, "3", 3, [("15", 15), ("6bar", 6), ("3", 3)],
     "attach one box to the adjoint tableau"),
    ("8", 8, "3bar", 3, [("15bar", 15), ("6", 6), ("3bar", 3)],
     "attach one antibox to the adjoint tableau"),
]


def partition_text(partition):
    return "[" + ",".join(str(value) for value in partition) + "]"


def hook_length(partition, row, col):
    right = partition[row - 1] - col
    below = sum(1 for size in partition[row:] if size >= col)
    return right, below, right + below + 1


def component_text(components):
    return " + ".join(label for label, _ in components)


class YoungTableauxGenerator(ProblemGenerator):
    """
    Young-tableaux arithmetic for representation dimensions and simple SU(3)
    tensor-product decompositions.

    Variants:
    - hook_length: S_n irreducible dimension n! / product hooks.
    - su3_decomposition: small SU(3) product decompositions with dimension
      checks.

    Op-codes used:
    - YOUNG_SETUP / HOOK / FACT / SU3_SETUP / TABLEAU_RULE / REP_DIM / CHECK
    - M / A / D (established/shared): exact integer arithmetic
    - Z: dimension or decomposition result
    """

    VARIANTS = ["hook_length", "su3_decomposition"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "hook_length":
            problem, steps, answer = self._generate_hook_length()
        else:
            problem, steps, answer = self._generate_su3_decomposition()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"young_tableaux_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_hook_length(self):
        partition = random.choice(PARTITIONS)
        n = sum(partition)
        hooks = []
        steps = [
            step("YOUNG_SETUP", f"partition={partition_text(partition)}",
                 f"n={n}", f"group=S_{n}"),
        ]
        for row, row_len in enumerate(partition, start=1):
            for col in range(1, row_len + 1):
                right, below, hook = hook_length(partition, row, col)
                hooks.append(hook)
                steps.append(step("HOOK", f"({row},{col})",
                                  f"right={right}", f"below={below}",
                                  f"hook={hook}"))
        hook_product = 1
        for hook in hooks:
            new_product = hook_product * hook
            steps.append(step("M", hook_product, hook, new_product))
            hook_product = new_product
        factorial = math.factorial(n)
        dimension = factorial // hook_product
        steps.extend([
            step("FACT", n, factorial),
            step("D", factorial, hook_product, dimension),
            step("CHECK", "n! divisible by hook product", "yes",
                 "integer dimension"),
        ])
        answer = f"dim S_{n}{partition_text(partition)} = {dimension}"
        problem = (
            f"Use the hook-length formula to find the S_{n} representation "
            f"dimension for partition {partition_text(partition)}."
        )
        return problem, steps, answer

    def _generate_su3_decomposition(self):
        left, left_dim, right, right_dim, components, rule = random.choice(
            SU3_DECOMPS
        )
        product_dim = left_dim * right_dim
        steps = [
            step("SU3_SETUP", f"left={left}", f"right={right}"),
            step("TABLEAU_RULE", f"{left} x {right}", rule,
                 component_text(components)),
            step("M", left_dim, right_dim, product_dim),
        ]
        running = 0
        for label, dim in components:
            steps.append(step("REP_DIM", label, dim))
            new_running = running + dim
            steps.append(step("A", running, dim, new_running))
            running = new_running
        steps.append(step("CHECK", "dimension balance",
                          f"{product_dim}={running}", "ok"))
        answer = f"{left} x {right} = {component_text(components)}"
        problem = (
            f"Use SU(3) Young-tableau rules to decompose {left} x {right} "
            "and check dimensions."
        )
        return problem, steps, answer
