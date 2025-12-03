import random
from base_generator import ProblemGenerator
from helpers import step, jid

LENGTH = [("m", "cm", 100), ("km", "m", 1000), ("ft", "in", 12)]
WEIGHT = [("kg", "g", 1000), ("lb", "oz", 16)]
TIME = [("hr", "min", 60), ("min", "sec", 60)]
MONEY = [("dollar", "cent", 100)]


class UnitConversionGenerator(ProblemGenerator):
    """Performs one-step unit conversions with factor-label style steps."""

    def generate(self) -> dict:
        category = random.choice(["length", "weight", "time", "money"])
        if category == "length":
            from_u, to_u, factor = random.choice(LENGTH)
        elif category == "weight":
            from_u, to_u, factor = random.choice(WEIGHT)
        elif category == "time":
            from_u, to_u, factor = random.choice(TIME)
        else:
            from_u, to_u, factor = random.choice(MONEY)

        value = random.randint(1, 50)
        problem = f"Convert {value} {from_u} to {to_u}"
        steps = []
        steps.append(step("CONV_FACTOR", f"1 {from_u}", f"{factor} {to_u}"))
        steps.append(step("M", value, factor, value * factor))
        steps.append(step("CONV_RESULT", f"{value} {from_u}", f"{value * factor} {to_u}"))
        steps.append(step("Z", f"{value * factor} {to_u}"))

        return dict(
            problem_id=jid(),
            operation=f"convert_{from_u}_to_{to_u}",
            problem=problem,
            steps=steps,
            final_answer=f"{value * factor} {to_u}",
        )
