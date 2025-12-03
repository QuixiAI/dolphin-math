import random
from base_generator import ProblemGenerator
from helpers import step, jid


class MultiDigitSubtractionGenerator(ProblemGenerator):
    """Generates standard column-form multi-digit subtraction with borrowing."""

    def generate(self) -> dict:
        operation = "multi_digit_subtraction"
        # Keep numbers at least two digits; ensure minuend >= subtrahend
        num1 = random.randint(10, 99999)
        num2 = random.randint(10, num1)  # guarantees non-negative result

        s1, s2 = str(num1), str(num2)
        max_len = max(len(s1), len(s2))
        s1, s2 = s1.zfill(max_len), s2.zfill(max_len)

        problem = f"{int(s1)} - {int(s2)}"
        borrow = 0
        steps = []
        steps.append(step("INT_ALIGN", s1, s2))

        for idx in range(max_len - 1, -1, -1):
            col_name = f"col_{max_len - idx}"  # 1-based from rightmost
            d1 = int(s1[idx])
            d2 = int(s2[idx])

            borrow_in = borrow
            d1_eff = d1 - borrow_in
            borrow_out = 0

            if d1_eff < d2:
                d1_eff += 10
                borrow_out = 1
                steps.append(step("BORROW", col_name, "from_left", 1))

            col_diff = d1_eff - d2
            sub_details = f"{d1}-{d2}-borrow{borrow_in}"
            sub_result = f"->{col_diff} (borrow_out {borrow_out})"
            steps.append(step("SUB_COL", col_name, sub_details, sub_result))

            borrow = borrow_out

        final_answer = num1 - num2
        steps.append(step("Z", str(final_answer)))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=str(final_answer),
        )
