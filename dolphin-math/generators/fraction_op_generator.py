import random
import math
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid, DELIM

class FractionOpGenerator(ProblemGenerator):
    """Generates fraction arithmetic problems (+, -, *, /)."""

    def __init__(self, op_symbol: str):
        if op_symbol not in ['+', '-', '*', '/']:
            raise ValueError("op_symbol must be '+', '-', '*', or '/'")
        self.op_symbol = op_symbol
        op_map = {'+':'add','-':'sub','*':'mul','/':'div'}
        self.op_name = f"fraction_{op_map[op_symbol]}" # Perform lookup outside f-string braces

    def generate(self) -> dict:
        n1, d1 = random.randint(1, 9), random.randint(2, 9)
        n2, d2 = random.randint(1, 9), random.randint(2, 9)
        # Ensure non-zero denominator for division's second operand (n2/d2 -> d2/n2)
        if self.op_symbol == '/' and n2 == 0:
             n2 = random.randint(1, 9) # Ensure n2 is non-zero for inversion

        f1, f2 = Fraction(n1, d1), Fraction(n2, d2)
        steps = []
        res = None
        problem = f"{f1} {self.op_symbol} {f2}"

        if self.op_symbol in "+-":
            d1_s, d2_s = f1.denominator, f2.denominator
            try:
                lcd = math.lcm(d1_s, d2_s)
            except AttributeError: # Fallback for Python < 3.9
                lcd = (d1_s * d2_s) // math.gcd(d1_s, d2_s)

            if d1_s != d2_s:
                steps.append(step("L", d1_s, d2_s, lcd)) # Find LCD using simplified denominators
            n1c, n2c = f1.numerator * (lcd // d1_s), f2.numerator * (lcd // d2_s) # Converted numerators
            if d1_s != lcd: steps.append(step("C", str(f1), lcd, f"{n1c}/{lcd}")) # Convert f1
            if d2_s != lcd: steps.append(step("C", str(f2), lcd, f"{n2c}/{lcd}")) # Convert f2
            out_num = n1c + n2c if self.op_symbol == "+" else n1c - n2c
            steps.append(step("A" if self.op_symbol == "+" else "S", n1c, n2c, out_num)) # Add/Sub numerators
            res = Fraction(out_num, lcd)
            out_den = lcd # Denominator before simplification

        elif self.op_symbol == "*":
            # Use actual numerators/denominators from Fraction objects (which may have auto-simplified)
            num1, den1 = f1.numerator, f1.denominator
            num2, den2 = f2.numerator, f2.denominator
            out_num, out_den = num1 * num2, den1 * den2
            steps += [step("M", num1, num2, out_num), step("M", den1, den2, out_den)] # Multiply numerators/denominators
            res = Fraction(out_num, out_den)
            # lcd = out_den # Not really lcd, but denominator before simplification

        else: # division '/'
            if n2 == 0: # Should be caught by earlier check, but safeguard
                return self.generate() # Retry if somehow n2 is 0
            inv = Fraction(d2, n2)
            # Show the fully inverted fraction string
            inv_str = f"{inv.numerator}/{inv.denominator}"
            steps.append(step("I", str(f2), inv_str)) # Invert divisor
            out_num, out_den = n1 * inv.numerator, d1 * inv.denominator # Use inverted parts
            # Show the correct multiplication steps
            steps += [step("M", n1, inv.numerator, out_num), step("M", d1, inv.denominator, out_den)] # Multiply
            res = Fraction(out_num, out_den)
            # out_den is already the correct denominator before simplification

        final_answer_str = str(res)
        # Determine pre-simplification string based on operation (using out_den)
        pre_simp_str = f"{out_num}/{out_den}"


        # Add simplification step if needed
        if final_answer_str != pre_simp_str and '/' in pre_simp_str:
            steps.append(step("F", pre_simp_str, final_answer_str)) # Simplify fraction

        steps.append(step("Z", final_answer_str)) # Final answer step

        return dict(
            problem_id=jid(),
            operation=self.op_name,
            problem=problem,
            steps=steps,
            final_answer=final_answer_str
        )
