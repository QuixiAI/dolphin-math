import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.geometric_mean_generator import sqrt_txt


def wrap(n):
    return f"({n})" if n < 0 else str(n)


class DistanceFormulaGenerator(ProblemGenerator):
    """
    Distance between two points: state the formula, compute both
    differences, square them (negatives parenthesized), add, and
    simplify the root. Pythagorean pairs give integers; other pairs
    give simplified radicals.

    Op-codes used:
    - DIST_FORMULA: d = √((x2 - x1)^2 + (y2 - y1)^2)
    - S / E / A: the differences, squares, and sum (established)
    - ROOT_SIMPLIFY: for radical answers (established)
    - Z: 'd = 5' or 'd = 2√13'
    """

    def generate(self) -> dict:
        while True:
            x1, y1 = random.randint(-9, 9), random.randint(-9, 9)
            x2, y2 = random.randint(-9, 9), random.randint(-9, 9)
            if (x1, y1) != (x2, y2) and x1 != x2 and y1 != y2:
                break
        dx, dy = x2 - x1, y2 - y1
        total = dx * dx + dy * dy
        val = sqrt_txt(total)

        steps = [
            step("DIST_FORMULA", "d = √((x2 - x1)^2 + (y2 - y1)^2)"),
            step("S", x2, x1, dx),
            step("S", y2, y1, dy),
            step("E", wrap(dx), 2, dx * dx),
            step("E", wrap(dy), 2, dy * dy),
            step("A", dx * dx, dy * dy, total),
        ]
        if "√" in val:
            steps.append(step("ROOT_SIMPLIFY", f"√{total} = {val}"))
        else:
            steps.append(step("E", val, 2, total))
        answer = f"d = {val}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="distance_formula",
            problem=(f"Find the distance between ({x1}, {y1}) and "
                     f"({x2}, {y2})."),
            steps=steps,
            final_answer=answer,
        )
