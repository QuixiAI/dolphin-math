import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(fraction_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


class AttentionGenerator(ProblemGenerator):
    """
    Scaled dot-product attention by hand for 2-3 tokens and d=2.

    Q and K are zero matrices, so QK^T/sqrt(2) is the zero matrix. Softmax is
    therefore exactly uniform in every row, and the attention output is the
    exact average of the V rows.

    Op-codes used:
    - ATTN_SETUP / ATTN_SCORE / SOFTMAX_EXP / SOFTMAX_WEIGHT / ATTN_OUTPUT
    - M / A / D (established/shared): dot products, softmax weights, V sums
    - Z: exact attention output matrix
    """

    def generate(self) -> dict:
        tokens = random.choice([2, 3])
        q = [[0, 0] for _ in range(tokens)]
        k = [[0, 0] for _ in range(tokens)]
        v = [
            [random.randint(-9, 9), random.randint(-9, 9)]
            for _ in range(tokens)
        ]
        steps = [
            step("ATTN_SETUP", f"tokens={tokens},d=2",
                 f"Q={matrix_text(q)}", f"K={matrix_text(k)}"),
            step("ATTN_SETUP", f"V={matrix_text(v)}"),
        ]
        scores = []
        for row in range(tokens):
            score_row = []
            for col in range(tokens):
                prod1 = q[row][0] * k[col][0]
                prod2 = q[row][1] * k[col][1]
                dot = prod1 + prod2
                steps.extend([
                    step("M", q[row][0], k[col][0], prod1),
                    step("M", q[row][1], k[col][1], prod2),
                    step("A", prod1, prod2, dot),
                    step("ATTN_SCORE", f"{row + 1},{col + 1}", dot),
                ])
                score_row.append(dot)
            scores.append(score_row)

        weight = Fraction(1, tokens)
        outputs = []
        for row in range(tokens):
            exp_sum = 0
            for col in range(tokens):
                steps.append(step("SOFTMAX_EXP", f"{row + 1},{col + 1}", 1))
                new_sum = exp_sum + 1
                steps.append(step("A", exp_sum, 1, new_sum))
                exp_sum = new_sum
            weights = []
            for col in range(tokens):
                steps.append(step("D", 1, exp_sum, fraction_text(weight)))
                steps.append(step("SOFTMAX_WEIGHT", f"{row + 1},{col + 1}",
                                  fraction_text(weight)))
                weights.append(weight)
            output_row = []
            for dim in range(2):
                running = Fraction(0)
                for col in range(tokens):
                    term = weights[col] * v[col][dim]
                    steps.append(step("M", fraction_text(weights[col]),
                                      v[col][dim], fraction_text(term)))
                    new_running = running + term
                    steps.append(step("A", fraction_text(running),
                                      fraction_text(term),
                                      fraction_text(new_running)))
                    running = new_running
                output_row.append(running)
            steps.append(step("ATTN_OUTPUT", row + 1, matrix_text([output_row])))
            outputs.append(output_row)

        answer = f"attention={matrix_text(outputs)}"
        steps.append(step("Z", answer))
        problem = (
            f"Compute scaled dot-product attention for Q={matrix_text(q)}, "
            f"K={matrix_text(k)}, V={matrix_text(v)} with d=2. Use softmax "
            "over each row of QK^T/sqrt(2)."
        )
        return dict(
            problem_id=jid(),
            operation="attention_scaled_dot_product_uniform",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
