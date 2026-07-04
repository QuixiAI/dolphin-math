import random

from base_generator import ProblemGenerator
from helpers import step, jid


VARIANTS = ["linear_form", "quadratic_form"]


def vector_text(values):
    return "(" + ",".join(str(value) for value in values) + ")"


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


class MatrixCalculusGenerator(ProblemGenerator):
    """
    Matrix-calculus gradients for linear and quadratic vector expressions.

    Variants:
    - linear_form: grad_x(a^T x)=a, with the dot-product value shown.
    - quadratic_form: grad_x(x^T A x)=(A+A^T)x for a 2D numeric example.

    Op-codes used:
    - MC_SETUP / GRADIENT_FORMULA / MATRIX_SUM / MAT_ENTRY / GRAD_ENTRY
    - M / A (established/shared): dot products, matrix sum, matrix-vector
      multiplication
    - Z: gradient, and dot-product value for the linear form
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "linear_form":
            problem, steps, answer = self._generate_linear_form()
        else:
            problem, steps, answer = self._generate_quadratic_form()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"matrix_calculus_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_linear_form(self):
        a = [random.randint(-6, 6), random.randint(-6, 6)]
        x = [random.randint(-6, 6), random.randint(-6, 6)]
        term0 = a[0] * x[0]
        term1 = a[1] * x[1]
        value = term0 + term1
        steps = [
            step("MC_SETUP", "expression=a^T x", f"a={vector_text(a)}",
                 f"x={vector_text(x)}"),
            step("GRADIENT_FORMULA", "grad_x(a^T x)=a"),
            step("M", a[0], x[0], term0),
            step("M", a[1], x[1], term1),
            step("A", term0, term1, value),
            step("GRAD_ENTRY", "g1", a[0]),
            step("GRAD_ENTRY", "g2", a[1]),
        ]
        answer = f"grad={vector_text(a)}; value={value}"
        problem = (
            f"For a={vector_text(a)} and x={vector_text(x)}, compute "
            "grad_x(a^T x) and the value a^T x."
        )
        return problem, steps, answer

    def _generate_quadratic_form(self):
        matrix = [
            [random.randint(-4, 4), random.randint(-4, 4)],
            [random.randint(-4, 4), random.randint(-4, 4)],
        ]
        x = [random.randint(-5, 5), random.randint(-5, 5)]
        symmetric = [
            [matrix[row][col] + matrix[col][row] for col in range(2)]
            for row in range(2)
        ]
        gradient = [
            symmetric[row][0] * x[0] + symmetric[row][1] * x[1]
            for row in range(2)
        ]
        steps = [
            step("MC_SETUP", "expression=x^T A x",
                 f"A={matrix_text(matrix)}", f"x={vector_text(x)}"),
            step("GRADIENT_FORMULA", "grad_x(x^T A x)=(A+A^T)x"),
            step("MATRIX_SUM", "B=A+A^T"),
        ]
        for row in range(2):
            for col in range(2):
                steps.append(step("A", matrix[row][col], matrix[col][row],
                                  symmetric[row][col]))
                steps.append(step("MAT_ENTRY", f"B{row + 1}{col + 1}",
                                  symmetric[row][col]))
        for row in range(2):
            term0 = symmetric[row][0] * x[0]
            term1 = symmetric[row][1] * x[1]
            value = term0 + term1
            steps.extend([
                step("M", symmetric[row][0], x[0], term0),
                step("M", symmetric[row][1], x[1], term1),
                step("A", term0, term1, value),
                step("GRAD_ENTRY", f"g{row + 1}", value),
            ])
        answer = f"grad={vector_text(gradient)}"
        problem = (
            f"For A={matrix_text(matrix)} and x={vector_text(x)}, compute "
            "grad_x(x^T A x) using (A+A^T)x."
        )
        return problem, steps, answer
