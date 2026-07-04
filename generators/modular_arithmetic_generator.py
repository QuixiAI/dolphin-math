import random

from base_generator import ProblemGenerator
from helpers import step, jid


def isbn10_check(prefix9):
    total = sum((10 - i) * int(d) for i, d in enumerate(prefix9))
    value = (-total) % 11
    return "X" if value == 10 else str(value)


def luhn_check(prefix):
    total = 0
    double = True
    rows = []
    for ch in reversed(prefix):
        digit = int(ch)
        raw = digit * 2 if double else digit
        adjusted = raw - 9 if raw > 9 else raw
        rows.append((digit, double, raw, adjusted))
        total += adjusted
        double = not double
    return (10 - total % 10) % 10, list(reversed(rows)), total


class ModularArithmeticGenerator(ProblemGenerator):
    """
    Applied modular arithmetic: clock arithmetic, ISBN-10 check digits, and
    Luhn check digits. Each variant shows the modular reduction that makes the
    procedure useful.

    Variants:
    - clock:   add hours modulo 12
    - isbn10:  solve the ISBN-10 check digit modulo 11
    - luhn:    solve a Luhn check digit modulo 10

    Op-codes used:
    - MOD_SETUP: modulus context and target
    - MOD_TERM: weighted term in a check digit sum
    - LUHN_DIGIT: Luhn digit transformation
    - A (established): running sum
    - MOD_REDUCE: reduce a value modulo m
    - MOD_SOLVE: solve for the needed residue
    - Z: final clock time or check digit
    """

    VARIANTS = ["clock", "isbn10", "luhn"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _clock(self):
        start = random.randint(1, 12)
        add = random.randint(1, 72)
        raw = start + add
        reduced = raw % 12
        answer_hour = 12 if reduced == 0 else reduced
        answer = f"{answer_hour} o'clock"
        steps = [
            step("MOD_SETUP", "12-hour clock", f"{start} + {add} hours"),
            step("A", start, add, raw),
            step("MOD_REDUCE", raw, "mod 12", reduced),
            step("MOD_SOLVE", "0 means 12 on a clock", answer),
            step("Z", answer),
        ]
        problem = (
            f"It is {start} o'clock. What time will it be after {add} "
            "hours on a 12-hour clock?"
        )
        return "clock", problem, steps, answer

    def _isbn10(self):
        prefix = "".join(str(random.randint(0, 9)) for _ in range(9))
        total = 0
        steps = [
            step("MOD_SETUP", "ISBN-10 modulus 11", f"prefix {prefix}"),
        ]
        for i, ch in enumerate(prefix):
            weight = 10 - i
            term = weight * int(ch)
            steps.append(step("MOD_TERM", f"{weight} * {ch}", term))
            if i == 0:
                total = term
            else:
                steps.append(step("A", total, term, total + term))
                total += term
        residue = total % 11
        check = isbn10_check(prefix)
        check_value = 10 if check == "X" else int(check)
        steps.extend([
            step("MOD_REDUCE", total, "mod 11", residue),
            step("MOD_SOLVE", f"d ≡ -{residue} mod 11", check),
            step("CHECK", f"{total} + {check_value}", total + check_value,
                 "multiple of 11"),
            step("Z", check),
        ])
        problem = f"Find the ISBN-10 check digit for prefix {prefix}."
        return "isbn10", problem, steps, check

    def _luhn(self):
        length = random.randint(7, 10)
        prefix = str(random.randint(1, 9)) + "".join(
            str(random.randint(0, 9)) for _ in range(length - 1)
        )
        check, rows, total = luhn_check(prefix)
        steps = [
            step("MOD_SETUP", "Luhn modulus 10", f"prefix {prefix}"),
        ]
        running = 0
        for idx, (digit, doubled, raw, adjusted) in enumerate(rows):
            action = "double" if doubled else "keep"
            steps.append(step("LUHN_DIGIT", f"digit {digit}", action,
                              f"{raw} -> {adjusted}"))
            if idx == 0:
                running = adjusted
            else:
                steps.append(step("A", running, adjusted, running + adjusted))
                running += adjusted
        residue = total % 10
        steps.extend([
            step("MOD_REDUCE", total, "mod 10", residue),
            step("MOD_SOLVE", f"d ≡ -{residue} mod 10", check),
            step("CHECK", f"{total} + {check}", total + check,
                 "multiple of 10"),
            step("Z", str(check)),
        ])
        problem = f"Find the Luhn check digit for prefix {prefix}."
        return "luhn", problem, steps, str(check)

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "clock":
            op_suffix, problem, steps, answer = self._clock()
        elif variant == "isbn10":
            op_suffix, problem, steps, answer = self._isbn10()
        else:
            op_suffix, problem, steps, answer = self._luhn()

        return dict(
            problem_id=jid(),
            operation=f"modular_arithmetic_{op_suffix}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
