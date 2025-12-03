import random
import math
from base_generator import ProblemGenerator
from helpers import step, jid


class PythagoreanLegGenerator(ProblemGenerator):
    """
    Generates Pythagorean theorem problems to find a leg.

    Given hypotenuse (c) and one leg (a), find the other leg (b).
    Formula: a² + b² = c², so b = √(c² - a²)

    Uses Pythagorean triples to ensure clean answers.

    Op-codes used:
    - PYTHAG_SETUP: Set up the right triangle (hypotenuse, known_leg, unknown)
    - PYTHAG_FORMULA: State the theorem (a² + b² = c²)
    - PYTHAG_SUBSTITUTE: Substitute known values (equation)
    - PYTHAG_SQUARE: Calculate squares (value, squared)
    - PYTHAG_SOLVE: Solve for unknown (calculation, result)
    - PYTHAG_ROOT: Take square root (value, root)
    - Z: Final answer
    """

    # Pythagorean triples: (a, b, c) where a² + b² = c²
    TRIPLES = [
        (3, 4, 5),
        (5, 12, 13),
        (8, 15, 17),
        (7, 24, 25),
        (6, 8, 10),
        (9, 12, 15),
        (12, 16, 20),
        (15, 20, 25),
        (9, 40, 41),
        (11, 60, 61),
        (20, 21, 29),
        (12, 35, 37),
    ]

    def generate(self) -> dict:
        """Generate a Pythagorean theorem find-leg problem."""
        # Select a random triple
        triple = random.choice(self.TRIPLES)
        a, b, c = triple

        # Optionally scale the triple
        scale = random.choice([1, 2, 3])
        a, b, c = a * scale, b * scale, c * scale

        # Randomly choose which leg is given and which to find
        if random.choice([True, False]):
            given_leg = a
            unknown_leg = b
        else:
            given_leg = b
            unknown_leg = a

        problem = f"In a right triangle, the hypotenuse is {c} units and one leg is {given_leg} units. Find the length of the other leg."

        steps_list = []
        steps_list.append(step("PYTHAG_SETUP", f"c={c}", f"a={given_leg}", "b=?"))
        steps_list.append(step("PYTHAG_FORMULA", "a² + b² = c²"))
        steps_list.append(step("PYTHAG_SUBSTITUTE", f"{given_leg}² + b² = {c}²"))

        given_squared = given_leg ** 2
        hyp_squared = c ** 2

        steps_list.append(step("PYTHAG_SQUARE", given_leg, given_squared))
        steps_list.append(step("PYTHAG_SQUARE", c, hyp_squared))
        steps_list.append(step("PYTHAG_SOLVE", f"b² = {hyp_squared} - {given_squared}", hyp_squared - given_squared))

        b_squared = hyp_squared - given_squared
        steps_list.append(step("PYTHAG_ROOT", b_squared, unknown_leg))

        final_answer = f"{unknown_leg} units"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="pythagorean_find_leg",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )


