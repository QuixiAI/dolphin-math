import random
from base_generator import ProblemGenerator
from helpers import step, jid


class RateConversionGenerator(ProblemGenerator):
    """
    Converts rates like mph -> ft/s (and reverse) using factor-label steps
    with explicit numerator/denominator conversions.
    """

    def generate(self) -> dict:
        # Scenarios chosen to keep integer intermediates/finals
        scenarios = [
            dict(
                from_unit="mi/hr",
                to_unit="ft/s",
                length_factor=5280,
                time_factor=3600,
                value_mult=15,  # value * 22/15 = integer
                length_first=True,
            ),
            dict(
                from_unit="ft/s",
                to_unit="mi/hr",
                length_factor=5280,
                time_factor=3600,
                value_mult=22,  # value * 15/22 = integer
                length_first=False,  # multiply time first, then divide length
            ),
            dict(
                from_unit="km/hr",
                to_unit="m/s",
                length_factor=1000,
                time_factor=3600,
                value_mult=18,  # value * 5/18 = integer
                length_first=True,
            ),
            dict(
                from_unit="m/s",
                to_unit="km/hr",
                length_factor=1000,
                time_factor=3600,
                value_mult=5,  # value * 18/5 = integer
                length_first=False,
            ),
        ]

        scenario = random.choice(scenarios)
        base = random.randint(1, 5) * scenario["value_mult"]
        value = base
        steps = []

        def multiply(val, factor):
            product = val * factor
            steps.append(step("M", val, factor, product))
            return product

        def divide(val, divisor):
            quotient = val // divisor
            steps.append(step("D", val, divisor, quotient))
            return quotient

        # Build problem string
        problem = f"Convert {value} {scenario['from_unit']} to {scenario['to_unit']}"

        # Apply numerator/denominator conversions
        current = value
        if scenario["length_first"]:
            steps.append(step("CONV_FACTOR", f"1 {scenario['from_unit'].split('/')[0]}", f"{scenario['length_factor']} {scenario['to_unit'].split('/')[0]}"))
            current = multiply(current, scenario["length_factor"])
            steps.append(step("CONV_FACTOR", f"1 {scenario['from_unit'].split('/')[1]}", f"{scenario['time_factor']} {scenario['to_unit'].split('/')[1]}"))
            current = divide(current, scenario["time_factor"])
        else:
            steps.append(step("CONV_FACTOR", f"1 {scenario['from_unit'].split('/')[1]}", f"{scenario['time_factor']} {scenario['to_unit'].split('/')[1]}"))
            current = multiply(current, scenario["time_factor"])
            steps.append(step("CONV_FACTOR", f"1 {scenario['from_unit'].split('/')[0]}", f"{scenario['length_factor']} {scenario['to_unit'].split('/')[0]}"))
            current = divide(current, scenario["length_factor"])

        final_answer = f"{current} {scenario['to_unit']}"
        steps.append(step("CONV_RESULT", f"{value} {scenario['from_unit']}", final_answer))
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="convert_rate",
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
