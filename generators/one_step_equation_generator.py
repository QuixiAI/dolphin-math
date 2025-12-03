import random
from base_generator import ProblemGenerator
from helpers import step, jid


class OneStepEquationGenerator(ProblemGenerator):
    """
    Generates one-step linear equations.

    Problem types:
    - x + a = b  (solve by subtracting)
    - x - a = b  (solve by adding)
    - ax = b     (solve by dividing)
    - x/a = b    (solve by multiplying)

    Op-codes used:
    - EQ_SETUP: Set up the equation (equation_string)
    - EQ_OP_BOTH: Apply operation to both sides (operation, value, left_result, right_result)
    - EQ_RESULT: Show the result (variable, value)
    - Z: Final answer
    """

    def __init__(self, operation: str = None, allow_negative: bool = True):
        """
        Initialize generator.

        Args:
            operation: One of '+', '-', '*', '/' or None for random
            allow_negative: Whether to allow negative solutions
        """
        if operation is not None and operation not in ['+', '-', '*', '/']:
            raise ValueError(f"Invalid operation: {operation}. Must be +, -, *, /, or None.")
        self.operation = operation
        self.allow_negative = allow_negative

    def generate(self) -> dict:
        """Generate a one-step equation problem."""
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
        """Generate x + a = b equation."""
        # x + a = b, solve by subtracting a from both sides
        a = random.randint(1, 20)

        if self.allow_negative:
            x = random.randint(-15, 20)
        else:
            x = random.randint(1, 20)

        b = x + a

        equation = f"x + {a} = {b}"
        steps = []

        # Step 1: Set up equation
        steps.append(step("EQ_SETUP", equation))

        # Step 2: Subtract a from both sides
        steps.append(step("EQ_OP_BOTH", "subtract", a, "x", b - a))

        # Step 3: Result
        steps.append(step("EQ_RESULT", "x", x))

        # Final answer
        steps.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="one_step_equation_add",
            problem=f"Solve for x: {equation}",
            steps=steps,
            final_answer=str(x),
        )

    def _generate_subtraction(self) -> dict:
        """Generate x - a = b equation."""
        # x - a = b, solve by adding a to both sides
        a = random.randint(1, 20)

        if self.allow_negative:
            b = random.randint(-15, 20)
        else:
            b = random.randint(1, 20)

        x = b + a

        equation = f"x - {a} = {b}"
        steps = []

        # Step 1: Set up equation
        steps.append(step("EQ_SETUP", equation))

        # Step 2: Add a to both sides
        steps.append(step("EQ_OP_BOTH", "add", a, "x", b + a))

        # Step 3: Result
        steps.append(step("EQ_RESULT", "x", x))

        # Final answer
        steps.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="one_step_equation_sub",
            problem=f"Solve for x: {equation}",
            steps=steps,
            final_answer=str(x),
        )

    def _generate_multiplication(self) -> dict:
        """Generate ax = b equation."""
        # ax = b, solve by dividing both sides by a
        a = random.randint(2, 12)

        if self.allow_negative:
            x = random.randint(-12, 12)
            if x == 0:
                x = random.choice([-1, 1]) * random.randint(1, 12)
        else:
            x = random.randint(1, 12)

        b = a * x

        equation = f"{a}x = {b}"
        steps = []

        # Step 1: Set up equation
        steps.append(step("EQ_SETUP", equation))

        # Step 2: Divide both sides by a
        steps.append(step("EQ_OP_BOTH", "divide", a, "x", b // a))

        # Step 3: Result
        steps.append(step("EQ_RESULT", "x", x))

        # Final answer
        steps.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="one_step_equation_mult",
            problem=f"Solve for x: {equation}",
            steps=steps,
            final_answer=str(x),
        )

    def _generate_division(self) -> dict:
        """Generate x/a = b equation."""
        # x/a = b, solve by multiplying both sides by a
        a = random.randint(2, 10)

        if self.allow_negative:
            b = random.randint(-10, 10)
            if b == 0:
                b = random.choice([-1, 1]) * random.randint(1, 10)
        else:
            b = random.randint(1, 10)

        x = a * b

        equation = f"x/{a} = {b}"
        steps = []

        # Step 1: Set up equation
        steps.append(step("EQ_SETUP", equation))

        # Step 2: Multiply both sides by a
        steps.append(step("EQ_OP_BOTH", "multiply", a, "x", a * b))

        # Step 3: Result
        steps.append(step("EQ_RESULT", "x", x))

        # Final answer
        steps.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="one_step_equation_div",
            problem=f"Solve for x: {equation}",
            steps=steps,
            final_answer=str(x),
        )
