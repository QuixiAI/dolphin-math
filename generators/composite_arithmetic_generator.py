import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec, money
from generators.mixed_number_operation_generator import (
    to_improper, to_mixed,
)


def long_divide_steps(dividend, divisor):
    """Standard long-division steps for an exact quotient.

    Emits one BRING_DOWN / D / M / S cycle per processed digit and
    returns (steps, quotient). Assumes divisor divides dividend.
    """
    s = str(dividend)
    steps = []
    cur = 0
    quotient_digits = []
    started = False
    for ch in s:
        cur = cur * 10 + int(ch)
        steps.append(step("BRING_DOWN", ch, f"current = {cur}"))
        q = cur // divisor
        if q == 0 and not started:
            # Leading zero quotient digit: note it and continue.
            steps.append(step("D", cur, divisor, 0))
            quotient_digits.append("0")
            continue
        started = True
        prod = q * divisor
        rem = cur - prod
        steps.append(step("D", cur, divisor, q))
        steps.append(step("M", q, divisor, prod))
        steps.append(step("S", cur, prod, rem))
        quotient_digits.append(str(q))
        cur = rem
    quotient = int("".join(quotient_digits))
    return steps, quotient


class CompositeArithmeticGenerator(ProblemGenerator):
    """
    One scratchpad that chains 2-3 elementary skills, the way a real
    word problem forces several tools in sequence (A5). Each variant
    opens with a COMPOSITE_SETUP naming the plan, then works each
    sub-skill with its own established op-codes.

    Variants:
    - mean_long_division: sum a list (column A steps), then divide the
      total by the count with the long-division algorithm to get the
      mean (a whole number by construction)
    - area_mixed: area of a rectangle with mixed-number sides —
      convert to improper, multiply, simplify, convert back
    - percent_of_total: total a bill (A steps), convert a percent to a
      decimal, multiply for the tip in exact dollars and cents

    Op-codes used:
    - COMPOSITE_SETUP: the multi-skill plan
    - A / MEAN_DIV / BRING_DOWN / D / M / S (established) for the mean
    - MIX_IMPROPER / M / F / IMPROPER_TO_MIX (established) for area
    - PERCENT_TO_DEC / M (established) for the tip
    - Z: the mean, the area with units, or the dollar amount
    """

    VARIANTS = ["mean_long_division", "area_mixed", "percent_of_total"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "mean_long_division":
            count = random.choice([4, 5, 6, 8])
            mean = random.randint(13, 96)
            # Split count·mean into `count` plausible scores.
            total = count * mean
            parts = []
            remaining = total
            for i in range(count - 1):
                lo = max(0, remaining - 100 * (count - 1 - i))
                hi = min(100, remaining)
                v = random.randint(lo, hi)
                parts.append(v)
                remaining -= v
            parts.append(remaining)
            random.shuffle(parts)
            listing = ", ".join(map(str, parts))
            steps = [step("COMPOSITE_SETUP",
                          "add the scores, then divide by the count",
                          f"mean of {count} numbers")]
            run = parts[0]
            for v in parts[1:]:
                steps.append(step("A", run, v, run + v))
                run += v
            steps.append(step("MEAN_DIV", total, count,
                              f"{total} ÷ {count}"))
            div_steps, q = long_divide_steps(total, count)
            steps.extend(div_steps)
            answer = str(q)
            steps.append(step("EVAL", "mean", answer))
            problem = (f"Find the mean of these test scores: "
                       f"{listing}.")
        elif variant == "area_mixed":
            def pick():
                whole = random.randint(1, 6)
                den = random.randint(2, 8)
                num = random.randint(1, den - 1)
                return whole, num, den
            w1, n1, d1 = pick()
            w2, n2, d2 = pick()
            a_num, a_den = to_improper(w1, n1, d1)
            b_num, b_den = to_improper(w2, n2, d2)
            res_num, res_den = a_num * b_num, a_den * b_den
            frac = Fraction(res_num, res_den)
            steps = [
                step("COMPOSITE_SETUP",
                     "area = length × width with mixed numbers",
                     "convert, multiply, simplify"),
                step("MIX_IMPROPER", f"{w1} {n1}/{d1}",
                     f"{a_num}/{a_den}"),
                step("MIX_IMPROPER", f"{w2} {n2}/{d2}",
                     f"{b_num}/{b_den}"),
                step("M", f"{a_num}/{a_den}", f"{b_num}/{b_den}",
                     f"{res_num}/{res_den}"),
            ]
            simp_num, simp_den = frac.numerator, frac.denominator
            if (simp_num, simp_den) != (res_num, res_den):
                steps.append(step("F", f"{res_num}/{res_den}",
                                  f"{simp_num}/{simp_den}"))
            if simp_den == 1:
                value = str(simp_num)
            elif abs(simp_num) >= simp_den:
                whole, rem, base = to_mixed(simp_num, simp_den)
                value = f"{whole} {rem}/{base}" if rem else str(whole)
                steps.append(step("IMPROPER_TO_MIX",
                                  f"{simp_num}/{simp_den}", value))
            else:
                value = f"{simp_num}/{simp_den}"
            answer = f"{value} square feet"
            steps.append(step("EVAL", "area", answer))
            problem = (f"A rectangle measures {w1} {n1}/{d1} feet by "
                       f"{w2} {n2}/{d2} feet. Find its area.")
        else:
            pct = random.choice([5, 10, 15, 20, 25, 50])
            n_items = random.choice([2, 3, 4])
            while True:
                items = [random.randint(6, 40) for _ in range(n_items)]
                total = sum(items)
                tip = Fraction(total * pct, 100)
                if (tip * 100).denominator == 1:
                    break
            listing = ", ".join(f"${v}" for v in items)
            steps = [step("COMPOSITE_SETUP",
                          "total the bill, then take the percent",
                          "sum, percent-to-decimal, multiply")]
            run = items[0]
            for v in items[1:]:
                steps.append(step("A", run, v, run + v))
                run += v
            dec_pct = dec(Fraction(pct, 100))
            steps.append(step("PERCENT_TO_DEC", f"{pct}%", dec_pct))
            steps.append(step("M", total, dec_pct, money(tip)))
            answer = money(tip)
            steps.append(step("EVAL", "tip", answer))
            problem = (f"A bill has items costing {listing}. Leave a "
                       f"{pct}% tip on the total. How much is the tip?")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"composite_arithmetic_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            grade_level="elementary",
            difficulty=4,
        )
