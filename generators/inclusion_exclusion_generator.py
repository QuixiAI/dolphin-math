import random

from base_generator import ProblemGenerator
from helpers import step, jid


class InclusionExclusionGenerator(ProblemGenerator):
    """
    Inclusion-exclusion counting for two and three finite sets.

    Variants:
    - two_sets: |A union B| = |A| + |B| - |A intersect B|
    - three_sets: add singles, subtract pair overlaps, add triple overlap

    Op-codes used:
    - IE_SETUP: given set counts
    - IE_FORMULA: inclusion-exclusion formula
    - A / S (established): arithmetic totals
    - Z: requested union size
    """

    VARIANTS = ["two_sets", "three_sets"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "two_sets":
            only_a = random.randint(5, 40)
            only_b = random.randint(5, 40)
            both = random.randint(1, 25)
            A = only_a + both
            B = only_b + both
            union = only_a + only_b + both
            sum_ab = A + B
            steps = [
                step("IE_SETUP", f"n(A)={A}, n(B)={B}",
                     f"n(A intersect B)={both}"),
                step("IE_FORMULA", "n(A union B)",
                     "n(A) + n(B) - n(A intersect B)"),
                step("A", A, B, sum_ab),
                step("S", sum_ab, both, union),
            ]
            problem = (
                f"In a survey, n(A) = {A}, n(B) = {B}, and "
                f"n(A intersect B) = {both}. How many are in A union B?"
            )
            answer = f"n(A union B) = {union}"
        else:
            only_a = random.randint(3, 25)
            only_b = random.randint(3, 25)
            only_c = random.randint(3, 25)
            ab_only = random.randint(1, 12)
            ac_only = random.randint(1, 12)
            bc_only = random.randint(1, 12)
            abc = random.randint(1, 8)
            A = only_a + ab_only + ac_only + abc
            B = only_b + ab_only + bc_only + abc
            C = only_c + ac_only + bc_only + abc
            AB = ab_only + abc
            AC = ac_only + abc
            BC = bc_only + abc
            union = only_a + only_b + only_c + ab_only + ac_only + bc_only + abc
            singles1 = A + B
            singles = singles1 + C
            pairs1 = AB + AC
            pairs = pairs1 + BC
            after_sub = singles - pairs
            steps = [
                step("IE_SETUP", f"n(A)={A}, n(B)={B}, n(C)={C}",
                     f"n(AB)={AB}, n(AC)={AC}, n(BC)={BC}, n(ABC)={abc}"),
                step("IE_FORMULA", "n(A union B union C)",
                     "n(A)+n(B)+n(C) - n(AB)-n(AC)-n(BC) + n(ABC)"),
                step("A", A, B, singles1),
                step("A", singles1, C, singles),
                step("A", AB, AC, pairs1),
                step("A", pairs1, BC, pairs),
                step("S", singles, pairs, after_sub),
                step("A", after_sub, abc, union),
            ]
            problem = (
                f"In a survey, n(A) = {A}, n(B) = {B}, n(C) = {C}, "
                f"n(A intersect B) = {AB}, n(A intersect C) = {AC}, "
                f"n(B intersect C) = {BC}, and n(A intersect B intersect C) = "
                f"{abc}. How many are in A union B union C?"
            )
            answer = f"n(A union B union C) = {union}"

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"inclusion_exclusion_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
