import random
from base_generator import ProblemGenerator
from helpers import step, jid

# Base length conversions to extend into area (square) and volume (cubic)
LENGTH_BASE = [("m", "cm", 100), ("km", "m", 1000), ("ft", "in", 12)]


class MultiStepUnitConversionGenerator(ProblemGenerator):
    """
    Performs multi-step conversions for area (square units) and volume (cubic units)
    using repeated factor-label multiplication.
    """

    def generate(self) -> dict:
        from_u, to_u, factor = random.choice(LENGTH_BASE)
        dimension = random.choice(["area", "volume"])
        power = 2 if dimension == "area" else 3

        value = random.randint(1, 20)
        problem = f"Convert {value} {from_u}^{power} to {to_u}^{power}"

        steps = []
        running = value
        # Multiply by the base factor once per dimension to mirror factor-label steps
        for _ in range(power):
            steps.append(step("CONV_FACTOR", f"1 {from_u}", f"{factor} {to_u}"))
            new_running = running * factor
            steps.append(step("M", running, factor, new_running))
            running = new_running

        final_answer = f"{running} {to_u}^{power}"
        steps.append(step("CONV_RESULT", f"{value} {from_u}^{power}", final_answer))
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=f"convert_{dimension}",
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
