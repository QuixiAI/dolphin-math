import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def vector_text(values):
    return "[" + ",".join(fraction_text(value) for value in values) + "]"


def random_vector(size, lo=-6, hi=6):
    return [random.randint(lo, hi) for _ in range(size)]


class IndexRaisingGenerator(ProblemGenerator):
    """
    Raise and lower vector/covector components with diagonal metrics.

    Variants:
    - lower: v_i = g_ii v^i.
    - raise: w^i = g^ii w_i.

    Op-codes used:
    - INDEX_METRIC / TENSOR_ENTRY
    - M (established/shared): componentwise exact scaling
    - Z: raised or lowered components
    """

    VARIANTS = ["lower", "raise"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "lower":
            problem, steps, answer = self._generate_lower()
        else:
            problem, steps, answer = self._generate_raise()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"index_raising_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_lower(self):
        metric_name, diag = random.choice([
            ("Minkowski", [-1, 1, 1, 1]),
            ("sphere", [1, random.randint(2, 6) ** 2]),
        ])
        vector = random_vector(len(diag))
        lowered = [Fraction(g) * v for g, v in zip(diag, vector)]
        steps = [
            step("INDEX_METRIC", "lower", metric_name,
                 f"g_ii={vector_text(diag)}"),
        ]
        for idx, (g, value, result) in enumerate(zip(diag, vector, lowered),
                                                start=1):
            steps.extend([
                step("M", fraction_text(g), value, fraction_text(result)),
                step("TENSOR_ENTRY", f"v_{idx}", fraction_text(result)),
            ])
        answer = f"v_i = {vector_text(lowered)}"
        problem = (
            f"Lower v^i={vector_text(vector)} using the diagonal "
            f"{metric_name} metric g_ii={vector_text(diag)}."
        )
        return problem, steps, answer

    def _generate_raise(self):
        metric_name, inverse = random.choice([
            ("Minkowski", [-1, 1, 1, 1]),
            ("sphere", [Fraction(1), Fraction(1, random.randint(2, 6) ** 2)]),
        ])
        covector = random_vector(len(inverse))
        raised = [Fraction(g) * value for g, value in zip(inverse, covector)]
        steps = [
            step("INDEX_METRIC", "raise", metric_name,
                 f"g^ii={vector_text(inverse)}"),
        ]
        for idx, (g, value, result) in enumerate(zip(inverse, covector, raised),
                                                start=1):
            steps.extend([
                step("M", fraction_text(g), value, fraction_text(result)),
                step("TENSOR_ENTRY", f"w^{idx}", fraction_text(result)),
            ])
        answer = f"w^i = {vector_text(raised)}"
        problem = (
            f"Raise w_i={vector_text(covector)} using the diagonal "
            f"{metric_name} inverse metric g^ii={vector_text(inverse)}."
        )
        return problem, steps, answer
