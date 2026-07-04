import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.matrix_ops_generator import mat


ORTHO_2 = [
    [[1, 1], [1, -1]],
    [[2, 1], [-1, 2]],
    [[3, 0], [0, 2]],
]

ORTHO_3 = [
    [[1, 1, 1], [1, -1, 0], [1, 1, -2]],
    [[2, 1, 0], [-1, 2, 0], [0, 0, 1]],
    [[1, 0, 1], [1, 0, -1], [0, 1, 0]],
]


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def fmt_num(value):
    value = Fraction(value)
    text = fmt_frac(value)
    return f"({text})" if value < 0 else text


def fmt_vec(v):
    return "[" + ", ".join(fmt_frac(x) for x in v) + "]"


def product_expr(a, b):
    a, b = Fraction(a), Fraction(b)
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


def dot(a, b):
    return sum(Fraction(x) * Fraction(y) for x, y in zip(a, b))


def dot_expr(a, b):
    terms = [product_expr(x, y) for x, y in zip(a, b) if x * y != 0]
    return " + ".join(terms) if terms else "0"


def scalar_label(coeff, name):
    coeff = Fraction(coeff)
    if coeff == 1:
        return name
    if coeff == -1:
        return f"-{name}"
    return f"{fmt_frac(coeff)}*{name}"


def vec_add(a, b):
    return [Fraction(x) + Fraction(y) for x, y in zip(a, b)]


def vec_sub(a, b):
    return [Fraction(x) - Fraction(y) for x, y in zip(a, b)]


def scalar_vec(c, v):
    return [Fraction(c) * Fraction(x) for x in v]


def scale_vec(c, v):
    return [c * x for x in v]


def mix_vectors(qs):
    coeffs = [random.choice([-3, -2, -1, 1, 2, 3])
              for _ in range(3)]
    if len(qs) == 2:
        return [qs[0], vec_add(qs[1], scale_vec(coeffs[0], qs[0]))]
    v1 = qs[0]
    v2 = vec_add(qs[1], scale_vec(coeffs[0], qs[0]))
    v3 = vec_add(vec_add(qs[2], scale_vec(coeffs[1], qs[0])),
                 scale_vec(coeffs[2], qs[1]))
    return [v1, v2, v3]


def random_basis(n):
    base = random.choice(ORTHO_2 if n == 2 else ORTHO_3)
    return [
        scale_vec(random.choice([1, 2, -1]), row)
        for row in base
    ]


def gram_schmidt(vectors):
    basis = []
    records = []
    for i, v in enumerate(vectors):
        current = [Fraction(x) for x in v]
        projections = []
        for j, u in enumerate(basis):
            numerator = dot(v, u)
            denominator = dot(u, u)
            coeff = numerator / denominator
            projection = scalar_vec(coeff, u)
            current = vec_sub(current, projection)
            projections.append((j, numerator, denominator, coeff,
                                projection, current))
        basis.append(current)
        records.append(projections)
    return basis, records


class GramSchmidtGenerator(ProblemGenerator):
    """
    Gram-Schmidt orthogonalization for two vectors in R2 or three vectors in
    R3. The requested output is an exact orthogonal basis, not a normalized
    basis, so no radicals are needed.

    Variants: two and three.

    Op-codes used:
    - GS_SETUP: vectors and goal
    - GS_VECTOR: start or finish one orthogonal vector
    - DOT (established): projection dot products
    - PROJ_COEFF: dot ratio for a projection
    - PROJ_VECTOR: projection vector
    - GS_SUBTRACT: subtract projection from the working vector
    - CHECK (established): pairwise orthogonality
    - Z: orthogonal basis
    """

    VARIANTS = ["two", "three"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        count = 2 if variant == "two" else 3
        original_orthogonal = random_basis(count)
        vectors = mix_vectors(original_orthogonal)
        basis, records = gram_schmidt(vectors)

        steps = [
            step("GS_SETUP", f"vectors {mat(vectors)}",
                 "orthogonal basis, not normalized"),
            step("GS_VECTOR", "u1 = v1", fmt_vec(basis[0])),
        ]
        for i in range(1, count):
            steps.append(step("GS_VECTOR", f"start v{i + 1}",
                              fmt_vec(vectors[i])))
            for j, numerator, denominator, coeff, projection, current in (
                    records[i]):
                steps.append(step("DOT", f"v{i + 1}·u{j + 1}",
                                  dot_expr(vectors[i], basis[j]),
                                  fmt_frac(numerator)))
                steps.append(step("DOT", f"u{j + 1}·u{j + 1}",
                                  dot_expr(basis[j], basis[j]),
                                  fmt_frac(denominator)))
                steps.append(step("PROJ_COEFF", f"v{i + 1} on u{j + 1}",
                                  f"{fmt_frac(numerator)}/"
                                  f"{fmt_frac(denominator)}",
                                  fmt_frac(coeff)))
                steps.append(step("PROJ_VECTOR",
                                  scalar_label(coeff, f"u{j + 1}"),
                                  fmt_vec(projection)))
                steps.append(step("GS_SUBTRACT",
                                  f"remove projection on u{j + 1}",
                                  fmt_vec(current)))
            steps.append(step("GS_VECTOR", f"u{i + 1}", fmt_vec(basis[i])))

        for i in range(count):
            for j in range(i + 1, count):
                steps.append(step("CHECK", f"u{i + 1}·u{j + 1}",
                                  fmt_frac(dot(basis[i], basis[j])),
                                  "orthogonal"))

        answer = f"orthogonal basis {mat(basis)}"
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"gram_schmidt_{variant}",
            problem=(f"Apply Gram-Schmidt to vectors {mat(vectors)} and "
                     f"give an orthogonal basis, not normalized."),
            steps=steps,
            final_answer=answer,
        )
