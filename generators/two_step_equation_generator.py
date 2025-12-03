import random
from base_generator import ProblemGenerator
from helpers import step, jid


class TwoStepEquationGenerator(ProblemGenerator):
    """
    Generates two-step linear equations.

    Problem types:
    - ax + b = c  (standard form)
    - ax - b = c
    - a(x + b) = c  (with distribution first)
    - x/a + b = c

    Op-codes used:
    - EQ_SETUP: Set up the equation (equation_string)
    - EQ_OP_BOTH: Apply operation to both sides (operation, value, new_left, new_right)
    - EQ_SIMPLIFY: Simplify after operation (simplified_equation)
    - EQ_RESULT: Show the result (variable, value)
    - Z: Final answer
    """

    def __init__(self, problem_type: str = None, allow_negative: bool = True):
        """
        Initialize generator.

        Args:
            problem_type: One of 'standard', 'subtract', 'distribute', 'fraction' or None for random
            allow_negative: Whether to allow negative solutions
        """
        valid_types = ['standard', 'subtract', 'distribute', 'fraction']
        if problem_type is not None and problem_type not in valid_types:
            raise ValueError(f"Invalid problem_type: {problem_type}. Must be one of {valid_types} or None.")
        self.problem_type = problem_type
        self.allow_negative = allow_negative

    def generate(self) -> dict:
        """Generate a two-step equation problem."""
        ptype = self.problem_type or random.choice(['standard', 'subtract', 'distribute', 'fraction'])

        if ptype == 'standard':
            return self._generate_standard()
        elif ptype == 'subtract':
            return self._generate_subtract()
        elif ptype == 'distribute':
            return self._generate_distribute()
        else:
            return self._generate_fraction()

    def _generate_standard(self) -> dict:
        """Generate ax + b = c equation."""
        # ax + b = c
        # Step 1: Subtract b from both sides -> ax = c - b
        # Step 2: Divide both sides by a -> x = (c - b) / a
        a = random.randint(2, 10)
        b = random.randint(1, 15)

        if self.allow_negative:
            x = random.randint(-10, 10)
            if x == 0:
                x = random.choice([-1, 1]) * random.randint(1, 10)
        else:
            x = random.randint(1, 10)

        c = a * x + b

        equation = f"{a}x + {b} = {c}"
        steps = []

        # Step 1: Set up equation
        steps.append(step("EQ_SETUP", equation))

        # Step 2: Subtract b from both sides
        new_right = c - b
        steps.append(step("EQ_OP_BOTH", "subtract", b, f"{a}x", new_right))

        # Step 3: Simplify
        steps.append(step("EQ_SIMPLIFY", f"{a}x = {new_right}"))

        # Step 4: Divide both sides by a
        steps.append(step("EQ_OP_BOTH", "divide", a, "x", x))

        # Step 5: Result
        steps.append(step("EQ_RESULT", "x", x))

        # Final answer
        steps.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="two_step_equation",
            problem=f"Solve for x: {equation}",
            steps=steps,
            final_answer=str(x),
        )

    def _generate_subtract(self) -> dict:
        """Generate ax - b = c equation."""
        # ax - b = c
        # Step 1: Add b to both sides -> ax = c + b
        # Step 2: Divide both sides by a -> x = (c + b) / a
        a = random.randint(2, 10)
        b = random.randint(1, 15)

        if self.allow_negative:
            x = random.randint(-10, 10)
            if x == 0:
                x = random.choice([-1, 1]) * random.randint(1, 10)
        else:
            x = random.randint(1, 10)

        c = a * x - b

        equation = f"{a}x - {b} = {c}"
        steps = []

        # Step 1: Set up equation
        steps.append(step("EQ_SETUP", equation))

        # Step 2: Add b to both sides
        new_right = c + b
        steps.append(step("EQ_OP_BOTH", "add", b, f"{a}x", new_right))

        # Step 3: Simplify
        steps.append(step("EQ_SIMPLIFY", f"{a}x = {new_right}"))

        # Step 4: Divide both sides by a
        steps.append(step("EQ_OP_BOTH", "divide", a, "x", x))

        # Step 5: Result
        steps.append(step("EQ_RESULT", "x", x))

        # Final answer
        steps.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="two_step_equation",
            problem=f"Solve for x: {equation}",
            steps=steps,
            final_answer=str(x),
        )

    def _generate_distribute(self) -> dict:
        """Generate a(x + b) = c equation."""
        # a(x + b) = c
        # Step 1: Divide both sides by a -> x + b = c/a
        # Step 2: Subtract b from both sides -> x = c/a - b
        a = random.randint(2, 8)
        b = random.randint(1, 10)

        if self.allow_negative:
            x = random.randint(-8, 8)
            if x == 0:
                x = random.choice([-1, 1]) * random.randint(1, 8)
        else:
            x = random.randint(1, 8)

        c = a * (x + b)

        equation = f"{a}(x + {b}) = {c}"
        steps = []

        # Step 1: Set up equation
        steps.append(step("EQ_SETUP", equation))

        # Step 2: Divide both sides by a
        inner = c // a  # = x + b
        steps.append(step("EQ_OP_BOTH", "divide", a, f"x + {b}", inner))

        # Step 3: Simplify
        steps.append(step("EQ_SIMPLIFY", f"x + {b} = {inner}"))

        # Step 4: Subtract b from both sides
        steps.append(step("EQ_OP_BOTH", "subtract", b, "x", x))

        # Step 5: Result
        steps.append(step("EQ_RESULT", "x", x))

        # Final answer
        steps.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="two_step_equation",
            problem=f"Solve for x: {equation}",
            steps=steps,
            final_answer=str(x),
        )

    def _generate_fraction(self) -> dict:
        """Generate x/a + b = c equation."""
        # x/a + b = c
        # Step 1: Subtract b from both sides -> x/a = c - b
        # Step 2: Multiply both sides by a -> x = a(c - b)
        a = random.randint(2, 8)
        b = random.randint(1, 10)

        if self.allow_negative:
            quotient = random.randint(-8, 8)
            if quotient == 0:
                quotient = random.choice([-1, 1]) * random.randint(1, 8)
        else:
            quotient = random.randint(1, 8)

        x = a * quotient
        c = quotient + b

        equation = f"x/{a} + {b} = {c}"
        steps = []

        # Step 1: Set up equation
        steps.append(step("EQ_SETUP", equation))

        # Step 2: Subtract b from both sides
        new_right = c - b
        steps.append(step("EQ_OP_BOTH", "subtract", b, f"x/{a}", new_right))

        # Step 3: Simplify
        steps.append(step("EQ_SIMPLIFY", f"x/{a} = {new_right}"))

        # Step 4: Multiply both sides by a
        steps.append(step("EQ_OP_BOTH", "multiply", a, "x", x))

        # Step 5: Result
        steps.append(step("EQ_RESULT", "x", x))

        # Final answer
        steps.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="two_step_equation",
            problem=f"Solve for x: {equation}",
            steps=steps,
            final_answer=str(x),
        )
