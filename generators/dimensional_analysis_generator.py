import random
from base_generator import ProblemGenerator
from helpers import step, jid


class DimensionalAnalysisGenerator(ProblemGenerator):
    """
    Performs multi-factor dimensional analysis across dosing (mg/kg), flow rates,
    pressure, and rate conversions with explicit factor-label multiplications/divisions.
    """

    def generate(self) -> dict:
        scenarios = [
            {
                "type": "dosing",
                "desc": "Medication dosing",
                "value_unit": "kg",
                "target_unit": "mg",
                "factors": [("dosage", "10 mg", "1 kg")],  # 10 mg/kg
            },
            {
                "type": "flow",
                "desc": "IV flow rate",
                "value_unit": "L/min",
                "target_unit": "mL/hr",
                "factors": [
                    ("volume", "1000 mL", "1 L"),
                    ("time", "60 min", "1 hr"),
                ],
            },
            {
                "type": "pressure",
                "desc": "Pressure conversion",
                "value_unit": "psi",
                "target_unit": "kPa",
                # 1 psi ≈ 6.9 kPa (rounded)
                "factors": [("pressure", "6.9 kPa", "1 psi")],
            },
            {
                "type": "pressure_atm",
                "desc": "Pressure conversion",
                "value_unit": "kPa",
                "target_unit": "atm",
                # 1 atm = 101.325 kPa => multiply by 1/101.325
                "factors": [("pressure", "1 atm", "101.325 kPa")],
            },
            {
                "type": "pressure_atm_to_kpa",
                "desc": "Pressure conversion",
                "value_unit": "atm",
                "target_unit": "kPa",
                "factors": [("pressure", "101.325 kPa", "1 atm")],
            },
            {
                "type": "dose_rate",
                "desc": "Dose rate conversion",
                "value_unit": "mcg/min",
                "target_unit": "mg/hr",
                # mcg -> mg (1 mg / 1000 mcg), min -> hr (60 min / 1 hr)
                "factors": [
                    ("time", "60 min", "1 hr"),
                    ("mass", "1 mg", "1000 mcg"),
                ],
            },
        ]

        scenario = random.choice(scenarios)

        base_value = random.randint(1, 5)
        if scenario["type"] == "dosing":
            value = base_value * 5  # 5,10,... keeps numbers tidy
        elif scenario["type"] in ("flow",):
            value = base_value * 2  # 2,4,... L/min
        elif scenario["type"] == "dose_rate":
            value = base_value * 10  # 10,20,... mcg/min
        else:
            value = base_value * 3  # pressure multiples

        steps = []
        running = value

        problem = f"{scenario['desc']}: Convert {value} {scenario['value_unit']} to {scenario['target_unit']}"

        for name, num, den in scenario["factors"]:
            steps.append(step("CONV_FACTOR", den, num))
            num_val = float(num.split()[0])
            den_val = float(den.split()[0])
            after_mul = running * num_val
            steps.append(step("M", running, num_val, after_mul))
            running = after_mul
            if den_val != 1:
                after_div = running / den_val
                steps.append(step("D", running, den_val, after_div))
                running = after_div

        final = round(running, 4) if "pressure" in scenario["type"] else round(running, 2)
        final_answer = f"{final} {scenario['target_unit']}"
        steps.append(step("CONV_RESULT", f"{value} {scenario['value_unit']}", final_answer))
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="dimensional_analysis",
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
