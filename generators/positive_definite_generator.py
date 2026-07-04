import random

from base_generator import ProblemGenerator
from helpers import step, jid


VARIANTS = ["positive", "not_positive"]


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def is_positive_definite(matrix):
    delta1 = matrix[0][0]
    det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return delta1 > 0 and det > 0


def positive_matrix():
    p = random.randint(1, 5)
    q = random.randint(-4, 4)
    r = random.randint(1, 5)
    return [
        [p * p, p * q],
        [p * q, q * q + r * r],
    ]


def non_positive_matrix():
    for _ in range(100):
        a = random.randint(-5, 5)
        b = random.randint(-6, 6)
        c = random.randint(-5, 5)
        matrix = [[a, b], [b, c]]
        if not is_positive_definite(matrix):
            return matrix
    return [[0, 1], [1, 0]]


class PositiveDefiniteGenerator(ProblemGenerator):
    """
    Positive-definiteness checks by Sylvester's criterion for 2x2 matrices.

    Variants:
    - positive: construct A=L L^T so both leading principal minors are positive.
    - not_positive: random symmetric matrix failing at least one minor.

    Op-codes used:
    - PD_SETUP / LEADING_MINOR / CHECK
    - M / S (established/shared): determinant arithmetic
    - Z: positive_definite or not_positive_definite
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        matrix = positive_matrix() if variant == "positive" else non_positive_matrix()
        a, b = matrix[0]
        _, c = matrix[1]
        ac = a * c
        b2 = b * b
        det = ac - b2
        positive = a > 0 and det > 0
        steps = [
            step("PD_SETUP", f"A={matrix_text(matrix)}",
                 "Sylvester criterion"),
            step("LEADING_MINOR", "Delta1", a),
            step("CHECK", "Delta1 > 0", f"{a} > 0",
                 "true" if a > 0 else "false"),
            step("M", a, c, ac),
            step("M", b, b, b2),
            step("S", ac, b2, det),
            step("LEADING_MINOR", "Delta2", det),
            step("CHECK", "Delta2 > 0", f"{det} > 0",
                 "true" if det > 0 else "false"),
            step("CHECK", "all leading minors positive",
                 "true" if positive else "false"),
        ]
        answer = "positive_definite" if positive else "not_positive_definite"
        steps.append(step("Z", answer))
        problem = (
            f"Use Sylvester's criterion to decide whether A={matrix_text(matrix)} "
            "is positive definite."
        )
        return dict(
            problem_id=jid(),
            operation=f"positive_definite_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
