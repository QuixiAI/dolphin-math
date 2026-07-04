import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


VARIANTS = ["polynomial_gram", "rbf_gram"]
LABELS = ["A", "B", "C"]


def fraction_text(value):
    return str(Fraction(value))


def vector_text(vector):
    return "(" + ",".join(fraction_text(value) for value in vector) + ")"


def points_text(labels, vectors):
    return ", ".join(
        f"{label}={vector_text(vector)}"
        for label, vector in zip(labels, vectors)
    )


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def exp_text(scale):
    scale = Fraction(scale)
    if scale == 0:
        return "1"
    return f"exp(-{fraction_text(scale)})"


class KernelEvaluationGenerator(ProblemGenerator):
    """
    Exact kernel evaluations and Gram matrices for small point sets.

    Variants:
    - polynomial_gram: K(x,z) = (x dot z + c)^d
    - rbf_gram: K(x,z) = exp(-gamma ||x-z||^2), kept symbolic and exact

    Op-codes used:
    - KERNEL_SETUP / DOT / KERNEL_BASE / DIST2 / KERNEL_EXPONENT /
      KERNEL_VALUE
    - A / S / M / E (established/shared): dot products, distances, powers
    - Z: exact Gram matrix
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "polynomial_gram":
            problem, steps, answer = self._generate_polynomial()
        else:
            problem, steps, answer = self._generate_rbf()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"kernel_evaluation_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _sample_points(self):
        count = random.choice([2, 3])
        grid = [(x, y) for x in range(-3, 4) for y in range(-3, 4)
                if (x, y) != (0, 0)]
        return random.sample(grid, count)

    def _generate_polynomial(self):
        vectors = self._sample_points()
        labels = LABELS[:len(vectors)]
        constant = random.randint(0, 2)
        degree = random.choice([2, 3])
        steps = [
            step("KERNEL_SETUP", "type=polynomial",
                 f"points={points_text(labels, vectors)}",
                 f"c={constant},d={degree}"),
        ]
        matrix = []
        for row, left in enumerate(vectors):
            matrix_row = []
            for col, right in enumerate(vectors):
                products = [left[i] * right[i] for i in range(2)]
                dot = products[0] + products[1]
                base = dot + constant
                value = base ** degree
                pair = f"{labels[row]},{labels[col]}"
                steps.extend([
                    step("M", left[0], right[0], products[0]),
                    step("M", left[1], right[1], products[1]),
                    step("A", products[0], products[1], dot),
                    step("DOT", pair, dot),
                    step("A", dot, constant, base),
                    step("KERNEL_BASE", pair, f"dot+c={dot}+{constant}",
                         base),
                    step("E", base, degree, value),
                    step("KERNEL_VALUE", pair, value),
                ])
                matrix_row.append(value)
            matrix.append(matrix_row)
        answer = f"K={matrix_text(matrix)}"
        problem = (
            f"Compute the Gram matrix for points {points_text(labels, vectors)} "
            "using polynomial kernel K(x,z)=(x dot z + c)^d "
            f"with c={constant} and d={degree}."
        )
        return problem, steps, answer

    def _generate_rbf(self):
        vectors = self._sample_points()
        labels = LABELS[:len(vectors)]
        gamma = random.choice([Fraction(1, 2), Fraction(1), Fraction(2)])
        steps = [
            step("KERNEL_SETUP", "type=rbf",
                 f"points={points_text(labels, vectors)}",
                 f"gamma={fraction_text(gamma)}"),
        ]
        matrix = []
        for row, left in enumerate(vectors):
            matrix_row = []
            for col, right in enumerate(vectors):
                dx = left[0] - right[0]
                dy = left[1] - right[1]
                dx2 = dx ** 2
                dy2 = dy ** 2
                dist2 = dx2 + dy2
                scale = gamma * dist2
                exponent = -scale
                value = exp_text(scale)
                pair = f"{labels[row]},{labels[col]}"
                steps.extend([
                    step("S", left[0], right[0], dx),
                    step("E", dx, 2, dx2),
                    step("S", left[1], right[1], dy),
                    step("E", dy, 2, dy2),
                    step("A", dx2, dy2, dist2),
                    step("DIST2", pair, dist2),
                    step("M", fraction_text(gamma), dist2,
                         fraction_text(scale)),
                    step("KERNEL_EXPONENT", pair, fraction_text(exponent)),
                    step("KERNEL_VALUE", pair, value),
                ])
                matrix_row.append(value)
            matrix.append(matrix_row)
        answer = f"K={matrix_text(matrix)}"
        problem = (
            f"Compute the Gram matrix for points {points_text(labels, vectors)} "
            "using RBF kernel K(x,z)=exp(-gamma ||x-z||^2) "
            f"with gamma={fraction_text(gamma)}."
        )
        return problem, steps, answer
