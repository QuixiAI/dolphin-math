import random
from base_generator import ProblemGenerator
from helpers import step, jid


class TemperatureConversionGenerator(ProblemGenerator):
    """
    Converts between Fahrenheit, Celsius, and Kelvin using explicit add/subtract and multiply/divide steps.
    """

    def generate(self) -> dict:
        scenarios = [
            ("F", "C"),
            ("C", "F"),
            ("C", "K"),
            ("K", "C"),
            ("F", "K"),
            ("K", "F"),
        ]
        from_unit, to_unit = random.choice(scenarios)

        # Keep values reasonable and allow negative Celsius/Fahrenheit
        value = random.randint(-40, 212)
        steps = []

        def add(x, y):
            res = x + y
            steps.append(step("A", x, y, res))
            return res

        def sub(x, y):
            res = x - y
            steps.append(step("S", x, y, res))
            return res

        def mul(x, y):
            res = x * y
            steps.append(step("M", x, y, res))
            return res

        def div(x, y):
            res = x // y if x % y == 0 else x / y
            steps.append(step("D", x, y, res))
            return res

        current = value
        if from_unit == "F" and to_unit == "C":
            current = sub(current, 32)
            current = mul(5, current)
            current = div(current, 9)
        elif from_unit == "C" and to_unit == "F":
            current = mul(9, current)
            current = div(current, 5)
            current = add(current, 32)
        elif from_unit == "C" and to_unit == "K":
            current = add(current, 273.15)
        elif from_unit == "K" and to_unit == "C":
            current = sub(current, 273.15)
        elif from_unit == "F" and to_unit == "K":
            current = sub(current, 32)
            current = mul(5, current)
            current = div(current, 9)
            current = add(current, 273.15)
        else:  # K to F
            current = sub(current, 273.15)
            current = mul(9, current)
            current = div(current, 5)
            current = add(current, 32)

        if isinstance(current, float):
            current = round(current, 2)

        final_answer = f"{current} {to_unit}"
        problem = f"Convert {value} {from_unit} to {to_unit}"
        steps.append(step("CONV_RESULT", f"{value} {from_unit}", final_answer))
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="convert_temperature",
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
