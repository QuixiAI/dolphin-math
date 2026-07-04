import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.matrix_ops_generator import mat, rnd_mat


class MatrixInverseGenerator(ProblemGenerator):
    """
    Inverse of a 2×2 matrix by the adjugate formula: compute the
    determinant, check invertibility, swap/negate, then divide each
    entry. Unimodular matrices give integer inverses; general ones
    give exact fractions; singular matrices are detected and refused.

    Op-codes used:
    - MAT_SETUP / DET_FORMULA / M / S / EVAL (established)
    - CHECK: det ≠ 0 (or = 0) before inverting (established)
    - INV_FORMULA: A⁻¹ = (1/det)·[[d, -b], [-c, a]]
    - REWRITE: the adjugate (established)
    - D: each entry divided by the determinant (established)
    - Z: the inverse matrix, or 'No inverse (det = 0)'
    """

    VARIANTS = ["unimodular", "general", "singular"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choices(
            self.VARIANTS, weights=[40, 45, 15])[0]

        if variant == "singular":
            a, b = (random.choice([v for v in range(-5, 6) if v != 0])
                    for _ in range(2))
            k = random.choice([-2, -1, 2, 3])
            A = [[a, b], [k * a, k * b]]
        else:
            while True:
                A = rnd_mat(2, 2, -6, 6)
                d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
                if variant == "unimodular" and abs(d) == 1:
                    break
                if variant == "general" and abs(d) > 1:
                    break

        a, b = A[0]
        c, dd = A[1]
        p1, p2 = a * dd, b * c
        det = p1 - p2
        steps = [
            step("MAT_SETUP", f"A = {mat(A)}", "A⁻¹"),
            step("DET_FORMULA", "det = ad - bc"),
            step("M", a, dd, p1),
            step("M", b, c, p2),
            step("S", p1, p2, det),
            step("EVAL", "det", det),
        ]
        if det == 0:
            steps.append(step("CHECK", "invertible", "det = 0",
                              "not invertible"))
            answer = "No inverse (det = 0)"
            steps.append(step("Z", answer))
        else:
            steps.append(step("CHECK", "invertible",
                              f"det = {det} ≠ 0", "invertible"))
            steps.append(step("INV_FORMULA",
                              "A⁻¹ = (1/det)·[[d, -b], [-c, a]]"))
            adj = [[dd, -b], [-c, a]]
            steps.append(step("REWRITE", f"adjugate = {mat(adj)}"))
            inv = [[Fraction(adj[i][j], det) for j in range(2)]
                   for i in range(2)]
            if abs(det) != 1:
                for i in range(2):
                    for j in range(2):
                        steps.append(step("D", adj[i][j], det,
                                          inv[i][j]))
            answer = mat(inv)
            steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"matrix_inverse_{variant}",
            problem=f"Find the inverse of A = {mat(A)}, if it exists.",
            steps=steps,
            final_answer=answer,
        )
