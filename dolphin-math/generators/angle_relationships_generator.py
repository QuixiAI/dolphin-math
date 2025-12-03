import random
from base_generator import ProblemGenerator
from helpers import step, jid


class AngleRelationshipsGenerator(ProblemGenerator):
    """
    Generates angle relationship problems.

    Problem types:
    - Complementary angles (sum to 90°)
    - Supplementary angles (sum to 180°)
    - Vertical angles (equal)

    Op-codes used:
    - ANGLE_SETUP: Set up the angle relationship (relationship_type, given_info)
    - ANGLE_RELATION: State the relationship (equation)
    - ANGLE_SOLVE: Solve for the unknown (operation, result)
    - Z: Final answer
    """

    def __init__(self, relationship_type: str = None):
        """
        Initialize generator.

        Args:
            relationship_type: One of 'complementary', 'supplementary', 'vertical' or None for random
        """
        valid_types = ['complementary', 'supplementary', 'vertical']
        if relationship_type is not None and relationship_type not in valid_types:
            raise ValueError(f"Invalid relationship_type: {relationship_type}. Must be one of {valid_types} or None.")
        self.relationship_type = relationship_type

    def generate(self) -> dict:
        """Generate an angle relationship problem."""
        rel_type = self.relationship_type or random.choice(['complementary', 'supplementary', 'vertical'])

        if rel_type == 'complementary':
            return self._generate_complementary()
        elif rel_type == 'supplementary':
            return self._generate_supplementary()
        else:
            return self._generate_vertical()

    def _generate_complementary(self) -> dict:
        """Generate complementary angles problem (sum to 90°)."""
        # Generate one angle, find the other
        angle1 = random.randint(10, 80)
        angle2 = 90 - angle1

        # Decide problem format
        problem_format = random.choice(['find_complement', 'algebraic'])

        if problem_format == 'find_complement':
            problem = f"Two angles are complementary. One angle measures {angle1}°. What is the measure of the other angle?"

            steps_list = []
            steps_list.append(step("ANGLE_SETUP", "complementary", f"angle1 = {angle1}°"))
            steps_list.append(step("ANGLE_RELATION", "angle1 + angle2 = 90°"))
            steps_list.append(step("ANGLE_SOLVE", f"90 - {angle1}", angle2))
            steps_list.append(step("Z", f"{angle2}°"))

            return dict(
                problem_id=jid(),
                operation="complementary_angles",
                problem=problem,
                steps=steps_list,
                final_answer=f"{angle2}°",
            )
        else:
            # Algebraic: (2x + a)° and (3x + b)° are complementary
            x = random.randint(5, 15)
            coef1 = random.randint(2, 5)
            coef2 = random.randint(2, 5)
            const1 = random.randint(0, 20)
            # Calculate const2 so that coef1*x + const1 + coef2*x + const2 = 90
            const2 = 90 - (coef1 * x + const1 + coef2 * x)

            expr1 = f"{coef1}x + {const1}" if const1 > 0 else f"{coef1}x"
            expr2 = f"{coef2}x + {const2}" if const2 >= 0 else f"{coef2}x - {-const2}"

            problem = f"Two complementary angles measure ({expr1})° and ({expr2})°. Find the value of x."

            steps_list = []
            steps_list.append(step("ANGLE_SETUP", "complementary", f"({expr1})° + ({expr2})° = 90°"))
            combined_coef = coef1 + coef2
            combined_const = const1 + const2
            steps_list.append(step("ANGLE_RELATION", f"{combined_coef}x + {combined_const} = 90"))
            steps_list.append(step("ANGLE_SOLVE", f"{combined_coef}x = {90 - combined_const}", f"x = {x}"))
            steps_list.append(step("Z", x))

            return dict(
                problem_id=jid(),
                operation="complementary_angles_algebraic",
                problem=problem,
                steps=steps_list,
                final_answer=str(x),
            )

    def _generate_supplementary(self) -> dict:
        """Generate supplementary angles problem (sum to 180°)."""
        angle1 = random.randint(20, 160)
        angle2 = 180 - angle1

        problem_format = random.choice(['find_supplement', 'algebraic'])

        if problem_format == 'find_supplement':
            problem = f"Two angles are supplementary. One angle measures {angle1}°. What is the measure of the other angle?"

            steps_list = []
            steps_list.append(step("ANGLE_SETUP", "supplementary", f"angle1 = {angle1}°"))
            steps_list.append(step("ANGLE_RELATION", "angle1 + angle2 = 180°"))
            steps_list.append(step("ANGLE_SOLVE", f"180 - {angle1}", angle2))
            steps_list.append(step("Z", f"{angle2}°"))

            return dict(
                problem_id=jid(),
                operation="supplementary_angles",
                problem=problem,
                steps=steps_list,
                final_answer=f"{angle2}°",
            )
        else:
            # Algebraic
            x = random.randint(10, 25)
            coef1 = random.randint(2, 6)
            coef2 = random.randint(2, 6)
            const1 = random.randint(0, 30)
            const2 = 180 - (coef1 * x + const1 + coef2 * x)

            expr1 = f"{coef1}x + {const1}" if const1 > 0 else f"{coef1}x"
            expr2 = f"{coef2}x + {const2}" if const2 >= 0 else f"{coef2}x - {-const2}"

            problem = f"Two supplementary angles measure ({expr1})° and ({expr2})°. Find the value of x."

            steps_list = []
            steps_list.append(step("ANGLE_SETUP", "supplementary", f"({expr1})° + ({expr2})° = 180°"))
            combined_coef = coef1 + coef2
            combined_const = const1 + const2
            steps_list.append(step("ANGLE_RELATION", f"{combined_coef}x + {combined_const} = 180"))
            steps_list.append(step("ANGLE_SOLVE", f"{combined_coef}x = {180 - combined_const}", f"x = {x}"))
            steps_list.append(step("Z", x))

            return dict(
                problem_id=jid(),
                operation="supplementary_angles_algebraic",
                problem=problem,
                steps=steps_list,
                final_answer=str(x),
            )

    def _generate_vertical(self) -> dict:
        """Generate vertical angles problem (equal angles)."""
        # Vertical angles are equal
        x = random.randint(5, 20)
        coef1 = random.randint(2, 6)
        const1 = random.randint(5, 30)

        # angle1 = coef1 * x + const1
        angle_value = coef1 * x + const1

        # angle2 expressed differently but equals angle1
        coef2 = random.randint(2, 6)
        const2 = angle_value - coef2 * x

        expr1 = f"{coef1}x + {const1}"
        expr2 = f"{coef2}x + {const2}" if const2 >= 0 else f"{coef2}x - {-const2}"

        problem = f"Two vertical angles measure ({expr1})° and ({expr2})°. Find the value of x."

        steps_list = []
        steps_list.append(step("ANGLE_SETUP", "vertical", "Vertical angles are equal"))
        steps_list.append(step("ANGLE_RELATION", f"{expr1} = {expr2}"))

        # Solve: coef1*x + const1 = coef2*x + const2
        # (coef1 - coef2)*x = const2 - const1
        coef_diff = coef1 - coef2
        const_diff = const2 - const1

        if coef_diff != 0:
            steps_list.append(step("ANGLE_SOLVE", f"{coef_diff}x = {const_diff}", f"x = {x}"))
        else:
            # Edge case: same coefficient, solve differently
            steps_list.append(step("ANGLE_SOLVE", f"x = {x}", f"x = {x}"))

        steps_list.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="vertical_angles",
            problem=problem,
            steps=steps_list,
            final_answer=str(x),
        )


class AnglesWithParallelLinesGenerator(ProblemGenerator):
    """
    Generates problems involving angles formed by parallel lines and a transversal.

    Angle types:
    - Corresponding angles (equal)
    - Alternate interior angles (equal)
    - Alternate exterior angles (equal)
    - Co-interior/Same-side interior angles (supplementary)

    Op-codes used:
    - PARALLEL_SETUP: Set up the parallel lines scenario (angle_type, relationship)
    - PARALLEL_RELATION: State the angle relationship (equation)
    - PARALLEL_SOLVE: Solve for the unknown (steps, result)
    - Z: Final answer
    """

    ANGLE_TYPES = ['corresponding', 'alternate_interior', 'alternate_exterior', 'co_interior']

    def __init__(self, angle_type: str = None):
        """
        Initialize generator.

        Args:
            angle_type: One of the ANGLE_TYPES or None for random
        """
        if angle_type is not None and angle_type not in self.ANGLE_TYPES:
            raise ValueError(f"Invalid angle_type: {angle_type}. Must be one of {self.ANGLE_TYPES} or None.")
        self.angle_type = angle_type

    def generate(self) -> dict:
        """Generate a parallel lines angle problem."""
        angle_type = self.angle_type or random.choice(self.ANGLE_TYPES)

        if angle_type == 'corresponding':
            return self._generate_corresponding()
        elif angle_type == 'alternate_interior':
            return self._generate_alternate_interior()
        elif angle_type == 'alternate_exterior':
            return self._generate_alternate_exterior()
        else:
            return self._generate_co_interior()

    def _generate_corresponding(self) -> dict:
        """Generate corresponding angles problem (equal)."""
        x = random.randint(5, 20)
        coef1 = random.randint(2, 6)
        const1 = random.randint(5, 40)
        angle_value = coef1 * x + const1

        coef2 = random.randint(2, 6)
        const2 = angle_value - coef2 * x

        expr1 = f"{coef1}x + {const1}"
        expr2 = f"{coef2}x + {const2}" if const2 >= 0 else f"{coef2}x - {-const2}"

        problem = f"Two parallel lines are cut by a transversal. Corresponding angles measure ({expr1})° and ({expr2})°. Find x."

        steps_list = []
        steps_list.append(step("PARALLEL_SETUP", "corresponding", "Corresponding angles are equal"))
        steps_list.append(step("PARALLEL_RELATION", f"{expr1} = {expr2}"))

        coef_diff = coef1 - coef2
        const_diff = const2 - const1

        steps_list.append(step("PARALLEL_SOLVE", f"{coef_diff}x = {const_diff}", f"x = {x}"))
        steps_list.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="parallel_corresponding_angles",
            problem=problem,
            steps=steps_list,
            final_answer=str(x),
        )

    def _generate_alternate_interior(self) -> dict:
        """Generate alternate interior angles problem (equal)."""
        x = random.randint(5, 20)
        coef1 = random.randint(2, 6)
        const1 = random.randint(5, 40)
        angle_value = coef1 * x + const1

        coef2 = random.randint(2, 6)
        const2 = angle_value - coef2 * x

        expr1 = f"{coef1}x + {const1}"
        expr2 = f"{coef2}x + {const2}" if const2 >= 0 else f"{coef2}x - {-const2}"

        problem = f"Two parallel lines are cut by a transversal. Alternate interior angles measure ({expr1})° and ({expr2})°. Find x."

        steps_list = []
        steps_list.append(step("PARALLEL_SETUP", "alternate_interior", "Alternate interior angles are equal"))
        steps_list.append(step("PARALLEL_RELATION", f"{expr1} = {expr2}"))

        coef_diff = coef1 - coef2
        const_diff = const2 - const1

        steps_list.append(step("PARALLEL_SOLVE", f"{coef_diff}x = {const_diff}", f"x = {x}"))
        steps_list.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="parallel_alternate_interior_angles",
            problem=problem,
            steps=steps_list,
            final_answer=str(x),
        )

    def _generate_alternate_exterior(self) -> dict:
        """Generate alternate exterior angles problem (equal)."""
        x = random.randint(5, 20)
        coef1 = random.randint(2, 6)
        const1 = random.randint(5, 40)
        angle_value = coef1 * x + const1

        coef2 = random.randint(2, 6)
        const2 = angle_value - coef2 * x

        expr1 = f"{coef1}x + {const1}"
        expr2 = f"{coef2}x + {const2}" if const2 >= 0 else f"{coef2}x - {-const2}"

        problem = f"Two parallel lines are cut by a transversal. Alternate exterior angles measure ({expr1})° and ({expr2})°. Find x."

        steps_list = []
        steps_list.append(step("PARALLEL_SETUP", "alternate_exterior", "Alternate exterior angles are equal"))
        steps_list.append(step("PARALLEL_RELATION", f"{expr1} = {expr2}"))

        coef_diff = coef1 - coef2
        const_diff = const2 - const1

        steps_list.append(step("PARALLEL_SOLVE", f"{coef_diff}x = {const_diff}", f"x = {x}"))
        steps_list.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="parallel_alternate_exterior_angles",
            problem=problem,
            steps=steps_list,
            final_answer=str(x),
        )

    def _generate_co_interior(self) -> dict:
        """Generate co-interior (same-side interior) angles problem (sum to 180°)."""
        x = random.randint(10, 25)
        coef1 = random.randint(2, 5)
        coef2 = random.randint(2, 5)
        const1 = random.randint(5, 30)
        # coef1*x + const1 + coef2*x + const2 = 180
        const2 = 180 - (coef1 * x + const1 + coef2 * x)

        expr1 = f"{coef1}x + {const1}"
        expr2 = f"{coef2}x + {const2}" if const2 >= 0 else f"{coef2}x - {-const2}"

        problem = f"Two parallel lines are cut by a transversal. Co-interior angles measure ({expr1})° and ({expr2})°. Find x."

        steps_list = []
        steps_list.append(step("PARALLEL_SETUP", "co_interior", "Co-interior angles are supplementary (sum to 180°)"))
        steps_list.append(step("PARALLEL_RELATION", f"({expr1}) + ({expr2}) = 180"))

        combined_coef = coef1 + coef2
        combined_const = const1 + const2

        steps_list.append(step("PARALLEL_SOLVE", f"{combined_coef}x + {combined_const} = 180", f"x = {x}"))
        steps_list.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="parallel_co_interior_angles",
            problem=problem,
            steps=steps_list,
            final_answer=str(x),
        )


class TriangleAngleSumGenerator(ProblemGenerator):
    """
    Generates triangle angle sum problems (angles sum to 180°).

    Op-codes used:
    - TRI_ANGLE_SETUP: Set up the triangle angles (angle1, angle2, angle3_expr)
    - TRI_ANGLE_SUM: Apply the angle sum property (equation)
    - TRI_ANGLE_SOLVE: Solve for the unknown (steps, result)
    - Z: Final answer
    """

    def generate(self) -> dict:
        """Generate a triangle angle sum problem."""
        problem_type = random.choice(['find_third', 'algebraic', 'exterior'])

        if problem_type == 'find_third':
            return self._generate_find_third()
        elif problem_type == 'algebraic':
            return self._generate_algebraic()
        else:
            return self._generate_exterior()

    def _generate_find_third(self) -> dict:
        """Generate problem: given two angles, find the third."""
        angle1 = random.randint(20, 80)
        angle2 = random.randint(20, 80)
        # Ensure valid triangle
        while angle1 + angle2 >= 170:
            angle1 = random.randint(20, 80)
            angle2 = random.randint(20, 80)

        angle3 = 180 - angle1 - angle2

        problem = f"In a triangle, two angles measure {angle1}° and {angle2}°. What is the measure of the third angle?"

        steps_list = []
        steps_list.append(step("TRI_ANGLE_SETUP", angle1, angle2, "x"))
        steps_list.append(step("TRI_ANGLE_SUM", f"{angle1} + {angle2} + x = 180"))
        steps_list.append(step("TRI_ANGLE_SOLVE", f"x = 180 - {angle1} - {angle2}", angle3))
        steps_list.append(step("Z", f"{angle3}°"))

        return dict(
            problem_id=jid(),
            operation="triangle_angle_sum",
            problem=problem,
            steps=steps_list,
            final_answer=f"{angle3}°",
        )

    def _generate_algebraic(self) -> dict:
        """Generate problem with algebraic expressions for angles."""
        x = random.randint(10, 30)

        # Generate three expressions that sum to 180
        coef1 = random.randint(1, 4)
        coef2 = random.randint(1, 4)
        coef3 = random.randint(1, 4)
        const1 = random.randint(0, 20)
        const2 = random.randint(0, 20)
        # const3 = 180 - (coef1 + coef2 + coef3)*x - const1 - const2
        const3 = 180 - (coef1 + coef2 + coef3) * x - const1 - const2

        expr1 = f"{coef1}x + {const1}" if const1 > 0 else f"{coef1}x"
        expr2 = f"{coef2}x + {const2}" if const2 > 0 else f"{coef2}x"
        expr3 = f"{coef3}x + {const3}" if const3 >= 0 else f"{coef3}x - {-const3}"

        problem = f"In a triangle, the angles measure ({expr1})°, ({expr2})°, and ({expr3})°. Find the value of x."

        steps_list = []
        steps_list.append(step("TRI_ANGLE_SETUP", expr1, expr2, expr3))
        steps_list.append(step("TRI_ANGLE_SUM", f"({expr1}) + ({expr2}) + ({expr3}) = 180"))

        total_coef = coef1 + coef2 + coef3
        total_const = const1 + const2 + const3

        steps_list.append(step("TRI_ANGLE_SOLVE", f"{total_coef}x + {total_const} = 180", f"x = {x}"))
        steps_list.append(step("Z", x))

        return dict(
            problem_id=jid(),
            operation="triangle_angle_sum_algebraic",
            problem=problem,
            steps=steps_list,
            final_answer=str(x),
        )

    def _generate_exterior(self) -> dict:
        """Generate exterior angle theorem problem."""
        # Exterior angle = sum of two non-adjacent interior angles
        angle1 = random.randint(30, 70)
        angle2 = random.randint(30, 70)
        exterior = angle1 + angle2

        problem = f"In a triangle, two interior angles measure {angle1}° and {angle2}°. What is the measure of the exterior angle at the third vertex?"

        steps_list = []
        steps_list.append(step("TRI_ANGLE_SETUP", angle1, angle2, "exterior"))
        steps_list.append(step("TRI_ANGLE_SUM", "Exterior angle = sum of remote interior angles"))
        steps_list.append(step("TRI_ANGLE_SOLVE", f"exterior = {angle1} + {angle2}", exterior))
        steps_list.append(step("Z", f"{exterior}°"))

        return dict(
            problem_id=jid(),
            operation="exterior_angle_theorem",
            problem=problem,
            steps=steps_list,
            final_answer=f"{exterior}°",
        )
