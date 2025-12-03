import random
from base_generator import ProblemGenerator
from helpers import step, jid


class OneStepInequalityGenerator(ProblemGenerator):
    """
    Generates one-step linear inequalities.

    Problem types:
    - x + a < b  (solve by subtracting)
    - x - a > b  (solve by adding)
    - ax < b     (solve by dividing) - note: reverse if a is negative
    - x/a ≥ b    (solve by multiplying)

    Op-codes used:
    - INEQ_SETUP: Set up the inequality (inequality_string)
    - INEQ_OP_BOTH: Apply operation to both sides (operation, value, new_left, new_right)
    - INEQ_FLIP: Note when inequality flips (reason)
    - INEQ_RESULT: Show the result (variable, relation, value)
    - Z: Final answer
    """

    RELATIONS = ['<', '>', '≤', '≥']

    def __init__(self, operation: str = None, include_negative_coefficient: bool = True):
        """
        Initialize generator.

        Args:
            operation: One of '+', '-', '*', '/' or None for random
            include_negative_coefficient: Whether to include problems that require flipping
        """
        if operation is not None and operation not in ['+', '-', '*', '/']:
            raise ValueError(f"Invalid operation: {operation}. Must be +, -, *, /, or None.")
        self.operation = operation
        self.include_negative_coefficient = include_negative_coefficient

    def generate(self) -> dict:
        """Generate a one-step inequality problem."""
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
        """Generate x + a < b (or other relation) inequality."""
        relation = random.choice(self.RELATIONS)
        a = random.randint(1, 15)
        b = random.randint(-10, 20)

        # The solution is x < (b - a) or similar
        boundary = b - a

        equation = f"x + {a} {relation} {b}"
        steps = []

        # Step 1: Set up inequality
        steps.append(step("INEQ_SETUP", equation))

        # Step 2: Subtract a from both sides
        steps.append(step("INEQ_OP_BOTH", "subtract", a, "x", boundary))

        # Step 3: Result
        steps.append(step("INEQ_RESULT", "x", relation, boundary))

        # Final answer
        answer = f"x {relation} {boundary}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="one_step_inequality",
            problem=f"Solve the inequality: {equation}",
            steps=steps,
            final_answer=answer,
        )

    def _generate_subtraction(self) -> dict:
        """Generate x - a > b (or other relation) inequality."""
        relation = random.choice(self.RELATIONS)
        a = random.randint(1, 15)
        b = random.randint(-10, 20)

        # The solution is x > (b + a) or similar
        boundary = b + a

        equation = f"x - {a} {relation} {b}"
        steps = []

        # Step 1: Set up inequality
        steps.append(step("INEQ_SETUP", equation))

        # Step 2: Add a to both sides
        steps.append(step("INEQ_OP_BOTH", "add", a, "x", boundary))

        # Step 3: Result
        steps.append(step("INEQ_RESULT", "x", relation, boundary))

        # Final answer
        answer = f"x {relation} {boundary}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="one_step_inequality",
            problem=f"Solve the inequality: {equation}",
            steps=steps,
            final_answer=answer,
        )

    def _generate_multiplication(self) -> dict:
        """Generate ax < b inequality, possibly with negative coefficient."""
        relation = random.choice(self.RELATIONS)

        # Decide whether to use negative coefficient
        if self.include_negative_coefficient and random.choice([True, False]):
            a = random.randint(-10, -2)
        else:
            a = random.randint(2, 10)

        # Generate b such that b/a is an integer
        quotient = random.randint(-10, 10)
        if quotient == 0:
            quotient = random.choice([-1, 1]) * random.randint(1, 10)
        b = a * quotient

        boundary = quotient
        flipped = a < 0

        # Format equation
        if a < 0:
            equation = f"{a}x {relation} {b}"
        else:
            equation = f"{a}x {relation} {b}"

        steps = []

        # Step 1: Set up inequality
        steps.append(step("INEQ_SETUP", equation))

        # Step 2: Divide both sides by a
        steps.append(step("INEQ_OP_BOTH", "divide", a, "x", boundary))

        # Step 3: Note flip if necessary
        if flipped:
            steps.append(step("INEQ_FLIP", "Dividing by negative number reverses inequality"))
            # Flip the relation
            flip_map = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}
            result_relation = flip_map[relation]
        else:
            result_relation = relation

        # Step 4: Result
        steps.append(step("INEQ_RESULT", "x", result_relation, boundary))

        # Final answer
        answer = f"x {result_relation} {boundary}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="one_step_inequality",
            problem=f"Solve the inequality: {equation}",
            steps=steps,
            final_answer=answer,
        )

    def _generate_division(self) -> dict:
        """Generate x/a ≥ b inequality, possibly with negative divisor."""
        relation = random.choice(self.RELATIONS)

        # Decide whether to use negative divisor
        if self.include_negative_coefficient and random.choice([True, False]):
            a = random.randint(-8, -2)
        else:
            a = random.randint(2, 8)

        b = random.randint(-8, 8)
        if b == 0:
            b = random.choice([-1, 1]) * random.randint(1, 8)

        boundary = a * b
        flipped = a < 0

        equation = f"x/{a} {relation} {b}"
        steps = []

        # Step 1: Set up inequality
        steps.append(step("INEQ_SETUP", equation))

        # Step 2: Multiply both sides by a
        steps.append(step("INEQ_OP_BOTH", "multiply", a, "x", boundary))

        # Step 3: Note flip if necessary
        if flipped:
            steps.append(step("INEQ_FLIP", "Multiplying by negative number reverses inequality"))
            flip_map = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}
            result_relation = flip_map[relation]
        else:
            result_relation = relation

        # Step 4: Result
        steps.append(step("INEQ_RESULT", "x", result_relation, boundary))

        # Final answer
        answer = f"x {result_relation} {boundary}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="one_step_inequality",
            problem=f"Solve the inequality: {equation}",
            steps=steps,
            final_answer=answer,
        )
