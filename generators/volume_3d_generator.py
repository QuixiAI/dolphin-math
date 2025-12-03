import random
import math
from base_generator import ProblemGenerator
from helpers import step, jid


class VolumePrismGenerator(ProblemGenerator):
    """
    Generates volume of prism problems.

    Prism types:
    - Rectangular prism: V = l × w × h
    - Triangular prism: V = (1/2 × b × h_triangle) × length

    Op-codes used:
    - VOL_SETUP: Set up the 3D shape (shape_type, dimensions)
    - VOL_FORMULA: State the volume formula (formula)
    - VOL_BASE_AREA: Calculate base area if needed (calculation, result)
    - VOL_CALCULATE: Calculate volume (calculation, result)
    - Z: Final answer
    """

    def __init__(self, prism_type: str = None):
        """
        Initialize generator.

        Args:
            prism_type: One of 'rectangular', 'triangular' or None for random
        """
        valid_types = ['rectangular', 'triangular']
        if prism_type is not None and prism_type not in valid_types:
            raise ValueError(f"Invalid prism_type: {prism_type}. Must be one of {valid_types} or None.")
        self.prism_type = prism_type

    def generate(self) -> dict:
        """Generate a prism volume problem."""
        ptype = self.prism_type or random.choice(['rectangular', 'triangular'])

        if ptype == 'rectangular':
            return self._generate_rectangular()
        else:
            return self._generate_triangular()

    def _generate_rectangular(self) -> dict:
        """Generate rectangular prism volume problem."""
        length = random.randint(3, 15)
        width = random.randint(3, 15)
        height = random.randint(3, 15)

        volume = length * width * height

        problem = f"Find the volume of a rectangular prism with length {length} units, width {width} units, and height {height} units."

        steps_list = []
        steps_list.append(step("VOL_SETUP", "rectangular_prism", f"l={length}, w={width}, h={height}"))
        steps_list.append(step("VOL_FORMULA", "V = l × w × h"))
        steps_list.append(step("VOL_CALCULATE", f"V = {length} × {width} × {height}", volume))

        final_answer = f"{volume} cubic units"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="volume_rectangular_prism",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_triangular(self) -> dict:
        """Generate triangular prism volume problem."""
        base = random.randint(4, 12)
        tri_height = random.randint(3, 10)
        length = random.randint(5, 15)

        # Base area = (1/2) × base × tri_height
        base_area = (base * tri_height) / 2
        volume = base_area * length

        problem = f"Find the volume of a triangular prism. The triangular base has a base of {base} units and height of {tri_height} units. The prism has a length of {length} units."

        steps_list = []
        steps_list.append(step("VOL_SETUP", "triangular_prism", f"b={base}, h_tri={tri_height}, length={length}"))
        steps_list.append(step("VOL_FORMULA", "V = Base Area × length"))
        steps_list.append(step("VOL_BASE_AREA", f"Base Area = (1/2) × {base} × {tri_height}", base_area))
        steps_list.append(step("VOL_CALCULATE", f"V = {base_area} × {length}", volume))

        if volume == int(volume):
            final_answer = f"{int(volume)} cubic units"
        else:
            final_answer = f"{volume} cubic units"

        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="volume_triangular_prism",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )


class VolumeCylinderGenerator(ProblemGenerator):
    """
    Generates volume of cylinder problems.

    Formula: V = πr²h

    Op-codes used:
    - VOL_SETUP: Set up the cylinder (radius, height)
    - VOL_FORMULA: State the formula (formula)
    - VOL_BASE_AREA: Calculate base area (calculation, result)
    - VOL_CALCULATE: Calculate volume (calculation, result)
    - Z: Final answer
    """

    def __init__(self, use_pi_symbol: bool = True):
        """
        Initialize generator.

        Args:
            use_pi_symbol: If True, leave answer in terms of π; if False, use 3.14
        """
        self.use_pi_symbol = use_pi_symbol

    def generate(self) -> dict:
        """Generate a cylinder volume problem."""
        # Randomly choose to give radius or diameter
        give_diameter = random.choice([True, False])

        if give_diameter:
            diameter = random.randint(4, 16)
            radius = diameter / 2
            height = random.randint(5, 20)
            problem = f"Find the volume of a cylinder with diameter {diameter} units and height {height} units."
        else:
            radius = random.randint(2, 10)
            height = random.randint(5, 20)
            problem = f"Find the volume of a cylinder with radius {radius} units and height {height} units."

        r_squared = radius ** 2
        volume_coef = r_squared * height

        steps_list = []

        if give_diameter:
            steps_list.append(step("VOL_SETUP", "cylinder", f"d={diameter}, h={height}"))
            steps_list.append(step("VOL_CALCULATE", f"radius = {diameter} / 2", radius))
        else:
            steps_list.append(step("VOL_SETUP", "cylinder", f"r={radius}, h={height}"))

        steps_list.append(step("VOL_FORMULA", "V = πr²h"))
        steps_list.append(step("VOL_BASE_AREA", f"r² = {radius}² = {r_squared}", r_squared))
        steps_list.append(step("VOL_CALCULATE", f"V = π × {r_squared} × {height}", f"{volume_coef}π"))

        if self.use_pi_symbol:
            if volume_coef == int(volume_coef):
                final_answer = f"{int(volume_coef)}π cubic units"
            else:
                final_answer = f"{volume_coef}π cubic units"
        else:
            volume = round(volume_coef * 3.14, 2)
            steps_list.append(step("VOL_CALCULATE", f"V ≈ {volume_coef} × 3.14", volume))
            final_answer = f"{volume} cubic units"

        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="volume_cylinder",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )


