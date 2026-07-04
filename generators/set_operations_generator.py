import itertools
import random

from base_generator import ProblemGenerator
from helpers import step, jid


LETTERS = ["a", "b", "c", "d", "e", "f"]
DIGITS = ["1", "2", "3", "4"]


def fmt_set(values):
    return "{" + ", ".join(values) + "}" if values else "{}"


def ordered(values, universe):
    return [value for value in universe if value in values]


def subsets(values):
    out = []
    for size in range(len(values) + 1):
        for combo in itertools.combinations(values, size):
            out.append(list(combo))
    return out


def fmt_power_set(values):
    return "{" + ", ".join(fmt_set(subset) for subset in subsets(values)) + "}"


def fmt_pairs(A, B):
    pairs = [f"({a}, {b})" for a in A for b in B]
    return "{" + ", ".join(pairs) + "}" if pairs else "{}"


class SetOperationsGenerator(ProblemGenerator):
    """
    Finite set algebra, power sets, and Cartesian products.

    Variants:
    - algebra: union, intersection, and difference
    - power_set: list all subsets
    - cartesian_product: list all ordered pairs

    Op-codes used:
    - SET_SETUP: define sets and requested operation
    - ELEMENT_SCAN: element-by-element membership decision
    - SUBSET_SIZE / POWER_SET_RESULT: power-set construction
    - CART_PAIR / CARTESIAN_RESULT: ordered-pair construction
    - COUNT / M / E (established): cardinality arithmetic
    - Z: exact set result
    """

    VARIANTS = ["algebra", "power_set", "cartesian_product"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _subset(pool, min_size=1, max_size=4):
        size = random.randint(min_size, max_size)
        return sorted(random.sample(pool, size), key=pool.index)

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "algebra":
            A = self._subset(LETTERS)
            B = self._subset(LETTERS)
            op = random.choice(["union", "intersect", "minus"])
            if op == "union":
                result = ordered(set(A) | set(B), LETTERS)
                problem = f"Given A = {fmt_set(A)} and B = {fmt_set(B)}, find A union B."
            elif op == "intersect":
                result = ordered(set(A) & set(B), LETTERS)
                problem = f"Given A = {fmt_set(A)} and B = {fmt_set(B)}, find A intersect B."
            else:
                result = ordered(set(A) - set(B), LETTERS)
                problem = f"Given A = {fmt_set(A)} and B = {fmt_set(B)}, find A minus B."
            answer = fmt_set(result)
            steps = [
                step("SET_SETUP", f"A = {fmt_set(A)}", f"B = {fmt_set(B)}",
                     op),
            ]
            for element in LETTERS:
                in_a = element in A
                in_b = element in B
                keep = element in result
                steps.append(step("ELEMENT_SCAN", element,
                                  f"in A={in_a}, in B={in_b}",
                                  "keep" if keep else "skip"))
            steps.append(step("COUNT", "result size", len(result)))
        elif variant == "power_set":
            S = self._subset(LETTERS, 2, 4)
            all_subsets = subsets(S)
            answer = f"P(S) = {fmt_power_set(S)}"
            steps = [
                step("SET_SETUP", f"S = {fmt_set(S)}", "power set"),
                step("E", 2, len(S), len(all_subsets)),
            ]
            for size in range(len(S) + 1):
                group = [fmt_set(subset) for subset in all_subsets
                         if len(subset) == size]
                steps.append(step("SUBSET_SIZE", size, ", ".join(group)))
            steps.append(step("POWER_SET_RESULT", fmt_power_set(S)))
            problem = f"Find the power set P(S) for S = {fmt_set(S)}."
        else:
            A = self._subset(LETTERS, 1, 3)
            B = self._subset(DIGITS, 1, 3)
            answer = f"A x B = {fmt_pairs(A, B)}"
            steps = [
                step("SET_SETUP", f"A = {fmt_set(A)}", f"B = {fmt_set(B)}",
                     "cartesian product"),
                step("M", len(A), len(B), len(A) * len(B)),
            ]
            for a in A:
                for b in B:
                    steps.append(step("CART_PAIR", a, b, f"({a}, {b})"))
            steps.append(step("CARTESIAN_RESULT", fmt_pairs(A, B)))
            problem = f"Find A x B for A = {fmt_set(A)} and B = {fmt_set(B)}."

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"set_operations_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
