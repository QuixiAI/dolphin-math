import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.matrix_ops_generator import mat, rnd_mat


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


class DeterminantGenerator(ProblemGenerator):
    """
    Determinants: 2×2 directly (ad - bc), 3×3 by cofactor expansion
    along the first row with each 2×2 minor worked in full and the
    alternating signs applied in the combining chain.

    Op-codes used:
    - MAT_SETUP: the matrix and the goal (established)
    - DET_FORMULA: ad - bc, or the cofactor expansion statement
    - COFACTOR: position, sign, and the minor (position+sign, minor)
    - M / S / A: products and the signed combination (established)
    - EVAL: each minor's determinant and each term (established)
    - Z: the determinant
    """

    VARIANTS = ["two", "three"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "two":
            A = rnd_mat(2, 2, -7, 7)
            p1 = A[0][0] * A[1][1]
            p2 = A[0][1] * A[1][0]
            d = p1 - p2
            steps = [
                step("MAT_SETUP", f"A = {mat(A)}", "det(A)"),
                step("DET_FORMULA", "det = ad - bc"),
                step("M", A[0][0], A[1][1], p1),
                step("M", A[0][1], A[1][0], p2),
                step("S", p1, p2, d),
            ]
            problem = f"Find the determinant of A = {mat(A)}."
        else:
            A = rnd_mat(3, 3, -4, 4)
            terms = []
            steps = [
                step("MAT_SETUP", f"A = {mat(A)}",
                     "det(A) by cofactor expansion along row 1"),
                step("DET_FORMULA",
                     "det = a11·M11 - a12·M12 + a13·M13"),
            ]
            for j in range(3):
                cols = [c for c in range(3) if c != j]
                minor = [[A[1][cols[0]], A[1][cols[1]]],
                         [A[2][cols[0]], A[2][cols[1]]]]
                sign = "+" if j % 2 == 0 else "-"
                steps.append(step("COFACTOR", f"(1,{j + 1}) sign {sign}",
                                  f"minor {mat(minor)}"))
                q1 = minor[0][0] * minor[1][1]
                q2 = minor[0][1] * minor[1][0]
                md = q1 - q2
                steps.append(step("M", minor[0][0], minor[1][1], q1))
                steps.append(step("M", minor[0][1], minor[1][0], q2))
                steps.append(step("S", q1, q2, md))
                t = A[0][j] * md
                steps.append(step("M", A[0][j], md, t))
                steps.append(step("EVAL", f"term {j + 1}", t))
                terms.append(t)
            acc = terms[0]
            steps.append(step("S", acc, terms[1], acc - terms[1]))
            acc -= terms[1]
            steps.append(step("A", acc, terms[2], acc + terms[2]))
            d = acc + terms[2]
            problem = (f"Find the determinant of A = {mat(A)} by "
                       f"cofactor expansion along the first row.")

        answer = str(d)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"determinant_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