class SurfaceAreaPrismGenerator(ProblemGenerator):
    """
    Generates surface area of prism problems.

    Rectangular prism: SA = 2(lw + lh + wh)

    Op-codes used:
    - SA_SETUP: Set up the 3D shape (shape_type, dimensions)
    - SA_FORMULA: State the formula (formula)
    - SA_FACES: Calculate each face area (face_type, calculation, area)
    - SA_TOTAL: Sum all faces (calculation, result)
    - Z: Final answer
    """

    def generate(self) -> dict:
        """Generate a rectangular prism surface area problem."""
        length = random.randint(3, 12)
        width = random.randint(3, 12)
        height = random.randint(3, 12)

        # Calculate face areas
        top_bottom = length * width
        front_back = length * height
        left_right = width * height

        surface_area = 2 * (top_bottom + front_back + left_right)

        problem = f"Find the surface area of a rectangular prism with length {length} units, width {width} units, and height {height} units."

        steps_list = []
        steps_list.append(step("SA_SETUP", "rectangular_prism", f"l={length}, w={width}, h={height}"))
        steps_list.append(step("SA_FORMULA", "SA = 2(lw + lh + wh)"))
        steps_list.append(step("SA_FACES", "top/bottom", f"{length} × {width}", top_bottom))
        steps_list.append(step("SA_FACES", "front/back", f"{length} × {height}", front_back))
        steps_list.append(step("SA_FACES", "left/right", f"{width} × {height}", left_right))
        steps_list.append(step("SA_TOTAL", f"SA = 2({top_bottom} + {front_back} + {left_right})", surface_area))

        final_answer = f"{surface_area} square units"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="surface_area_rectangular_prism",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )


class SurfaceAreaCylinderGenerator(ProblemGenerator):
    """
    Generates surface area of cylinder problems.

    Formula: SA = 2πr² + 2πrh = 2πr(r + h)

    Op-codes used:
    - SA_SETUP: Set up the cylinder (radius, height)
    - SA_FORMULA: State the formula (formula)
    - SA_BASES: Calculate circular base areas (calculation, result)
    - SA_LATERAL: Calculate lateral surface area (calculation, result)
    - SA_TOTAL: Sum all areas (calculation, result)
    - Z: Final answer
    """

    def __init__(self, use_pi_symbol: bool = True):
        """
        Initialize generator.

        Args:
            use_pi_symbol: If True, leave answer in terms of π
        """
        self.use_pi_symbol = use_pi_symbol

    def generate(self) -> dict:
        """Generate a cylinder surface area problem."""
        radius = random.randint(2, 10)
        height = random.randint(5, 15)

        # Bases: 2πr²
        bases_coef = 2 * radius ** 2

        # Lateral: 2πrh
        lateral_coef = 2 * radius * height

        total_coef = bases_coef + lateral_coef

        problem = f"Find the surface area of a cylinder with radius {radius} units and height {height} units."

        steps_list = []
        steps_list.append(step("SA_SETUP", "cylinder", f"r={radius}, h={height}"))
        steps_list.append(step("SA_FORMULA", "SA = 2πr² + 2πrh"))
        steps_list.append(step("SA_BASES", f"2π({radius})² = 2π × {radius**2}", f"{bases_coef}π"))
        steps_list.append(step("SA_LATERAL", f"2π × {radius} × {height}", f"{lateral_coef}π"))
        steps_list.append(step("SA_TOTAL", f"SA = {bases_coef}π + {lateral_coef}π", f"{total_coef}π"))

        if self.use_pi_symbol:
            final_answer = f"{total_coef}π square units"
        else:
            surface_area = round(total_coef * 3.14, 2)
            steps_list.append(step("SA_TOTAL", f"SA ≈ {total_coef} × 3.14", surface_area))
            final_answer = f"{surface_area} square units"

        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="surface_area_cylinder",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )
