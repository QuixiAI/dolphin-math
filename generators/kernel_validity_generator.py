import random

from base_generator import ProblemGenerator
from helpers import step, jid


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def bool_text(value):
    return "true" if value else "false"


class KernelValidityGenerator(ProblemGenerator):
    """
    Check whether a small candidate kernel Gram matrix is PSD.

    For a 2x2 symmetric matrix [[a,b],[b,c]], positive semidefiniteness is
    equivalent to all principal minors being nonnegative:
      a >= 0, c >= 0, and ac - b^2 >= 0.

    Op-codes used:
    - PSD_SETUP / PRINCIPAL_MINOR / DET / KERNEL_VALIDITY
    - CHECK (established): nonnegative-minor checks
    - M / S (established/shared): determinant arithmetic
    - Z: PSD truth value and principal minors
    """

    def generate(self) -> dict:
        if random.choice([True, False]):
            a = random.randint(1, 12)
            c = random.randint(1, 12)
            limit = int((a * c) ** 0.5)
            b = random.randint(-limit, limit)
        else:
            a = random.randint(1, 12)
            c = random.randint(1, 12)
            limit = int((a * c) ** 0.5)
            choices = [value for value in range(-14, 15)
                       if abs(value) > limit]
            b = random.choice(choices)
        matrix = [[a, b], [b, c]]
        ac = a * c
        b2 = b * b
        det = ac - b2
        checks = [a >= 0, c >= 0, det >= 0]
        is_psd = all(checks)
        steps = [
            step("PSD_SETUP", f"K={matrix_text(matrix)}",
                 "criterion=all principal minors >= 0"),
            step("PRINCIPAL_MINOR", "K11", a),
            step("CHECK", "K11 >= 0", f"{a} >= 0", bool_text(checks[0])),
            step("PRINCIPAL_MINOR", "K22", c),
            step("CHECK", "K22 >= 0", f"{c} >= 0", bool_text(checks[1])),
            step("M", a, c, ac),
            step("M", b, b, b2),
            step("S", ac, b2, det),
            step("DET", "K", det),
            step("PRINCIPAL_MINOR", "det(K)", det),
            step("CHECK", "det(K) >= 0", f"{det} >= 0",
                 bool_text(checks[2])),
            step("KERNEL_VALIDITY", f"psd={bool_text(is_psd)}"),
        ]
        answer = f"PSD={bool_text(is_psd)}; minors=({a},{c},{det})"
        steps.append(step("Z", answer))
        problem = (
            f"Check whether the candidate kernel Gram matrix K={matrix_text(matrix)} "
            "is PSD using Sylvester's criterion for 2x2 matrices."
        )
        return dict(
            problem_id=jid(),
            operation="kernel_validity_psd_2x2",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
