import random

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.matrix_ops_generator import mat


VARS = ["x1", "x2", "x3", "x4"]


def nz_int(lo=-3, hi=3):
    return random.choice([v for v in range(lo, hi + 1) if v != 0])


def row_op_txt(target, multiplier, source):
    """'R3 -> R3 - 2·R1' for subtracting multiplier times source."""
    if multiplier == 1:
        tail = f"- R{source}"
    elif multiplier == -1:
        tail = f"+ R{source}"
    elif multiplier > 0:
        tail = f"- {multiplier}·R{source}"
    else:
        tail = f"+ {-multiplier}·R{source}"
    return f"R{target} -> R{target} {tail}"


def add_multiple(M, target, source, multiplier):
    M[target] = [
        M[target][j] + multiplier * M[source][j]
        for j in range(len(M[target]))
    ]


def apply_reverse_op(M, target, source, multiplier):
    M[target] = [
        M[target][j] - multiplier * M[source][j]
        for j in range(len(M[target]))
    ]


def linear_combo(terms):
    pieces = []
    for coeff, var in terms:
        if coeff == 0:
            continue
        body = var if abs(coeff) == 1 else f"{abs(coeff)}*{var}"
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return " ".join(pieces) if pieces else "0"


def null_basis_from_rref(R, pivot_cols):
    n = len(R[0])
    free_cols = [j for j in range(n) if j not in pivot_cols]
    basis = []
    for free in free_cols:
        vec = [0] * n
        vec[free] = 1
        for row, pivot in enumerate(pivot_cols):
            vec[pivot] = -R[row][free]
        basis.append(vec)
    return basis


def column_basis(A, pivot_cols):
    return [[row[col] for row in A] for col in pivot_cols]


class SubspaceBasisGenerator(ProblemGenerator):
    """
    RREF, rank, null-space basis, and column-space basis for 3x4 integer
    matrices. Problems are constructed from a known RREF and integer row
    additions, so the row-reduction path uses exact integer arithmetic.

    Variants: rank2 and rank3.

    Op-codes used:
    - MAT_SETUP (established): matrix and goal
    - ROW_OP (established): one row operation and resulting row
    - RREF_RESULT: reduced row echelon form
    - PIVOT_COLS: pivot columns and rank
    - NULL_REL: pivot-variable relation from the RREF
    - NULL_VECTOR: one free-variable basis vector
    - COL_BASIS: original pivot columns
    - Z: rank, null basis, and column basis
    """

    VARIANTS = ["rank2", "rank3"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _rref(rank):
        coeffs = [random.randint(-4, 4) for _ in range(4)]
        if rank == 2:
            a, b, c, d = coeffs
            return [[1, 0, a, b], [0, 1, c, d], [0, 0, 0, 0]]
        a, b, c, _ = coeffs
        return [[1, 0, 0, a], [0, 1, 0, b], [0, 0, 1, c]]

    @staticmethod
    def _forward_ops(rank):
        if rank == 2:
            return [
                (1, 0, nz_int()),
                (2, 0, nz_int()),
                (2, 1, nz_int()),
                (0, 1, nz_int()),
            ]
        return [
            (1, 0, nz_int()),
            (2, 1, nz_int()),
            (0, 2, nz_int()),
            (2, 0, nz_int()),
        ]

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        rank = 2 if variant == "rank2" else 3
        pivot_cols = list(range(rank))
        R = self._rref(rank)
        forward_ops = self._forward_ops(rank)
        A = [row[:] for row in R]
        for target, source, multiplier in forward_ops:
            add_multiple(A, target, source, multiplier)

        steps = [
            step("MAT_SETUP", f"A = {mat(A)}",
                 "RREF, rank, null space, column space")
        ]
        work = [row[:] for row in A]
        for target, source, multiplier in reversed(forward_ops):
            apply_reverse_op(work, target, source, multiplier)
            steps.append(step("ROW_OP",
                              row_op_txt(target + 1, multiplier,
                                         source + 1),
                              mat([work[target]])[1:-1]))
        steps.append(step("RREF_RESULT", "RREF(A)", mat(work)))
        pivot_text = ", ".join(str(col + 1) for col in pivot_cols)
        steps.append(step("PIVOT_COLS", f"columns {pivot_text}",
                          f"rank = {rank}"))

        free_cols = [j for j in range(4) if j not in pivot_cols]
        for row, pivot in enumerate(pivot_cols):
            equation = linear_combo(
                [(work[row][col], VARS[col]) for col in range(4)]
            )
            relation = linear_combo(
                [(-work[row][free], VARS[free]) for free in free_cols]
            )
            steps.append(step("NULL_REL", f"{equation} = 0",
                              f"{VARS[pivot]} = {relation}"))

        null_basis = null_basis_from_rref(work, pivot_cols)
        for free, vec in zip(free_cols, null_basis):
            assignments = [
                f"{VARS[col]}={1 if col == free else 0}"
                for col in free_cols
            ]
            steps.append(step("NULL_VECTOR", ", ".join(assignments),
                              str(vec)))

        col_basis = column_basis(A, pivot_cols)
        steps.append(step("COL_BASIS", f"original columns {pivot_text}",
                          mat(col_basis)))

        answer = (f"rank {rank}; null basis {mat(null_basis)}; "
                  f"column basis {mat(col_basis)}")
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"subspace_basis_{variant}",
            problem=(f"Find the RREF, rank, null space basis, and column "
                     f"space basis for A = {mat(A)}."),
            steps=steps,
            final_answer=answer,
        )
