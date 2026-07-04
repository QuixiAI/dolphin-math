import random
from fractions import Fraction
from math import gcd, isqrt

from base_generator import ProblemGenerator
from helpers import step, jid


def matmul(A, B):
    return [
        [sum(A[i][k] * B[k][j] for k in range(len(B)))
         for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v)))
            for i in range(len(A))]


def det2(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def inverse_2x2_int(A):
    det = det2(A)
    return [[A[1][1] // det, -A[0][1] // det],
            [-A[1][0] // det, A[0][0] // det]]


def fmt_matrix(M):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]"
                           for row in M) + "]"


def fmt_vector(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def fmt_terms(raw_terms):
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        text = body if body and abs(coeff) == 1 else (
            f"{abs(coeff)}{body}" if body else str(abs(coeff))
        )
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def char_poly(trace, det):
    return fmt_terms([(1, "r^2"), (-trace, "r"), (det, "")])


def add_expr(a, b):
    return f"{a} + {b}" if b >= 0 else f"{a} - {abs(b)}"


def eigenvalues(A):
    trace = A[0][0] + A[1][1]
    det = det2(A)
    disc = trace * trace - 4 * det
    root = isqrt(disc)
    return sorted([(trace - root) // 2, (trace + root) // 2])


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


def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


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


def subtract_lambda(A, lam):
    return [
        [A[i][j] - (lam if i == j else 0) for j in range(2)]
        for i in range(2)
    ]


def null_vector(M):
    R, pivot_cols = rref(M)
    free_cols = [j for j in range(2) if j not in pivot_cols]
    vec = [Fraction(0), Fraction(0)]
    vec[free_cols[0]] = Fraction(1)
    for row, pivot in enumerate(pivot_cols):
        vec[pivot] = -R[row][free_cols[0]]
    return primitive_int_vector(vec)


def exp_t(lam):
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
        body = exp_t(lam) if abs(coeff) == 1 else f"{abs(coeff)}{exp_t(lam)}"
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return " ".join(pieces) if pieces else "0"


def solution_vector(constants, lambdas, vectors):
    entries = []
    for row in range(2):
        terms = [
            (constants[i] * vectors[i][row], lambdas[i])
            for i in range(2)
        ]
        entries.append(combo_text(terms))
    return f"x(t) = [{entries[0]}, {entries[1]}]"


def lambda_vec_text(lam, vector):
    if lam == 1:
        return f"v = {fmt_vector(vector)}"
    if lam == -1:
        return f"-v = {fmt_vector(vector)}"
    return f"{lam}v = {fmt_vector(vector)}"


class ODESystemGenerator(ProblemGenerator):
    """
    Linear systems x' = A x solved by eigenvalues and eigenvectors.

    Variant:
    - two_by_two_distinct

    Op-codes used:
    - ODE_SETUP (established): matrix system and initial vector
    - TRACE / DET2 / CHAR_EQ: characteristic polynomial
    - EIGENPAIR / CHECK: eigenvectors and Av=lambda v checks
    - SOL_FORM: eigenmode form of x(t)
    - INITIAL_SYSTEM / SOLVE_CONST: constants from x(0)
    - Z: explicit vector solution
    """

    VARIANTS = ["two_by_two_distinct"]

    BASES = [
        [[1, 1], [0, 1]],
        [[1, 0], [1, 1]],
        [[1, -1], [1, 0]],
        [[2, 1], [1, 1]],
        [[1, 2], [1, 1]],
        [[2, -1], [1, 0]],
    ]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        lambdas = sorted(random.sample([-4, -3, -2, -1, 1, 2, 3, 4], 2))
        P = random.choice(self.BASES)
        D = [[lambdas[0], 0], [0, lambdas[1]]]
        A = matmul(matmul(P, D), inverse_2x2_int(P))
        lambdas = eigenvalues(A)
        vectors = [null_vector(subtract_lambda(A, lam)) for lam in lambdas]
        constants = [
            random.choice([-4, -3, -2, -1, 1, 2, 3, 4]),
            random.choice([-4, -3, -2, -1, 1, 2, 3, 4]),
        ]
        x0 = [
            constants[0] * vectors[0][i] + constants[1] * vectors[1][i]
            for i in range(2)
        ]
        trace = A[0][0] + A[1][1]
        prod_diag = A[0][0] * A[1][1]
        prod_off = A[0][1] * A[1][0]
        det = prod_diag - prod_off
        char = char_poly(trace, det)

        answer = solution_vector(constants, lambdas, vectors)
        steps = [
            step("ODE_SETUP", f"A = {fmt_matrix(A)}",
                 f"x(0) = {fmt_vector(x0)}"),
            step("TRACE", add_expr(A[0][0], A[1][1]), trace),
            step("M", A[0][0], A[1][1], prod_diag),
            step("M", A[0][1], A[1][0], prod_off),
            step("S", prod_diag, prod_off, det),
            step("DET2", "ad - bc", det),
            step("CHAR_EQ", "det(A - rI)", f"{char} = 0"),
        ]
        for lam, vec in zip(lambdas, vectors):
            Av = matvec(A, vec)
            lv = [lam * value for value in vec]
            steps.extend([
                step("EIGENPAIR", f"lambda = {lam}", fmt_vector(vec)),
                step("CHECK", f"A*{fmt_vector(vec)}", fmt_vector(Av),
                     lambda_vec_text(lam, lv)),
            ])
        steps.extend([
            step("SOL_FORM", "x(t)",
                 (f"C1{exp_t(lambdas[0])}{fmt_vector(vectors[0])} + "
                  f"C2{exp_t(lambdas[1])}{fmt_vector(vectors[1])}")),
            step("INITIAL_SYSTEM",
                 f"C1{fmt_vector(vectors[0])} + C2{fmt_vector(vectors[1])}",
                 fmt_vector(x0)),
            step("SOLVE_CONST", f"C1 = {constants[0]}",
                 f"C2 = {constants[1]}"),
            step("Z", answer),
        ])
        problem = (
            f"Solve x' = A x for A = {fmt_matrix(A)} with "
            f"x(0) = {fmt_vector(x0)} using eigenvalues."
        )
        return dict(
            problem_id=jid(),
            operation="ode_system_two_by_two_distinct",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
