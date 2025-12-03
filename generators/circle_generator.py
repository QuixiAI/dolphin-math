import random
import math
from base_generator import ProblemGenerator
from helpers import step, jid


class CircleAreaCircumferenceGenerator(ProblemGenerator):
    """
    Generates circle area and circumference problems.

    Formulas:
    - Circumference: C = 2πr or C = πd
    - Area: A = πr²

    Op-codes used:
    - CIRCLE_SETUP: Set up the circle (given_value, given_type)
    - CIRCLE_FORMULA: State the formula being used (formula)
    - CIRCLE_SUBSTITUTE: Substitute values (substitution)
    - CIRCLE_CALCULATE: Perform calculation (calculation, result)
    - Z: Final answer
    """

    def __init__(self, problem_type: str = None, use_pi_symbol: bool = True):
        """
        Initialize generator.

        Args:
            problem_type: One of 'area_from_radius', 'area_from_diameter',
                         'circumference_from_radius', 'circumference_from_diameter',
                         'radius_from_area', 'radius_from_circumference' or None for random
            use_pi_symbol: If True, leave answer in terms of π; if False, use 3.14
        """
        valid_types = ['area_from_radius', 'area_from_diameter',
                      'circumference_from_radius', 'circumference_from_diameter',
                      'radius_from_area', 'radius_from_circumference']
        if problem_type is not None and problem_type not in valid_types:
            raise ValueError(f"Invalid problem_type: {problem_type}. Must be one of {valid_types} or None.")
        self.problem_type = problem_type
        self.use_pi_symbol = use_pi_symbol

    def generate(self) -> dict:
        """Generate a circle problem."""
        ptype = self.problem_type or random.choice([
            'area_from_radius', 'area_from_diameter',
            'circumference_from_radius', 'circumference_from_diameter'
        ])

        if ptype == 'area_from_radius':
            return self._generate_area_from_radius()
        elif ptype == 'area_from_diameter':
            return self._generate_area_from_diameter()
        elif ptype == 'circumference_from_radius':
            return self._generate_circumference_from_radius()
        elif ptype == 'circumference_from_diameter':
            return self._generate_circumference_from_diameter()
        elif ptype == 'radius_from_area':
            return self._generate_radius_from_area()
        else:
            return self._generate_radius_from_circumference()

    def _generate_area_from_radius(self) -> dict:
        """Generate: Given radius, find area."""
        radius = random.randint(2, 15)

        problem = f"Find the area of a circle with radius {radius} units."

        steps_list = []
        steps_list.append(step("CIRCLE_SETUP", radius, "radius"))
        steps_list.append(step("CIRCLE_FORMULA", "A = πr²"))
        steps_list.append(step("CIRCLE_SUBSTITUTE", f"A = π × {radius}²"))

        r_squared = radius ** 2
        steps_list.append(step("CIRCLE_CALCULATE", f"A = π × {r_squared}", f"{r_squared}π"))

        if self.use_pi_symbol:
            final_answer = f"{r_squared}π square units"
        else:
            area = round(r_squared * 3.14, 2)
            steps_list.append(step("CIRCLE_CALCULATE", f"A ≈ {r_squared} × 3.14", area))
            final_answer = f"{area} square units"

        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="circle_area",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_area_from_diameter(self) -> dict:
        """Generate: Given diameter, find area."""
        diameter = random.randint(4, 20)
        radius = diameter / 2

        problem = f"Find the area of a circle with diameter {diameter} units."

        steps_list = []
        steps_list.append(step("CIRCLE_SETUP", diameter, "diameter"))
        steps_list.append(step("CIRCLE_CALCULATE", f"radius = diameter / 2 = {diameter} / 2", radius))
        steps_list.append(step("CIRCLE_FORMULA", "A = πr²"))
        steps_list.append(step("CIRCLE_SUBSTITUTE", f"A = π × {radius}²"))

        r_squared = radius ** 2
        steps_list.append(step("CIRCLE_CALCULATE", f"A = π × {r_squared}", f"{r_squared}π"))

        if self.use_pi_symbol:
            if r_squared == int(r_squared):
                final_answer = f"{int(r_squared)}π square units"
            else:
                final_answer = f"{r_squared}π square units"
        else:
            area = round(r_squared * 3.14, 2)
            steps_list.append(step("CIRCLE_CALCULATE", f"A ≈ {r_squared} × 3.14", area))
            final_answer = f"{area} square units"

        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="circle_area",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_circumference_from_radius(self) -> dict:
        """Generate: Given radius, find circumference."""
        radius = random.randint(2, 15)

        problem = f"Find the circumference of a circle with radius {radius} units."

        steps_list = []
        steps_list.append(step("CIRCLE_SETUP", radius, "radius"))
        steps_list.append(step("CIRCLE_FORMULA", "C = 2πr"))
        steps_list.append(step("CIRCLE_SUBSTITUTE", f"C = 2 × π × {radius}"))

        coef = 2 * radius
        steps_list.append(step("CIRCLE_CALCULATE", f"C = {coef}π", f"{coef}π"))

        if self.use_pi_symbol:
            final_answer = f"{coef}π units"
        else:
            circumference = round(coef * 3.14, 2)
            steps_list.append(step("CIRCLE_CALCULATE", f"C ≈ {coef} × 3.14", circumference))
            final_answer = f"{circumference} units"

        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="circle_circumference",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_circumference_from_diameter(self) -> dict:
        """Generate: Given diameter, find circumference."""
        diameter = random.randint(4, 20)

        problem = f"Find the circumference of a circle with diameter {diameter} units."

        steps_list = []
        steps_list.append(step("CIRCLE_SETUP", diameter, "diameter"))
        steps_list.append(step("CIRCLE_FORMULA", "C = πd"))
        steps_list.append(step("CIRCLE_SUBSTITUTE", f"C = π × {diameter}"))
        steps_list.append(step("CIRCLE_CALCULATE", f"C = {diameter}π", f"{diameter}π"))

        if self.use_pi_symbol:
            final_answer = f"{diameter}π units"
        else:
            circumference = round(diameter * 3.14, 2)
            steps_list.append(step("CIRCLE_CALCULATE", f"C ≈ {diameter} × 3.14", circumference))
            final_answer = f"{circumference} units"

        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="circle_circumference",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_radius_from_area(self) -> dict:
        """Generate: Given area, find radius."""
        radius = random.randint(2, 12)
        area = radius ** 2  # Area in terms of π (area = r²π)

        problem = f"A circle has an area of {area}π square units. Find the radius."

        steps_list = []
        steps_list.append(step("CIRCLE_SETUP", f"{area}π", "area"))
        steps_list.append(step("CIRCLE_FORMULA", "A = πr², so r² = A/π"))
        steps_list.append(step("CIRCLE_SUBSTITUTE", f"r² = {area}π / π = {area}"))
        steps_list.append(step("CIRCLE_CALCULATE", f"r = √{area}", radius))

        final_answer = f"{radius} units"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="circle_radius_from_area",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_radius_from_circumference(self) -> dict:
        """Generate: Given circumference, find radius."""
        radius = random.randint(2, 12)
        circumference = 2 * radius  # Circumference in terms of π

        problem = f"A circle has a circumference of {circumference}π units. Find the radius."

        steps_list = []
        steps_list.append(step("CIRCLE_SETUP", f"{circumference}π", "circumference"))
        steps_list.append(step("CIRCLE_FORMULA", "C = 2πr, so r = C/(2π)"))
        steps_list.append(step("CIRCLE_SUBSTITUTE", f"r = {circumference}π / (2π)"))
        steps_list.append(step("CIRCLE_CALCULATE", f"r = {circumference} / 2", radius))

        final_answer = f"{radius} units"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="circle_radius_from_circumference",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )
