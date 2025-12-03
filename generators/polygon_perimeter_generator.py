import random
from base_generator import ProblemGenerator
from helpers import step, jid


class PolygonPerimeterGenerator(ProblemGenerator):
    """Computes perimeter of an n-sided polygon by summing side lengths."""

    def generate(self) -> dict:
        n_sides = random.randint(3, 8)
        sides = [random.randint(2, 15) for _ in range(n_sides)]
        steps = []

        # Start with first two sides, then accumulate the rest
        running = sides[0] + sides[1]
        steps.append(step("A", sides[0], sides[1], running))  # First addition
        for side in sides[2:]:
            new_total = running + side
            steps.append(step("A", running, side, new_total))
            running = new_total

        perim = running
        steps.append(step("PERIM", perim))
        steps.append(step("Z", str(perim)))

        sides_str = ", ".join(str(s) for s in sides)
        return dict(
            problem_id=jid(),
            operation="polygon_perimeter",
            problem=f"Find perimeter of polygon with sides: {sides_str}",
            steps=steps,
            final_answer=str(perim),
        )
