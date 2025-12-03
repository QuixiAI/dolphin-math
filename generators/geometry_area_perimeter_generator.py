import random
from base_generator import ProblemGenerator
from helpers import step, jid


class GeometryAreaPerimeterGenerator(ProblemGenerator):
    """Computes perimeter and area for basic shapes with human-style steps."""

    def generate(self) -> dict:
        shape = random.choice(["rectangle", "triangle", "parallelogram", "trapezoid"])
        steps = []

        if shape == "rectangle":
            w = random.randint(2, 20)
            h = random.randint(2, 20)
            problem = f"Rectangle width {w}, height {h}: find perimeter and area"
            # Perimeter: 2*(w+h)
            s = w + h
            steps.append(step("A", w, h, s))
            perim = 2 * s
            steps.append(step("M", 2, s, perim))
            steps.append(step("PERIM", perim))
            # Area: w*h
            area = w * h
            steps.append(step("AREA", w, h, area))

        elif shape == "triangle":
            # Make perimeter simple and area integral
            base = random.choice([b for b in range(4, 20) if b % 2 == 0])
            height = random.choice([h for h in range(4, 20) if h % 2 == 0])
            side2 = random.randint(3, 15)
            side3 = random.randint(3, 15)
            problem = f"Triangle sides {base}, {side2}, {side3} with height {height} to base {base}: find perimeter and area"
            perim = base + side2 + side3
            steps.append(step("A", base, side2, base + side2))
            steps.append(step("A", base + side2, side3, perim))
            steps.append(step("PERIM", perim))
            # Area = (base * height)/2
            mult = base * height
            steps.append(step("M", base, height, mult))
            area = mult // 2
            steps.append(step("D", mult, 2, area))
            steps.append(step("AREA", area))

        elif shape == "parallelogram":
            base = random.randint(3, 15)
            side = random.randint(3, 15)
            height = random.randint(3, 12)
            problem = f"Parallelogram base {base}, side {side}, height {height}: find perimeter and area"
            perim = 2 * (base + side)
            steps.append(step("A", base, side, base + side))
            steps.append(step("M", 2, base + side, perim))
            steps.append(step("PERIM", perim))
            area = base * height
            steps.append(step("M", base, height, area))
            steps.append(step("AREA", area))

        else:  # trapezoid (isosceles)
            base1 = random.randint(4, 12)
            base2 = random.randint(4, 12)
            height = random.randint(3, 10)
            leg = random.randint(3, 10)
            problem = f"Trapezoid bases {base1}, {base2}, legs {leg}, height {height}: find perimeter and area"
            perim = base1 + base2 + 2 * leg
            steps.append(step("A", base1, base2, base1 + base2))
            steps.append(step("M", 2, leg, 2 * leg))
            steps.append(step("A", base1 + base2, 2 * leg, perim))
            steps.append(step("PERIM", perim))
            # Area = ( (b1 + b2) / 2 ) * h ; choose integers
            sum_bases = base1 + base2
            steps.append(step("A", base1, base2, sum_bases))
            half_sum = sum_bases / 2
            steps.append(step("D", sum_bases, 2, half_sum))
            area = half_sum * height
            steps.append(step("M", half_sum, height, area))
            steps.append(step("AREA", area))

        final_answer = steps[-1].split("|")[-1] if steps and steps[-1].startswith("AREA") else ""
        # Build combined final string
        perim_val = next((s.split("|")[1] for s in steps if s.startswith("PERIM")), None)
        area_val = next((s.split("|")[-1] for s in steps if s.startswith("AREA")), None)
        final_answer = f"Perimeter={perim_val}, Area={area_val}"
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=f"geometry_{shape}",
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