class PythagoreanWordProblemGenerator(ProblemGenerator):
    """
    Generates word problems involving the Pythagorean theorem.

    Contexts include ladders against walls, diagonal of rectangles, etc.

    Op-codes used:
    - PYTHAG_CONTEXT: Describe the real-world setup (context, values)
    - PYTHAG_MODEL: Model as a right triangle (a, b, c identification)
    - PYTHAG_FORMULA: State the theorem
    - PYTHAG_SUBSTITUTE: Substitute values
    - PYTHAG_CALCULATE: Perform calculations
    - Z: Final answer
    """

    # Pythagorean triples
    TRIPLES = [
        (3, 4, 5),
        (5, 12, 13),
        (8, 15, 17),
        (6, 8, 10),
        (9, 12, 15),
        (12, 16, 20),
        (15, 20, 25),
    ]

    def generate(self) -> dict:
        """Generate a Pythagorean theorem word problem."""
        context = random.choice(['ladder', 'diagonal', 'distance'])

        triple = random.choice(self.TRIPLES)
        scale = random.choice([1, 2])
        a, b, c = triple[0] * scale, triple[1] * scale, triple[2] * scale

        if context == 'ladder':
            return self._generate_ladder(a, b, c)
        elif context == 'diagonal':
            return self._generate_diagonal(a, b, c)
        else:
            return self._generate_distance(a, b, c)

    def _generate_ladder(self, a, b, c) -> dict:
        """Generate ladder against wall problem."""
        # Ladder (c) against wall, find either height (b) or distance from wall (a)
        find_height = random.choice([True, False])

        if find_height:
            problem = f"A {c}-foot ladder is placed against a wall. The base of the ladder is {a} feet from the wall. How high up the wall does the ladder reach?"
            answer = b
            given = a
        else:
            problem = f"A {c}-foot ladder reaches {b} feet up a wall. How far is the base of the ladder from the wall?"
            answer = a
            given = b

        steps_list = []
        steps_list.append(step("PYTHAG_CONTEXT", "ladder", f"ladder={c}ft, given={given}ft"))
        steps_list.append(step("PYTHAG_MODEL", f"ground={a}", f"wall={b}", f"ladder={c}"))
        steps_list.append(step("PYTHAG_FORMULA", "a² + b² = c²"))

        if find_height:
            steps_list.append(step("PYTHAG_SUBSTITUTE", f"{a}² + h² = {c}²"))
            steps_list.append(step("PYTHAG_CALCULATE", f"h² = {c**2} - {a**2} = {c**2 - a**2}", c**2 - a**2))
            steps_list.append(step("PYTHAG_CALCULATE", f"h = √{c**2 - a**2}", answer))
        else:
            steps_list.append(step("PYTHAG_SUBSTITUTE", f"d² + {b}² = {c}²"))
            steps_list.append(step("PYTHAG_CALCULATE", f"d² = {c**2} - {b**2} = {c**2 - b**2}", c**2 - b**2))
            steps_list.append(step("PYTHAG_CALCULATE", f"d = √{c**2 - b**2}", answer))

        final_answer = f"{answer} feet"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="pythagorean_word_problem",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_diagonal(self, a, b, c) -> dict:
        """Generate rectangle diagonal problem."""
        problem = f"A rectangle has a length of {a} units and a width of {b} units. What is the length of its diagonal?"

        steps_list = []
        steps_list.append(step("PYTHAG_CONTEXT", "rectangle_diagonal", f"length={a}, width={b}"))
        steps_list.append(step("PYTHAG_MODEL", f"length={a}", f"width={b}", "diagonal=?"))
        steps_list.append(step("PYTHAG_FORMULA", "d² = l² + w²"))
        steps_list.append(step("PYTHAG_SUBSTITUTE", f"d² = {a}² + {b}²"))
        steps_list.append(step("PYTHAG_CALCULATE", f"d² = {a**2} + {b**2} = {a**2 + b**2}", a**2 + b**2))
        steps_list.append(step("PYTHAG_CALCULATE", f"d = √{c**2}", c))

        final_answer = f"{c} units"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="pythagorean_word_problem",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_distance(self, a, b, c) -> dict:
        """Generate distance/displacement problem."""
        problem = f"A person walks {a} meters east and then {b} meters north. What is the straight-line distance from the starting point?"

        steps_list = []
        steps_list.append(step("PYTHAG_CONTEXT", "displacement", f"east={a}m, north={b}m"))
        steps_list.append(step("PYTHAG_MODEL", f"east={a}", f"north={b}", "distance=?"))
        steps_list.append(step("PYTHAG_FORMULA", "d² = east² + north²"))
        steps_list.append(step("PYTHAG_SUBSTITUTE", f"d² = {a}² + {b}²"))
        steps_list.append(step("PYTHAG_CALCULATE", f"d² = {a**2} + {b**2} = {a**2 + b**2}", a**2 + b**2))
        steps_list.append(step("PYTHAG_CALCULATE", f"d = √{c**2}", c))

        final_answer = f"{c} meters"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="pythagorean_word_problem",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )
