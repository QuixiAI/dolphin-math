import random

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.diagonalization_generator import (
    columns_to_matrix,
    inverse_2x2,
    matmul,
    scalar_vector_text,
    unimodular_matrix,
)
from generators.eigenvalue_generator import matvec, null_vector, subtract_lambda
from generators.matrix_ops_generator import mat


def exp_text(lam):
    if lam == 1:
        return "e^t"
    if lam == -1:
        return "e^(-t)"
    return f"e^({lam}t)"


def combo_text(terms):
    pieces = []
    for coeff, lam in terms:
        if coeff == 0:
            continue
        body = exp_text(lam) if abs(coeff) == 1 else (
            f"{abs(coeff)}*{exp_text(lam)}"
        )
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return " ".join(pieces) if pieces else "0"


def symbolic_matrix(entries):
    return "[" + ", ".join(
        "[" + ", ".join(row) + "]" for row in entries
    ) + "]"


def exp_entries(P, P_inv, lambdas):
    entries = []
    term_records = []
    for i in range(2):
        row = []
        record_row = []
        for j in range(2):
            terms = [
                (P[i][0] * P_inv[0][j], lambdas[0]),
                (P[i][1] * P_inv[1][j], lambdas[1]),
            ]
            row.append(combo_text(terms))
            record_row.append(terms)
        entries.append(row)
        term_records.append(record_row)
    return entries, term_records


class MatrixExponentialGenerator(ProblemGenerator):
    """
    Matrix exponential for diagonalizable 2x2 matrices:
    e^(At) = P*e^(Dt)*P^-1. Eigenvalues are small distinct integers and P is
    unimodular, so the symbolic entries are exact linear combinations of
    e^(lambda t) terms.

    Op-codes used:
    - MAT_SETUP (established): matrix and goal
    - EIGENVALUE / EIGENVECTOR (established): eigenpairs
    - CHECK (established): Av = lambda v and e^(A0) = I
    - DIAG_FORM (established): P, D, and P^-1
    - EXP_DIAG: e^(Dt)
    - EXP_FORM: e^(At) = P*e^(Dt)*P^-1
    - EXP_ENTRY: one symbolic entry of e^(At)
    - Z: e^(At)
    """

    def generate(self) -> dict:
        lambdas = sorted(random.sample([-3, -2, -1, 1, 2, 3], 2))
        raw_p = unimodular_matrix()
        raw_p_inv = inverse_2x2(raw_p)
        D = [[lambdas[0], 0], [0, lambdas[1]]]
        A = matmul(matmul(raw_p, D), raw_p_inv)
        vectors = [null_vector(subtract_lambda(A, lam)) for lam in lambdas]
        P = columns_to_matrix(vectors)
        P_inv = inverse_2x2(P)
        entries, term_records = exp_entries(P, P_inv, lambdas)
        expD = [[exp_text(lambdas[0]), "0"], ["0", exp_text(lambdas[1])]]

        steps = [
            step("MAT_SETUP", f"A = {mat(A)}", "compute e^(At)"),
        ]
        for lam, vec in zip(lambdas, vectors):
            Av = matvec(A, vec)
            lv = [lam * value for value in vec]
            steps.extend([
                step("EIGENVALUE", f"λ = {lam}", f"diagonal entry of D"),
                step("EIGENVECTOR", f"λ = {lam}", str(vec)),
                step("CHECK", f"A*{vec}", str(Av),
                     scalar_vector_text(lam, lv)),
            ])
        steps.extend([
            step("DIAG_FORM", f"P = {mat(P)}", f"D = {mat(D)}",
                 f"P^-1 = {mat(P_inv)}"),
            step("EXP_DIAG", "e^(Dt)", symbolic_matrix(expD)),
            step("EXP_FORM", "e^(At) = P*e^(Dt)*P^-1"),
        ])
        for i in range(2):
            for j in range(2):
                raw_terms = combo_text(term_records[i][j])
                steps.append(step("EXP_ENTRY", f"({i + 1},{j + 1})",
                                  raw_terms, entries[i][j]))
        steps.append(step("CHECK", "t = 0", mat([[1, 0], [0, 1]]),
                          "identity"))

        answer = f"e^(At)={symbolic_matrix(entries)}"
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="matrix_exponential_diagonalizable",
            problem=f"Find e^(At) for A = {mat(A)} by diagonalization.",
            steps=steps,
            final_answer=answer,
        )
