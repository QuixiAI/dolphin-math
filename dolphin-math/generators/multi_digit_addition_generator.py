import random
from base_generator import ProblemGenerator
from helpers import step, jid


class MultiDigitAdditionGenerator(ProblemGenerator):
    """Generates standard column-form multi-digit addition with carries."""

    def generate(self) -> dict:
        operation = "multi_digit_addition"
        # Keep numbers at least two digits to show meaningful carrying cases
        num1 = random.randint(10, 99999)
        num2 = random.randint(10, 99999)

        s1, s2 = str(num1), str(num2)
        max_len = max(len(s1), len(s2))
        s1, s2 = s1.zfill(max_len), s2.zfill(max_len)

        problem = f"{int(s1)} + {int(s2)}"
        carry = 0
        steps = []
        steps.append(step("INT_ALIGN", s1, s2))

        # Right-to-left column addition
        for idx in range(max_len - 1, -1, -1):
            col_name = f"col_{max_len - idx}"  # 1-based from rightmost
            d1 = int(s1[idx])
            d2 = int(s2[idx])
            col_sum = d1 + d2 + carry
            result_digit = col_sum % 10
            new_carry = col_sum // 10

            add_details = f"{d1}+{d2}+{carry}"
            add_result = f"->{result_digit} (carry {new_carry})"
            steps.append(step("ADD_COL", col_name, add_details, add_result))
            carry = new_carry

        if carry:
            steps.append(step("CARRY_FINAL", carry))

        final_answer = num1 + num2
        steps.append(step("Z", str(final_answer)))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=str(final_answer),
        )
