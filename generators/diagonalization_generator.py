import random

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.eigenvalue_generator import (
    factored_text,
    matvec,
    null_vector,
    poly_coeffs_from_roots,
    poly_text,
    subtract_lambda,
)
from generators.matrix_ops_generator import mat


def fmt_num(n):
    return f"({n})" if n < 0 else str(n)


def product_expr(a, b):
    if a == 0 or b == 0:
        return "0"
    if a == 1:
        return fmt_num(b)
    if b == 1:
        return fmt_num(a)
    if a == -1:
        return fmt_num(-b)
    if b == -1:
        return fmt_num(-a)
    return f"{fmt_num(a)}*{fmt_num(b)}"


def product_sum_expr(*pairs):
    terms = [product_expr(a, b) for a, b in pairs if a * b != 0]
    if not terms:
        return "0"
    return " + ".join(terms)


def matmul(A, B):
    return [
        [sum(A[i][k] * B[k][j] for k in range(len(B)))
         for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def inverse_2x2(A):
    a, b = A[0]
    c, d = A[1]
    det = a * d - b * c
    return [[d // det, -b // det], [-c // det, a // det]]


def matrix_power(A, k):
    result = [[1, 0], [0, 1]]
    for _ in range(k):
        result = matmul(result, A)
    return result


def columns_to_matrix(cols):
    return [[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]]


def scalar_vector_text(lam, lv):
    if lam == 1:
        return f"v = {lv}"
    if lam == -1:
        return f"-v = {lv}"
    return f"{lam}*v = {lv}"


def unimodular_matrix():
    a = random.choice([-2, -1, 1, 2])
    b = random.choice([-2, -1, 1, 2])
    return [[1, a], [b, 1 + a * b]]


class DiagonalizationGenerator(ProblemGenerator):
    """
    Diagonalize a 2x2 matrix with two distinct integer eigenvalues and use
    A^k = P*D^k*P^-1 to compute a matrix power. Matrices are built from a
    unimodular eigenvector matrix so every displayed matrix stays integral.

    Op-codes used:
    - MAT_SETUP (established): matrix, exponent, and goal
    - CHAR_POLY (established): characteristic polynomial
    - EIGENVALUE / EIGENVECTOR (established): eigenpairs
    - CHECK (established): Av = lambda v and P*D*P^-1 = A
    - DIAG_FORM: P, D, and P^-1
    - E / D_POWER: diagonal power computation
    - POWER_FORM: A^k = P*D^k*P^-1
    - POWER_ENTRY: each entry of A^k from the matrix product
    - Z: P, D, P^-1, and A^k
    """

    def generate(self) -> dict:
        lambdas = sorted(random.sample([-3, -2, -1, 2, 3], 2))
        raw_p = unimodular_matrix()
        raw_p_inv = inverse_2x2(raw_p)
        D = [[lambdas[0], 0], [0, lambdas[1]]]
        A = matmul(matmul(raw_p, D), raw_p_inv)
        k = random.randint(2, 4)

        vectors = [
            null_vector(subtract_lambda(A, lam))
            for lam in lambdas
        ]
        P = columns_to_matrix(vectors)
        P_inv = inverse_2x2(P)
        Dk = [[lambdas[0] ** k, 0], [0, lambdas[1] ** k]]
        B = matmul(P, Dk)
        Ak = matmul(B, P_inv)
        direct = matrix_power(A, k)
        assert direct == Ak

        coeffs = poly_coeffs_from_roots(lambdas)
        expanded = poly_text(coeffs)
        factored = factored_text(lambdas)

        steps = [
            step("MAT_SETUP", f"A = {mat(A)}, k = {k}",
                 "diagonalize and compute A^k"),
            step("CHAR_POLY", f"p(λ) = {expanded}", factored),
        ]
        for lam, vec in zip(lambdas, vectors):
            Av = matvec(A, vec)
            lv = [lam * value for value in vec]
            steps.extend([
                step("EIGENVALUE", f"λ = {lam}", f"p({lam}) = 0"),
                step("EIGENVECTOR", f"λ = {lam}", str(vec)),
                step("CHECK", f"A*{vec}", str(Av),
                     scalar_vector_text(lam, lv)),
            ])

        steps.extend([
            step("DIAG_FORM", f"P = {mat(P)}", f"D = {mat(D)}",
                 f"P^-1 = {mat(P_inv)}"),
            step("CHECK", "P*D*P^-1", mat(A), "matches A"),
            step("E", lambdas[0], k, Dk[0][0]),
            step("E", lambdas[1], k, Dk[1][1]),
            step("D_POWER", f"D^{k}", mat(Dk)),
            step("POWER_FORM", f"A^{k} = P*D^{k}*P^-1"),
        ])

        for i in range(2):
            for j in range(2):
                expr = product_sum_expr(
                    (B[i][0], P_inv[0][j]),
                    (B[i][1], P_inv[1][j]),
                )
                steps.append(step("POWER_ENTRY", f"({i + 1},{j + 1})",
                                  expr, Ak[i][j]))
        steps.append(step("CHECK", f"direct A^{k}", mat(direct),
                          "matches diagonalization"))

        answer = (f"P={mat(P)}, D={mat(D)}, P^-1={mat(P_inv)}, "
                  f"A^{k}={mat(Ak)}")
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="diagonalization_power",
            problem=f"Diagonalize A = {mat(A)} and compute A^{k}.",
            steps=steps,
            final_answer=answer,
        )
