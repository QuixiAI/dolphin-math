import random
from base_generator import ProblemGenerator
from helpers import step, jid


def mat(m):
    return "[" + ", ".join(
        "[" + ", ".join(str(v) for v in row) + "]" for row in m) + "]"


def rnd_mat(rows, cols, lo=-6, hi=6):
    return [[random.randint(lo, hi) for _ in range(cols)]
            for _ in range(rows)]


class MatrixOpsGenerator(ProblemGenerator):
    """
    Matrix arithmetic with every entry's work shown.

    Variants:
    - add_sub:         entrywise A ± B
    - scalar:          k·A
    - multiply:        2×2 by 2×2; each entry is a row×column pair of
                       products and a sum (M, M, A, then MAT_ENTRY)
    - multiply_vector: 2×2 by 2×1

    Op-codes used:
    - MAT_SETUP: the matrices and the operation (given, goal)
    - A / S / M: entrywise arithmetic (established)
    - MAT_ENTRY: one finished entry of the result (position, value)
    - Z: the result matrix in row-major bracket form
    """

    VARIANTS = ["add_sub", "scalar", "multiply", "multiply_vector"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "add_sub":
            A = rnd_mat(2, 2)
            B = rnd_mat(2, 2)
            minus = random.random() < 0.5
            op = "-" if minus else "+"
            R = [[A[i][j] - B[i][j] if minus else A[i][j] + B[i][j]
                  for j in range(2)] for i in range(2)]
            steps = [step("MAT_SETUP", f"A = {mat(A)}, B = {mat(B)}",
                          f"A {op} B")]
            for i in range(2):
                for j in range(2):
                    steps.append(step("S" if minus else "A",
                                      A[i][j], B[i][j], R[i][j]))
                    steps.append(step("MAT_ENTRY", f"({i + 1},{j + 1})",
                                      R[i][j]))
            problem = (f"Given A = {mat(A)} and B = {mat(B)}, compute "
                       f"A {op} B.")
        elif variant == "scalar":
            A = rnd_mat(2, 2)
            k = random.choice([2, 3, 4, 5, -2, -3])
            R = [[k * A[i][j] for j in range(2)] for i in range(2)]
            steps = [step("MAT_SETUP", f"A = {mat(A)}", f"{k}A")]
            for i in range(2):
                for j in range(2):
                    steps.append(step("M", k, A[i][j], R[i][j]))
                    steps.append(step("MAT_ENTRY", f"({i + 1},{j + 1})",
                                      R[i][j]))
            problem = f"Given A = {mat(A)}, compute {k}A."
        else:
            A = rnd_mat(2, 2, -5, 5)
            cols = 1 if variant == "multiply_vector" else 2
            B = rnd_mat(2, cols, -5, 5)
            R = [[sum(A[i][t] * B[t][j] for t in range(2))
                  for j in range(cols)] for i in range(2)]
            name_b = "v" if cols == 1 else "B"
            goal = f"A{name_b}" if cols == 1 else "AB"
            steps = [step("MAT_SETUP",
                          f"A = {mat(A)}, {name_b} = {mat(B)}", goal)]
            for i in range(2):
                for j in range(cols):
                    p1 = A[i][0] * B[0][j]
                    p2 = A[i][1] * B[1][j]
                    steps.append(step("M", A[i][0], B[0][j], p1))
                    steps.append(step("M", A[i][1], B[1][j], p2))
                    steps.append(step("A", p1, p2, R[i][j]))
                    steps.append(step("MAT_ENTRY",
                                      f"({i + 1},{j + 1})", R[i][j]))
            problem = (f"Given A = {mat(A)} and {name_b} = {mat(B)}, "
                       f"compute {goal}. Show the row-by-column work.")

        answer = mat(R)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"matrix_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
