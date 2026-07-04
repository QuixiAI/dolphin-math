import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def vector_text(values):
    return "(" + ",".join(fraction_text(value) for value in values) + ")"


class LayerNormGenerator(ProblemGenerator):
    """
    LayerNorm by hand for a two-element vector with exact standard deviation.

    Vectors are generated as (m-a, m+a), so the population mean is m, variance
    is a^2, and std is a. The normalized vector is exactly (-1, 1).

    Op-codes used:
    - LAYERNORM_SETUP / MEAN / VARIANCE / STD / NORMALIZE / SCALE_SHIFT
    - A / S / D / E / ROOT / M (established/shared): full LayerNorm arithmetic
    - Z: mean, variance, normalized vector, output vector
    """

    def generate(self) -> dict:
        mean_value = random.randint(-10, 10)
        spread = random.randint(1, 12)
        x = (mean_value - spread, mean_value + spread)
        gamma = (random.randint(1, 4), random.randint(1, 4))
        beta = (random.randint(-5, 5), random.randint(-5, 5))

        total = x[0] + x[1]
        mean = Fraction(total, 2)
        devs = [Fraction(value) - mean for value in x]
        squares = [dev * dev for dev in devs]
        square_sum = squares[0] + squares[1]
        variance = square_sum / 2
        std = spread
        normalized = [dev / std for dev in devs]
        scaled = [gamma[i] * normalized[i] for i in range(2)]
        output = [scaled[i] + beta[i] for i in range(2)]

        steps = [
            step("LAYERNORM_SETUP", f"x={vector_text(x)}",
                 f"gamma={vector_text(gamma)}", f"beta={vector_text(beta)}"),
            step("A", x[0], x[1], total),
            step("D", total, 2, fraction_text(mean)),
            step("MEAN", fraction_text(mean)),
        ]
        for index, value in enumerate(x):
            steps.extend([
                step("S", value, fraction_text(mean), fraction_text(devs[index])),
                step("E", fraction_text(devs[index]), 2,
                     fraction_text(squares[index])),
            ])
        steps.extend([
            step("A", fraction_text(squares[0]), fraction_text(squares[1]),
                 fraction_text(square_sum)),
            step("D", fraction_text(square_sum), 2, fraction_text(variance)),
            step("VARIANCE", fraction_text(variance)),
            step("ROOT", f"sqrt({fraction_text(variance)})", std),
            step("STD", std),
        ])
        for index in range(2):
            steps.extend([
                step("D", fraction_text(devs[index]), std,
                     fraction_text(normalized[index])),
                step("NORMALIZE", index + 1, fraction_text(normalized[index])),
                step("M", gamma[index], fraction_text(normalized[index]),
                     fraction_text(scaled[index])),
                step("A", fraction_text(scaled[index]), beta[index],
                     fraction_text(output[index])),
                step("SCALE_SHIFT", index + 1, fraction_text(output[index])),
            ])
        answer = (
            f"mean={fraction_text(mean)}; variance={fraction_text(variance)}; "
            f"normalized={vector_text(normalized)}; y={vector_text(output)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Apply LayerNorm to x={vector_text(x)} with gamma={vector_text(gamma)} "
            f"and beta={vector_text(beta)}. Use population variance and "
            "epsilon=0."
        )
        return dict(
            problem_id=jid(),
            operation="layer_norm_exact_2d",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
