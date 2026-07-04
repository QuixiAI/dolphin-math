import random
from fractions import Fraction
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.matrix_ops_generator import mat


def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


def nz_int(lo=-4, hi=4):
    return random.choice([v for v in range(lo, hi + 1) if v != 0])


def subtract_lambda(A, lam):
    return [
        [A[i][j] - (lam if i == j else 0) for j in range(len(A))]
        for i in range(len(A))
    ]


def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v)))
            for i in range(len(A))]


def rref(M):
    work = [[Fraction(v) for v in row] for row in M]
    rows, cols = len(work), len(work[0])
    pivot_cols = []
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows)
                      if work[r][col] != 0), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [v / scale for v in work[pivot_row]]
        for r in range(rows):
            if r == pivot_row or work[r][col] == 0:
                continue
            factor = work[r][col]
            work[r] = [
                work[r][j] - factor * work[pivot_row][j]
                for j in range(cols)
            ]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == rows:
            break
    return work, pivot_cols


def primitive_int_vector(vec):
    scale = 1
    for value in vec:
        scale = lcm(scale, value.denominator)
    ints = [value.numerator * (scale // value.denominator) for value in vec]
    common = 0
    for value in ints:
        common = gcd(common, abs(value))
    ints = [value // common for value in ints]
    first = next(value for value in ints if value != 0)
    if first < 0:
        ints = [-value for value in ints]
    return ints


def null_vector(M):
    R, pivot_cols = rref(M)
    n = len(M[0])
    free_cols = [j for j in range(n) if j not in pivot_cols]
    free = free_cols[0]
    vec = [Fraction(0) for _ in range(n)]
    vec[free] = Fraction(1)
    for row, pivot in enumerate(pivot_cols):
        vec[pivot] = -R[row][free]
    return primitive_int_vector(vec)


def poly_coeffs_from_roots(roots):
    coeffs = [1]
    for root in roots:
        new = [0] * (len(coeffs) + 1)
        for i, coeff in enumerate(coeffs):
            new[i] += coeff
            new[i + 1] -= coeff * root
        coeffs = new
    return coeffs


def poly_text(coeffs):
    degree = len(coeffs) - 1
    pieces = []
    for i, coeff in enumerate(coeffs):
        power = degree - i
        if coeff == 0:
            continue
        abs_coeff = abs(coeff)
        if power == 0:
            body = str(abs_coeff)
        elif power == 1:
            body = "λ" if abs_coeff == 1 else f"{abs_coeff}λ"
        else:
            body = f"λ^{power}" if abs_coeff == 1 else (
                f"{abs_coeff}λ^{power}"
            )
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return " ".join(pieces) if pieces else "0"


def factor_text(root):
    if root == 0:
        return "λ"
    if root > 0:
        return f"(λ - {root})"
    return f"(λ + {-root})"


def factored_text(roots):
    return "*".join(factor_text(root) for root in roots)


def eigenpair_text(lam, vec):
    return f"λ={lam}: span({vec})"


def shifted_matrix_label(lam):
    if lam < 0:
        return f"A + {-lam}I"
    if lam == 0:
        return "A"
    return f"A - {lam}I"


class EigenvalueGenerator(ProblemGenerator):
    """
    Eigenvalues and eigenvectors for 2x2 and 3x3 upper-triangular matrices
    with distinct integer eigenvalues. The characteristic polynomial is shown
    from det(lambda I - A), then each eigenspace solves (A - lambda I)v = 0.

    Variants: two and three.

    Op-codes used:
    - MAT_SETUP (established): matrix and goal
    - CHAR_SETUP: characteristic determinant setup
    - CHAR_DIAG: diagonal factors of lambda I - A
    - CHAR_POLY: expanded and factored characteristic polynomial
    - EIGENVALUE: one root of the characteristic polynomial
    - EIGEN_MATRIX: A - lambda I
    - EIGENVECTOR: a basis vector for the eigenspace
    - CHECK (established): A*v equals lambda*v
    - Z: characteristic polynomial and eigenpairs
    """

    VARIANTS = ["two", "three"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _matrix(n):
        roots = random.sample(range(-5, 6), n)
        if n == 2:
            A = [[roots[0], nz_int()], [0, roots[1]]]
        else:
            A = [
                [roots[0], nz_int(), nz_int()],
                [0, roots[1], nz_int()],
                [0, 0, roots[2]],
            ]
        return A, sorted(roots)

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        n = 2 if variant == "two" else 3
        A, roots = self._matrix(n)
        coeffs = poly_coeffs_from_roots(roots)
        expanded = poly_text(coeffs)
        factored = factored_text(roots)
        diag_factors = ", ".join(factor_text(A[i][i]) for i in range(n))

        steps = [
            step("MAT_SETUP", f"A = {mat(A)}",
                 "characteristic polynomial and eigenvectors"),
            step("CHAR_SETUP", "p(λ) = det(λI - A)",
                 "triangular determinant"),
            step("CHAR_DIAG", "diagonal of λI - A", diag_factors),
            step("CHAR_POLY", f"p(λ) = {expanded}", factored),
        ]

        eigenpairs = []
        for lam in roots:
            eig_matrix = subtract_lambda(A, lam)
            vec = null_vector(eig_matrix)
            Av = matvec(A, vec)
            lv = [lam * value for value in vec]
            eig_label = shifted_matrix_label(lam)
            steps.extend([
                step("EIGENVALUE", f"λ = {lam}", f"p({lam}) = 0"),
                step("EIGEN_MATRIX", eig_label, mat(eig_matrix)),
                step("EIGENVECTOR", f"{eig_label} times v = 0", str(vec)),
                step("CHECK", f"A*{vec}", str(Av), f"{lam}*v = {lv}"),
            ])
            eigenpairs.append(eigenpair_text(lam, vec))

        answer = (f"p(λ)={expanded} = {factored}; eigenpairs "
                  f"{', '.join(eigenpairs)}")
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"eigenvalues_{variant}",
            problem=(f"Find the characteristic polynomial, eigenvalues, "
                     f"and eigenvectors of A = {mat(A)}."),
            steps=steps,
            final_answer=answer,
        )
