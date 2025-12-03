import random
from fractions import Fraction
from decimal import Decimal, getcontext
from base_generator import ProblemGenerator
from helpers import step, jid

getcontext().prec = 10


class FractionDecimalPercentConverter(ProblemGenerator):
    """Converts between fraction, decimal, and percent with clear human steps."""

    def generate(self) -> dict:
        direction = random.choice(["frac_to_dec", "frac_to_percent", "dec_to_frac", "percent_to_dec", "percent_to_frac"])
        steps = []

        if direction == "frac_to_dec":
            num = random.randint(1, 9)
            den = random.randint(2, 12)
            frac = Fraction(num, den)
            dec = Decimal(num) / Decimal(den)
            steps.append(step("FRAC_TO_DEC", f"{num}/{den}", f"{dec.normalize():f}"))
            final_answer = f"{dec.normalize():f}"
            problem = f"Convert {num}/{den} to decimal"
            operation = "convert_frac_to_dec"

        elif direction == "frac_to_percent":
            num = random.randint(1, 9)
            den = random.randint(2, 12)
            frac = Fraction(num, den)
            percent = (Decimal(num) / Decimal(den)) * Decimal(100)
            steps.append(step("FRAC_TO_DEC", f"{num}/{den}", f"{(Decimal(num)/Decimal(den)).normalize():f}"))
            percent_str = f"{percent.quantize(Decimal('0.01'))}%"
            steps.append(step("DEC_TO_PERCENT", f"{(Decimal(num)/Decimal(den)).normalize():f}", percent_str))
            final_answer = percent_str
            problem = f"Convert {num}/{den} to percent"
            operation = "convert_frac_to_percent"

        elif direction == "dec_to_frac":
            dec_places = random.choice([1, 2])
            whole = random.randint(0, 9)
            frac_part = random.randint(1, 9)
            dec_str = f"{whole}.{frac_part}" if dec_places == 1 else f"{whole}.{frac_part}{random.randint(0,9)}"
            dec_val = Decimal(dec_str)
            frac = Fraction(dec_val)
            steps.append(step("DEC_TO_FRAC", dec_str, f"{frac.numerator}/{frac.denominator}"))
            final_answer = f"{frac.numerator}/{frac.denominator}"
            problem = f"Convert {dec_str} to fraction"
            operation = "convert_dec_to_frac"

        elif direction == "percent_to_dec":
            percent_val = random.choice([5, 10, 12.5, 20, 25, 50, 75, 80, 90])
            percent_str = f"{percent_val}%"
            dec = Decimal(str(percent_val)) / Decimal(100)
            steps.append(step("PERCENT_TO_DEC", percent_str, f"{dec:f}"))
            final_answer = f"{dec:f}"
            problem = f"Convert {percent_str} to decimal"
            operation = "convert_percent_to_dec"

        else:  # percent_to_frac
            percent_val = random.choice([5, 10, 12.5, 20, 25, 50, 75, 80, 90])
            percent_str = f"{percent_val}%"
            dec = Decimal(str(percent_val)) / Decimal(100)
            frac = Fraction(dec)
            steps.append(step("PERCENT_TO_DEC", percent_str, f"{dec:f}"))
            steps.append(step("DEC_TO_FRAC", f"{dec:f}", f"{frac.numerator}/{frac.denominator}"))
            final_answer = f"{frac.numerator}/{frac.denominator}"
            problem = f"Convert {percent_str} to fraction"
            operation = "convert_percent_to_frac"

        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
