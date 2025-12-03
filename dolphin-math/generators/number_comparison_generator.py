import random
from base_generator import ProblemGenerator
from helpers import step, jid


class NumberComparisonGenerator(ProblemGenerator):
    """Compares whole numbers or decimals by place value."""

    def generate(self) -> dict:
        mode = random.choice(["whole", "decimal"])
        if mode == "whole":
            a = random.randint(10, 99999)
            b = random.randint(10, 99999)
        else:
            a = round(random.uniform(0.1, 999.9), 2)
            b = round(random.uniform(0.1, 999.9), 2)

        # Avoid equal too often
        if a == b:
            b += 1

        a_str, b_str = str(a), str(b)
        steps = []
        # Normalize with leading zeros for whole comparison of length
        a_pad = a_str
        b_pad = b_str
        if mode == "whole":
            max_len = max(len(a_str), len(b_str))
            a_pad = a_str.zfill(max_len)
            b_pad = b_str.zfill(max_len)

        steps.append(step("ALIGN_NUM", a_pad, b_pad))
        relation = ">" if a > b else "<"
        if a == b:
            relation = "="
        steps.append(step("CMP_NUM", a, b, relation))
        steps.append(step("Z", f"{a} {relation} {b}"))

        return dict(
            problem_id=jid(),
            operation="number_compare",
            problem=f"Compare: {a} ? {b}",
            steps=steps,
            final_answer=f"{a} {relation} {b}",
        )
