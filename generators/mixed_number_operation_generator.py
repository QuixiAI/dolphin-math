import random
import math
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


def to_improper(whole: int, num: int, den: int):
    return whole * den + num, den


def to_mixed(num: int, den: int):
    whole = num // den
    rem = num % den
    return whole, rem, den


def lcm(a: int, b: int) -> int:
    return abs(a * b) // math.gcd(a, b)


class MixedNumberOperationGenerator(ProblemGenerator):
    """Generates mixed number operations (+, -, *, /) with step-by-step conversions."""

    def __init__(self, op_symbol: str):
        if op_symbol not in ['+', '-', '*', '/']:
            raise ValueError("op_symbol must be one of '+', '-', '*', '/'")
        self.op_symbol = op_symbol
        self.operation = f"mixed_number_{self._name_for_op()}"

    def _name_for_op(self):
        return {
            '+': "add",
            '-': "sub",
            '*': "mult",
            '/': "div",
        }[self.op_symbol]

    def _pick_mixed(self):
        whole = random.randint(0, 5)
        den = random.randint(2, 12)
        num = random.randint(1, den - 1)
        # Avoid 0/den to keep conversion meaningful
        return whole, num, den

    def generate(self) -> dict:
        w1, n1, d1 = self._pick_mixed()
        w2, n2, d2 = self._pick_mixed()

        # For subtraction, ensure first >= second to avoid negatives for now
        if self.op_symbol == '-':
            frac1 = Fraction(w1 * d1 + n1, d1)
            frac2 = Fraction(w2 * d2 + n2, d2)
            if frac1 < frac2:
                w1, n1, d1, w2, n2, d2 = w2, n2, d2, w1, n1, d1

        problem = f"{w1} {n1}/{d1} {self.op_symbol} {w2} {n2}/{d2}"
        steps = []

        # Convert to improper
        imp1_num, imp1_den = to_improper(w1, n1, d1)
        imp2_num, imp2_den = to_improper(w2, n2, d2)
        steps.append(step("MIX_IMPROPER", f"{w1} {n1}/{d1}", f"{imp1_num}/{imp1_den}"))
        steps.append(step("MIX_IMPROPER", f"{w2} {n2}/{d2}", f"{imp2_num}/{imp2_den}"))

        if self.op_symbol in ['+', '-']:
            lcd = lcm(imp1_den, imp2_den)
            steps.append(step("L", imp1_den, imp2_den, lcd))
            imp1_lcd = imp1_num * (lcd // imp1_den)
            imp2_lcd = imp2_num * (lcd // imp2_den)
            steps.append(step("C", f"{imp1_num}/{imp1_den}", lcd, f"{imp1_lcd}/{lcd}"))
            steps.append(step("C", f"{imp2_num}/{imp2_den}", lcd, f"{imp2_lcd}/{lcd}"))
            if self.op_symbol == '+':
                res_num = imp1_lcd + imp2_lcd
                steps.append(step("A", imp1_lcd, imp2_lcd, res_num))
            else:
                res_num = imp1_lcd - imp2_lcd
                steps.append(step("S", imp1_lcd, imp2_lcd, res_num))
            res_den = lcd
        elif self.op_symbol == '*':
            res_num = imp1_num * imp2_num
            res_den = imp1_den * imp2_den
            steps.append(step("M", f"{imp1_num}/{imp1_den}", f"{imp2_num}/{imp2_den}", f"{res_num}/{res_den}"))
        else:  # division
            steps.append(step("I", f"{imp2_num}/{imp2_den}", f"{imp2_den}/{imp2_num}"))
            res_num = imp1_num * imp2_den
            res_den = imp1_den * imp2_num
            steps.append(step("M", f"{imp1_num}/{imp1_den}", f"{imp2_den}/{imp2_num}", f"{res_num}/{res_den}"))

        # Simplify (always emit F for consistency)
        frac_res = Fraction(res_num, res_den)
        simp_num, simp_den = frac_res.numerator, frac_res.denominator
        steps.append(step("F", f"{res_num}/{res_den}", f"{simp_num}/{simp_den}"))

        # Convert to mixed if improper (always emit when |num| >= den)
        if abs(simp_num) >= simp_den:
            whole, rem, base_den = to_mixed(abs(simp_num), simp_den)
            if simp_num < 0:
                whole = -whole
            if rem == 0:
                final_answer = str(whole)
            else:
                final_answer = f"{whole} {rem}/{base_den}" if whole != 0 else f"{rem}/{base_den}"
            steps.append(step("IMPROPER_TO_MIX", f"{simp_num}/{simp_den}", final_answer))
        else:
            final_answer = f"{simp_num}/{simp_den}"

        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=self.operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
