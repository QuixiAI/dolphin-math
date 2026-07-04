import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def point_text(point):
    return f"({fraction_text(point[0])},{fraction_text(point[1])})"


def points_text(points):
    return "[" + ", ".join(point_text(point) for point in points) + "]"


def vector_text(values):
    return "(" + ",".join(fraction_text(value) for value in values) + ")"


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(fraction_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def add_running_steps(steps, values):
    running = Fraction(0)
    for value in values:
        new_running = running + value
        steps.append(step("A", fraction_text(running), fraction_text(value),
                          fraction_text(new_running)))
        running = new_running
    return running


class PCAGenerator(ProblemGenerator):
    """
    2D PCA from a small dataset: mean, covariance, eigendecomposition, projection.

    The generated datasets are shifted axis pairs, so the population covariance
    is diagonal after centering and the principal component is one coordinate
    axis. This keeps every PCA step exact.

    Op-codes used:
    - PCA_SETUP / CENTER / COV_ENTRY / EIGENVALUES / PC_VECTOR / PROJECT
    - CHECK (established): compare eigenvalues
    - A / S / M / D / E (established/shared): means, covariance entries,
      and projection dot products
    - Z: covariance, principal component, and projection scores
    """

    def generate(self) -> dict:
        mean_x = random.randint(-5, 5)
        mean_y = random.randint(-5, 5)
        spread_major = random.randint(3, 8)
        spread_minor = random.randint(1, spread_major - 1)
        major_axis = random.choice(["x", "y"])
        if major_axis == "x":
            spread_x, spread_y = spread_major, spread_minor
        else:
            spread_x, spread_y = spread_minor, spread_major
        points = [
            (mean_x + spread_x, mean_y),
            (mean_x - spread_x, mean_y),
            (mean_x, mean_y + spread_y),
            (mean_x, mean_y - spread_y),
        ]
        n = len(points)

        steps = [
            step("PCA_SETUP", f"points={points_text(points)}",
                 "population covariance"),
        ]
        sum_x = add_running_steps(steps, [point[0] for point in points])
        mean_x_value = Fraction(sum_x, n)
        steps.append(step("D", fraction_text(sum_x), n,
                          fraction_text(mean_x_value)))
        sum_y = add_running_steps(steps, [point[1] for point in points])
        mean_y_value = Fraction(sum_y, n)
        steps.append(step("D", fraction_text(sum_y), n,
                          fraction_text(mean_y_value)))

        centered = []
        for index, point in enumerate(points, start=1):
            cx = Fraction(point[0]) - mean_x_value
            cy = Fraction(point[1]) - mean_y_value
            centered.append((cx, cy))
            steps.extend([
                step("S", point[0], fraction_text(mean_x_value),
                     fraction_text(cx)),
                step("S", point[1], fraction_text(mean_y_value),
                     fraction_text(cy)),
                step("CENTER", f"P{index}", point_text((cx, cy))),
            ])

        cov_entries = []
        for name, selector in (
            ("xx", lambda p: p[0] * p[0]),
            ("xy", lambda p: p[0] * p[1]),
            ("yy", lambda p: p[1] * p[1]),
        ):
            products = []
            for cx, cy in centered:
                if name == "xx":
                    value = cx ** 2
                    steps.append(step("E", fraction_text(cx), 2,
                                      fraction_text(value)))
                elif name == "yy":
                    value = cy ** 2
                    steps.append(step("E", fraction_text(cy), 2,
                                      fraction_text(value)))
                else:
                    value = cx * cy
                    steps.append(step("M", fraction_text(cx), fraction_text(cy),
                                      fraction_text(value)))
                products.append(value)
            total = add_running_steps(steps, products)
            entry = total / n
            steps.append(step("D", fraction_text(total), n,
                              fraction_text(entry)))
            steps.append(step("COV_ENTRY", name, fraction_text(entry)))
            cov_entries.append(entry)

        cov_xx, cov_xy, cov_yy = cov_entries
        covariance = [[cov_xx, cov_xy], [cov_xy, cov_yy]]
        lambda_x = cov_xx
        lambda_y = cov_yy
        if lambda_x >= lambda_y:
            pc = (Fraction(1), Fraction(0))
            pc_name = "e1"
            relation = ">="
        else:
            pc = (Fraction(0), Fraction(1))
            pc_name = "e2"
            relation = "<"
        steps.extend([
            step("EIGENVALUES", "diagonal covariance",
                 f"lambda_x={fraction_text(lambda_x)}, "
                 f"lambda_y={fraction_text(lambda_y)}"),
            step("CHECK", "lambda_x vs lambda_y",
                 f"{fraction_text(lambda_x)} {relation} {fraction_text(lambda_y)}",
                 f"pc={pc_name}"),
            step("PC_VECTOR", pc_name, vector_text(pc)),
        ])

        scores = []
        for index, (cx, cy) in enumerate(centered, start=1):
            term_x = cx * pc[0]
            term_y = cy * pc[1]
            score_value = term_x + term_y
            steps.extend([
                step("M", fraction_text(cx), fraction_text(pc[0]),
                     fraction_text(term_x)),
                step("M", fraction_text(cy), fraction_text(pc[1]),
                     fraction_text(term_y)),
                step("A", fraction_text(term_x), fraction_text(term_y),
                     fraction_text(score_value)),
                step("PROJECT", f"P{index}", fraction_text(score_value)),
            ])
            scores.append(score_value)

        answer = (
            f"cov={matrix_text(covariance)}; pc={vector_text(pc)}; "
            f"scores={','.join(fraction_text(score) for score in scores)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"For points {points_text(points)}, use population covariance "
            "(divide by n) to compute 2D PCA and project each centered point "
            "onto the principal component."
        )
        return dict(
            problem_id=jid(),
            operation="pca_2d_projection",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
