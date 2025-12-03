import random
from base_generator import ProblemGenerator
from helpers import step, jid


class MultiDigitMultiplicationGenerator(ProblemGenerator):
    """Generates standard column-form multi-digit integer multiplication."""

    def generate(self) -> dict:
        operation = "multi_digit_multiplication"
        # Choose 2–5 digit numbers to keep partials manageable
        top = random.randint(10, 99999)
        bottom = random.randint(10, 99999)

        # Place the larger number on top for more familiar layout
        if bottom > top:
            top, bottom = bottom, top

        top_str = str(top)
        bottom_str = str(bottom)
        problem = f"{top_str} * {bottom_str}"

        steps = []
        steps.append(step("MUL_SETUP", top_str, bottom_str))

        partials = []
        for idx, digit_char in enumerate(reversed(bottom_str)):
            digit = int(digit_char)
            partial = digit * top
            shifted = partial * (10 ** idx)
            steps.append(step("MUL_PARTIAL", digit, top_str, str(shifted)))
            partials.append(shifted)

        total = sum(partials)
        partial_expr = " + ".join(str(p) for p in partials)
        steps.append(step("ADD_PARTIALS", partial_expr, str(total)))
        steps.append(step("Z", str(total)))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=str(total),
        )
