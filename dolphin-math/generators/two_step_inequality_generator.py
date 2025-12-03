import random
from base_generator import ProblemGenerator
from helpers import step, jid


class TwoStepInequalityGenerator(ProblemGenerator):
    """
    Generates two-step linear inequalities.

    Problem types:
    - ax + b < c
    - ax - b > c
    - a(x + b) ≤ c
    - x/a + b ≥ c

    Op-codes used:
    - INEQ_SETUP: Set up the inequality (inequality_string)
    - INEQ_OP_BOTH: Apply operation to both sides (operation, value, new_left, new_right)
    - INEQ_SIMPLIFY: Simplify after operation (simplified_inequality)
    - INEQ_FLIP: Note when inequality flips (reason)
    - INEQ_RESULT: Show the result (variable, relation, value)
    - Z: Final answer
    """

    RELATIONS = ['<', '>', '≤', '≥']

    def __init__(self, problem_type: str = None, include_negative_coefficient: bool = True):
        """
        Initialize generator.

        Args:
            problem_type: One of 'standard', 'subtract', 'distribute', 'fraction' or None for random
            include_negative_coefficient: Whether to include problems requiring flip
        """
        valid_types = ['standard', 'subtract', 'distribute', 'fraction']
        if problem_type is not None and problem_type not in valid_types:
            raise ValueError(f"Invalid problem_type: {problem_type}. Must be one of {valid_types} or None.")
        self.problem_type = problem_type
        self.include_negative_coefficient = include_negative_coefficient

    def generate(self) -> dict:
        """Generate a two-step inequality problem."""
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
        """Generate ax + b < c inequality."""
        relation = random.choice(self.RELATIONS)

        # Decide on coefficient sign
        if self.include_negative_coefficient and random.choice([True, False]):
            a = random.randint(-8, -2)
        else:
            a = random.randint(2, 8)

        b = random.randint(1, 12)

        # Generate solution boundary
        boundary = random.randint(-10, 10)
        if boundary == 0:
            boundary = random.choice([-1, 1]) * random.randint(1, 10)

        c = a * boundary + b
        flipped = a < 0

        equation = f"{a}x + {b} {relation} {c}"
        steps = []

        # Step 1: Set up inequality
        steps.append(step("INEQ_SETUP", equation))

        # Step 2: Subtract b from both sides
        new_right = c - b
        steps.append(step("INEQ_OP_BOTH", "subtract", b, f"{a}x", new_right))

        # Step 3: Simplify
        steps.append(step("INEQ_SIMPLIFY", f"{a}x {relation} {new_right}"))

        # Step 4: Divide both sides by a
        steps.append(step("INEQ_OP_BOTH", "divide", a, "x", boundary))

        # Step 5: Note flip if necessary
        if flipped:
            steps.append(step("INEQ_FLIP", "Dividing by negative number reverses inequality"))
            flip_map = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}
            result_relation = flip_map[relation]
        else:
            result_relation = relation

        # Step 6: Result
        steps.append(step("INEQ_RESULT", "x", result_relation, boundary))

        # Final answer
        answer = f"x {result_relation} {boundary}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="two_step_inequality",
            problem=f"Solve the inequality: {equation}",
            steps=steps,
            final_answer=answer,
        )

    def _generate_subtract(self) -> dict:
        """Generate ax - b > c inequality."""
        relation = random.choice(self.RELATIONS)

        if self.include_negative_coefficient and random.choice([True, False]):
            a = random.randint(-8, -2)
        else:
            a = random.randint(2, 8)

        b = random.randint(1, 12)
        boundary = random.randint(-10, 10)
        if boundary == 0:
            boundary = random.choice([-1, 1]) * random.randint(1, 10)

        c = a * boundary - b
        flipped = a < 0

        equation = f"{a}x - {b} {relation} {c}"
        steps = []

        # Step 1: Set up inequality
        steps.append(step("INEQ_SETUP", equation))

        # Step 2: Add b to both sides
        new_right = c + b
        steps.append(step("INEQ_OP_BOTH", "add", b, f"{a}x", new_right))

        # Step 3: Simplify
        steps.append(step("INEQ_SIMPLIFY", f"{a}x {relation} {new_right}"))

        # Step 4: Divide both sides by a
        steps.append(step("INEQ_OP_BOTH", "divide", a, "x", boundary))

        # Step 5: Note flip if necessary
        if flipped:
            steps.append(step("INEQ_FLIP", "Dividing by negative number reverses inequality"))
            flip_map = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}
            result_relation = flip_map[relation]
        else:
            result_relation = relation

        # Step 6: Result
        steps.append(step("INEQ_RESULT", "x", result_relation, boundary))

        # Final answer
        answer = f"x {result_relation} {boundary}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="two_step_inequality",
            problem=f"Solve the inequality: {equation}",
            steps=steps,
            final_answer=answer,
        )

    def _generate_distribute(self) -> dict:
        """Generate a(x + b) ≤ c inequality."""
        relation = random.choice(self.RELATIONS)

        if self.include_negative_coefficient and random.choice([True, False]):
            a = random.randint(-6, -2)
        else:
            a = random.randint(2, 6)

        b = random.randint(1, 8)
        boundary = random.randint(-8, 8)
        if boundary == 0:
            boundary = random.choice([-1, 1]) * random.randint(1, 8)

        c = a * (boundary + b)
        flipped = a < 0

        equation = f"{a}(x + {b}) {relation} {c}"
        steps = []

        # Step 1: Set up inequality
        steps.append(step("INEQ_SETUP", equation))

        # Step 2: Divide both sides by a
        inner = c // a  # = boundary + b
        steps.append(step("INEQ_OP_BOTH", "divide", a, f"x + {b}", inner))

        # Step 3: Note flip if necessary (before simplify for clarity)
        if flipped:
            steps.append(step("INEQ_FLIP", "Dividing by negative number reverses inequality"))
            flip_map = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}
            current_relation = flip_map[relation]
        else:
            current_relation = relation

        # Step 4: Simplify
        steps.append(step("INEQ_SIMPLIFY", f"x + {b} {current_relation} {inner}"))

        # Step 5: Subtract b from both sides
        steps.append(step("INEQ_OP_BOTH", "subtract", b, "x", boundary))

        # Step 6: Result
        steps.append(step("INEQ_RESULT", "x", current_relation, boundary))

        # Final answer
        answer = f"x {current_relation} {boundary}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="two_step_inequality",
            problem=f"Solve the inequality: {equation}",
            steps=steps,
            final_answer=answer,
        )

    def _generate_fraction(self) -> dict:
        """Generate x/a + b ≥ c inequality."""
        relation = random.choice(self.RELATIONS)

        if self.include_negative_coefficient and random.choice([True, False]):
            a = random.randint(-6, -2)
        else:
            a = random.randint(2, 6)

        b = random.randint(1, 8)
        quotient = random.randint(-6, 6)
        if quotient == 0:
            quotient = random.choice([-1, 1]) * random.randint(1, 6)

        boundary = a * quotient
        c = quotient + b
        flipped = a < 0

        equation = f"x/{a} + {b} {relation} {c}"
        steps = []

        # Step 1: Set up inequality
        steps.append(step("INEQ_SETUP", equation))

        # Step 2: Subtract b from both sides
        new_right = c - b  # = quotient
        steps.append(step("INEQ_OP_BOTH", "subtract", b, f"x/{a}", new_right))

        # Step 3: Simplify
        steps.append(step("INEQ_SIMPLIFY", f"x/{a} {relation} {new_right}"))

        # Step 4: Multiply both sides by a
        steps.append(step("INEQ_OP_BOTH", "multiply", a, "x", boundary))

        # Step 5: Note flip if necessary
        if flipped:
            steps.append(step("INEQ_FLIP", "Multiplying by negative number reverses inequality"))
            flip_map = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}
            result_relation = flip_map[relation]
        else:
            result_relation = relation

        # Step 6: Result
        steps.append(step("INEQ_RESULT", "x", result_relation, boundary))

        # Final answer
        answer = f"x {result_relation} {boundary}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="two_step_inequality",
            problem=f"Solve the inequality: {equation}",
            steps=steps,
            final_answer=answer,
        )
