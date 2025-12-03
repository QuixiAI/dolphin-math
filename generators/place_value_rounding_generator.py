import random
from base_generator import ProblemGenerator
from helpers import step, jid


class PlaceValueRoundingGenerator(ProblemGenerator):
    """Rounds whole numbers or decimals to a specified place with digit inspection steps."""

    def generate(self) -> dict:
        mode = random.choice(["whole", "decimal"])
        if mode == "whole":
            number = random.randint(100, 99999)
            target = random.choice([10, 100, 1000])
            operation = f"round_to_{target}"
            problem = f"Round {number} to the nearest {target}"
            remainder = number % target
            neighbor_flag = remainder >= target / 2
            steps = []
            steps.append(step("ROUND_CHECK", number, target, ">=5" if neighbor_flag else "<5"))
            base = (number // target) * target
            rounded = base + (target if neighbor_flag else 0)
            steps.append(step("ROUND_RESULT", str(number), str(rounded)))
            steps.append(step("Z", str(rounded)))
            return dict(
                problem_id=jid(),
                operation=operation,
                problem=problem,
                steps=steps,
                final_answer=str(rounded),
            )
        else:
            # decimal rounding to tenths or hundredths
            whole = random.randint(1, 99)
            frac1 = random.randint(0, 9)
            frac2 = random.randint(0, 9)
            number = float(f"{whole}.{frac1}{frac2}")
            target_place = random.choice(["tenth", "hundredth"])
            target_map = {"tenth": 1, "hundredth": 2}
            place = target_map[target_place]
            operation = f"round_to_{target_place}"
            problem = f"Round {number} to the nearest {target_place}"
            # Work with string digits
            num_str = f"{number:.2f}"
            digits = [d for d in num_str if d.isdigit()]
            target_idx = len(str(whole)) + place - 1
            neighbor_idx = target_idx + 1
            target_digit = int(digits[target_idx])
            neighbor = int(digits[neighbor_idx]) if neighbor_idx < len(digits) else 0

            steps = []
            steps.append(step("ROUND_CHECK", target_digit, neighbor, ">=5" if neighbor >= 5 else "<5"))
            rounded_val = round(number, place)
            rounded_str = f"{rounded_val:.{place}f}"
            steps.append(step("ROUND_RESULT", num_str, rounded_str))
            steps.append(step("Z", rounded_str))

            return dict(
                problem_id=jid(),
                operation=operation,
                problem=problem,
                steps=steps,
                final_answer=rounded_str,
            )
