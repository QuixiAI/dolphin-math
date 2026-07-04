import random

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.de_moivre_generator import TRIG
from generators.matrix_ops_generator import mat


ANGLES = [30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]
TURNS = [-2, -1, 0, 1, 2]

SO3_GENERATORS = {
    "x": [[0, 0, 0], [0, 0, -1], [0, 1, 0]],
    "y": [[0, 0, 1], [0, 0, 0], [-1, 0, 0]],
    "z": [[0, -1, 0], [1, 0, 0], [0, 0, 0]],
}

SO3_SQUARES = {
    "x": [[0, 0, 0], [0, -1, 0], [0, 0, -1]],
    "y": [[-1, 0, 0], [0, 0, 0], [0, 0, -1]],
    "z": [[-1, 0, 0], [0, -1, 0], [0, 0, 0]],
}


def neg_text(value):
    if value == "0":
        return "0"
    if value.startswith("-"):
        return value[1:]
    return f"-{value}"


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ", ".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def so2_matrix(cos_text, sin_text):
    return [[cos_text, neg_text(sin_text)], [sin_text, cos_text]]


def so3_matrix(axis, cos_text, sin_text):
    if axis == "x":
        return [
            ["1", "0", "0"],
            ["0", cos_text, neg_text(sin_text)],
            ["0", sin_text, cos_text],
        ]
    if axis == "y":
        return [
            [cos_text, "0", sin_text],
            ["0", "1", "0"],
            [neg_text(sin_text), "0", cos_text],
        ]
    return [
        [cos_text, neg_text(sin_text), "0"],
        [sin_text, cos_text, "0"],
        ["0", "0", "1"],
    ]


def so3_expr_matrix(axis):
    if axis == "x":
        return [
            ["1", "0", "0"],
            ["0", "cos(theta)", "-sin(theta)"],
            ["0", "sin(theta)", "cos(theta)"],
        ]
    if axis == "y":
        return [
            ["cos(theta)", "0", "sin(theta)"],
            ["0", "1", "0"],
            ["-sin(theta)", "0", "cos(theta)"],
        ]
    return [
        ["cos(theta)", "-sin(theta)", "0"],
        ["sin(theta)", "cos(theta)", "0"],
        ["0", "0", "1"],
    ]


def random_angle():
    angle = random.choice(ANGLES)
    theta = angle + 360 * random.choice(TURNS)
    return theta, angle


class LieExponentialGenerator(ProblemGenerator):
    """
    Exponentiate standard Lie algebra generators into exact rotation matrices.

    Variants:
    - so2: e^(theta J) with J^2 = -I.
    - so3: e^(theta K_axis) with Rodrigues' formula.

    Op-codes used:
    - LIE_EXP_SETUP / MATRIX_POWER / SERIES_GROUP / LIE_EXP_FORM
    - RODRIGUES_FORM / TABLE_LOOKUP / MAT_ENTRY / CHECK
    - Z: exact exponential matrix
    """

    VARIANTS = ["so2", "so3"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        theta, angle = random_angle()
        cos_text, sin_text = TRIG[angle]
        if variant == "so2":
            problem, steps, answer = self._generate_so2(theta, angle,
                                                        cos_text, sin_text)
        else:
            axis = random.choice(["x", "y", "z"])
            problem, steps, answer = self._generate_so3(axis, theta, angle,
                                                        cos_text, sin_text)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"lie_exponential_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_so2(self, theta, angle, cos_text, sin_text):
        J = [[0, -1], [1, 0]]
        result = so2_matrix(cos_text, sin_text)
        expr = [["cos(theta)", "-sin(theta)"],
                ["sin(theta)", "cos(theta)"]]
        steps = [
            step("LIE_EXP_SETUP", "SO2", f"theta={theta} deg",
                 f"J={mat(J)}", "goal=e^(theta J)"),
            step("MOD_REDUCE", theta, "mod 360", angle),
            step("MATRIX_POWER", "J^2", "-I"),
            step("SERIES_GROUP", "even powers", "cos(theta)I"),
            step("SERIES_GROUP", "odd powers", "sin(theta)J"),
            step("LIE_EXP_FORM", "e^(theta J)",
                 "cos(theta)I + sin(theta)J"),
            step("TABLE_LOOKUP", f"cos {angle} deg", cos_text),
            step("TABLE_LOOKUP", f"sin {angle} deg", sin_text),
        ]
        for i in range(2):
            for j in range(2):
                steps.append(step("MAT_ENTRY", f"({i + 1},{j + 1})",
                                  expr[i][j], result[i][j]))
        steps.extend([
            step("CHECK", "R^T R", "I", "orthogonal"),
            step("CHECK", "det R", "1", "proper rotation"),
        ])
        answer = f"e^(theta J)={matrix_text(result)}"
        problem = (
            f"Exponentiate the so(2) element theta={theta} deg with "
            f"J={mat(J)}."
        )
        return problem, steps, answer

    def _generate_so3(self, axis, theta, angle, cos_text, sin_text):
        K = SO3_GENERATORS[axis]
        K2 = SO3_SQUARES[axis]
        result = so3_matrix(axis, cos_text, sin_text)
        expr = so3_expr_matrix(axis)
        steps = [
            step("LIE_EXP_SETUP", "SO3", f"axis={axis}",
                 f"theta={theta} deg", f"K={mat(K)}"),
            step("MOD_REDUCE", theta, "mod 360", angle),
            step("MATRIX_POWER", "K^2", mat(K2)),
            step("RODRIGUES_FORM", "e^(theta K)",
                 "I + sin(theta)K + (1-cos(theta))K^2"),
            step("TABLE_LOOKUP", f"cos {angle} deg", cos_text),
            step("TABLE_LOOKUP", f"sin {angle} deg", sin_text),
        ]
        for i in range(3):
            for j in range(3):
                steps.append(step("MAT_ENTRY", f"({i + 1},{j + 1})",
                                  expr[i][j], result[i][j]))
        steps.extend([
            step("CHECK", "R^T R", "I", "orthogonal"),
            step("CHECK", "det R", "1", "proper rotation"),
        ])
        answer = f"e^(theta K_{axis})={matrix_text(result)}"
        problem = (
            f"Exponentiate the so(3) element theta={theta} deg about the "
            f"{axis}-axis with K={mat(K)}."
        )
        return problem, steps, answer
