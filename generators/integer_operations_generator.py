import random
from base_generator import ProblemGenerator
from helpers import step, jid


class IntegerOperationsGenerator(ProblemGenerator):
    """
    Generates integer operation problems involving positive and negative numbers.
    Covers addition, subtraction, multiplication, and division with explicit
    sign rule steps.

    Op-codes used:
    - INT_SIGN_RULE: Explain the sign rule being applied (rule_name, explanation)
    - INT_ABS: Take absolute value (number, abs_value)
    - INT_OP: Perform operation on absolute values (op, val1, val2, result)
    - INT_APPLY_SIGN: Apply determined sign to result (unsigned_result, sign, final_result)
    - INT_REWRITE: Rewrite expression (e.g., subtraction as addition) (original, rewritten)
    - Z: Final answer
    """

    def __init__(self, operation: str = None):
        """
        Initialize with optional operation type.

        Args:
            operation: One of '+', '-', '*', '/', or None for random.
        """
        if operation is not None and operation not in ['+', '-', '*', '/']:
            raise ValueError(f"Invalid operation: {operation}. Must be +, -, *, /, or None.")
        self.operation = operation

    def generate(self) -> dict:
        op = self.operation or random.choice(['+', '-', '*', '/'])

        if op == '+':
            return self._generate_addition()
        elif op == '-':
            return self._generate_subtraction()
        elif op == '*':
            return self._generate_multiplication()
        else:
            return self._generate_division()

    def _generate_addition(self) -> dict:
        """Generate integer addition problem with sign rules."""
        # Generate two integers, at least one negative
        a = random.randint(-20, 20)
        b = random.randint(-20, 20)

        # Ensure at least one is negative for interesting problems
        if a >= 0 and b >= 0:
            if random.choice([True, False]):
                a = -a
            else:
                b = -b

        steps = []
        result = a + b

        # Format the problem
        b_str = f"+ ({b})" if b < 0 else f"+ {b}"
        problem = f"({a}) {b_str}" if a < 0 else f"{a} {b_str}"

        if a >= 0 and b >= 0:
            # Both positive - simple addition
            steps.append(step("INT_SIGN_RULE", "same_signs", "Both positive: add and keep positive"))
            steps.append(step("INT_OP", "+", a, b, result))
        elif a < 0 and b < 0:
            # Both negative - add absolutes, result is negative
            steps.append(step("INT_SIGN_RULE", "same_signs", "Both negative: add absolute values, result is negative"))
            abs_a, abs_b = abs(a), abs(b)
            steps.append(step("INT_ABS", a, abs_a))
            steps.append(step("INT_ABS", b, abs_b))
            unsigned_sum = abs_a + abs_b
            steps.append(step("INT_OP", "+", abs_a, abs_b, unsigned_sum))
            steps.append(step("INT_APPLY_SIGN", unsigned_sum, "negative", result))
        else:
            # Different signs - subtract smaller absolute from larger
            steps.append(step("INT_SIGN_RULE", "different_signs", "Different signs: subtract absolute values, take sign of larger absolute value"))
            abs_a, abs_b = abs(a), abs(b)
            steps.append(step("INT_ABS", a, abs_a))
            steps.append(step("INT_ABS", b, abs_b))

            if abs_a > abs_b:
                diff = abs_a - abs_b
                steps.append(step("INT_OP", "-", abs_a, abs_b, diff))
                sign = "negative" if a < 0 else "positive"
                steps.append(step("INT_APPLY_SIGN", diff, sign, result))
            elif abs_b > abs_a:
                diff = abs_b - abs_a
                steps.append(step("INT_OP", "-", abs_b, abs_a, diff))
                sign = "negative" if b < 0 else "positive"
                steps.append(step("INT_APPLY_SIGN", diff, sign, result))
            else:
                # Equal absolutes, result is 0
                steps.append(step("INT_OP", "-", abs_a, abs_b, 0))

        steps.append(step("Z", result))

        return dict(
            problem_id=jid(),
            operation="integer_addition",
            problem=f"Calculate: {problem}",
            steps=steps,
            final_answer=str(result),
        )

    def _generate_subtraction(self) -> dict:
        """Generate integer subtraction problem - rewrite as addition."""
        a = random.randint(-20, 20)
        b = random.randint(-20, 20)

        # Ensure at least one is negative or result is negative
        if a >= 0 and b >= 0 and a >= b:
            if random.choice([True, False]):
                a = -a
            else:
                b = -b

        steps = []
        result = a - b

        # Format the problem
        b_str = f"- ({b})" if b < 0 else f"- {b}"
        problem = f"({a}) {b_str}" if a < 0 else f"{a} {b_str}"

        # Rewrite subtraction as adding the opposite
        opposite_b = -b
        steps.append(step("INT_REWRITE", f"{a} - ({b})" if b < 0 else f"{a} - {b}",
                         f"{a} + ({opposite_b})" if opposite_b < 0 else f"{a} + {opposite_b}"))
        steps.append(step("INT_SIGN_RULE", "subtract_rule", "Subtracting is adding the opposite"))

        # Now it's an addition problem
        if (a >= 0 and opposite_b >= 0) or (a < 0 and opposite_b < 0):
            # Same signs
            if a < 0 and opposite_b < 0:
                steps.append(step("INT_SIGN_RULE", "same_signs", "Both negative: add absolute values, result is negative"))
                abs_a, abs_ob = abs(a), abs(opposite_b)
                steps.append(step("INT_ABS", a, abs_a))
                steps.append(step("INT_ABS", opposite_b, abs_ob))
                unsigned_sum = abs_a + abs_ob
                steps.append(step("INT_OP", "+", abs_a, abs_ob, unsigned_sum))
                steps.append(step("INT_APPLY_SIGN", unsigned_sum, "negative", result))
            else:
                steps.append(step("INT_SIGN_RULE", "same_signs", "Both positive: add and keep positive"))
                steps.append(step("INT_OP", "+", a, opposite_b, result))
        else:
            # Different signs
            steps.append(step("INT_SIGN_RULE", "different_signs", "Different signs: subtract absolute values, take sign of larger absolute value"))
            abs_a, abs_ob = abs(a), abs(opposite_b)
            steps.append(step("INT_ABS", a, abs_a))
            steps.append(step("INT_ABS", opposite_b, abs_ob))

            if abs_a > abs_ob:
                diff = abs_a - abs_ob
                steps.append(step("INT_OP", "-", abs_a, abs_ob, diff))
                sign = "negative" if a < 0 else "positive"
                steps.append(step("INT_APPLY_SIGN", diff, sign, result))
            elif abs_ob > abs_a:
                diff = abs_ob - abs_a
                steps.append(step("INT_OP", "-", abs_ob, abs_a, diff))
                sign = "negative" if opposite_b < 0 else "positive"
                steps.append(step("INT_APPLY_SIGN", diff, sign, result))
            else:
                steps.append(step("INT_OP", "-", abs_a, abs_ob, 0))

        steps.append(step("Z", result))

        return dict(
            problem_id=jid(),
            operation="integer_subtraction",
            problem=f"Calculate: {problem}",
            steps=steps,
            final_answer=str(result),
        )

    def _generate_multiplication(self) -> dict:
        """Generate integer multiplication problem with sign rules."""
        a = random.randint(-12, 12)
        b = random.randint(-12, 12)

        # Avoid trivial cases
        if a == 0:
            a = random.choice([-1, 1]) * random.randint(1, 12)
        if b == 0:
            b = random.choice([-1, 1]) * random.randint(1, 12)

        # Ensure at least one negative
        if a > 0 and b > 0:
            if random.choice([True, False]):
                a = -a
            else:
                b = -b

        steps = []
        result = a * b

        # Format the problem
        problem = f"({a}) × ({b})"

        abs_a, abs_b = abs(a), abs(b)

        # Determine sign rule
        if (a > 0 and b > 0) or (a < 0 and b < 0):
            steps.append(step("INT_SIGN_RULE", "mult_same_signs", "Same signs: positive × positive = positive, or negative × negative = positive"))
            result_sign = "positive"
        else:
            steps.append(step("INT_SIGN_RULE", "mult_different_signs", "Different signs: positive × negative = negative"))
            result_sign = "negative"

        steps.append(step("INT_ABS", a, abs_a))
        steps.append(step("INT_ABS", b, abs_b))

        unsigned_product = abs_a * abs_b
        steps.append(step("INT_OP", "×", abs_a, abs_b, unsigned_product))
        steps.append(step("INT_APPLY_SIGN", unsigned_product, result_sign, result))

        steps.append(step("Z", result))

        return dict(
            problem_id=jid(),
            operation="integer_multiplication",
            problem=f"Calculate: {problem}",
            steps=steps,
            final_answer=str(result),
        )

    def _generate_division(self) -> dict:
        """Generate integer division problem with sign rules (exact division only)."""
        # Generate divisor and quotient, then compute dividend
        divisor = random.randint(2, 12)
        quotient = random.randint(1, 12)

        # Apply signs
        if random.choice([True, False]):
            divisor = -divisor
        if random.choice([True, False]):
            quotient = -quotient

        dividend = divisor * quotient  # Ensures exact division

        steps = []
        result = quotient

        # Format the problem
        problem = f"({dividend}) ÷ ({divisor})"

        abs_dividend, abs_divisor = abs(dividend), abs(divisor)

        # Determine sign rule
        if (dividend > 0 and divisor > 0) or (dividend < 0 and divisor < 0):
            steps.append(step("INT_SIGN_RULE", "div_same_signs", "Same signs: positive ÷ positive = positive, or negative ÷ negative = positive"))
            result_sign = "positive"
        else:
            steps.append(step("INT_SIGN_RULE", "div_different_signs", "Different signs: result is negative"))
            result_sign = "negative"

        steps.append(step("INT_ABS", dividend, abs_dividend))
        steps.append(step("INT_ABS", divisor, abs_divisor))

        unsigned_quotient = abs_dividend // abs_divisor
        steps.append(step("INT_OP", "÷", abs_dividend, abs_divisor, unsigned_quotient))
        steps.append(step("INT_APPLY_SIGN", unsigned_quotient, result_sign, result))

        steps.append(step("Z", result))

        return dict(
            problem_id=jid(),
            operation="integer_division",
            problem=f"Calculate: {problem}",
            steps=steps,
            final_answer=str(result),
        )
