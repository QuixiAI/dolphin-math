import random
from datetime import date, timedelta

from base_generator import ProblemGenerator
from helpers import step, jid


WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"]


class CalendarArithmeticGenerator(ProblemGenerator):
    """
    Calendar arithmetic with explicit day counts and modulo-7 weekday logic:
    days between dates, weekday after an offset, and counting a weekday in an
    inclusive date range.

    Variants:
    - days_between
    - weekday_after
    - count_weekday

    Op-codes used:
    - CAL_SETUP: dates and target
    - DATE_ORDINAL: date converted to ordinal day number
    - CAL_DIVMOD: divide a day count by 7
    - MOD_REDUCE: reduce weekday index modulo 7
    - WEEKDAY_SCAN: inspect leftover days after full weeks
    - A / S (established): arithmetic
    - Z: final day count or weekday
    """

    VARIANTS = ["days_between", "weekday_after", "count_weekday"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _random_date():
        start = date(2024, 1, 1)
        return start + timedelta(days=random.randint(0, 5 * 365))

    def _days_between(self):
        start = self._random_date()
        delta = random.randint(1, 180)
        end = start + timedelta(days=delta)
        answer = f"{delta} days"
        steps = [
            step("CAL_SETUP", f"start {start.isoformat()}",
                 f"end {end.isoformat()}", "days between"),
            step("DATE_ORDINAL", start.isoformat(), start.toordinal()),
            step("DATE_ORDINAL", end.isoformat(), end.toordinal()),
            step("S", end.toordinal(), start.toordinal(), delta),
            step("Z", answer),
        ]
        problem = (
            f"How many days are from {start.isoformat()} to "
            f"{end.isoformat()}? Do not include the start date."
        )
        return "days_between", problem, steps, answer

    def _weekday_after(self):
        start = self._random_date()
        days = random.randint(1, 120)
        start_idx = start.weekday()
        raw = start_idx + days
        end_idx = raw % 7
        answer = WEEKDAYS[end_idx]
        steps = [
            step("CAL_SETUP", start.isoformat(),
                 f"{WEEKDAYS[start_idx]}, offset {days} days", "weekday"),
            step("A", start_idx, days, raw),
            step("MOD_REDUCE", raw, "mod 7", end_idx),
            step("WEEKDAY_SCAN", f"index {end_idx}", answer),
            step("Z", answer),
        ]
        problem = (
            f"{start.isoformat()} is a {WEEKDAYS[start_idx]}. What weekday "
            f"is it after {days} days?"
        )
        return "weekday_after", problem, steps, answer

    def _count_weekday(self):
        start = self._random_date()
        length = random.randint(7, 120)
        end = start + timedelta(days=length - 1)
        target_idx = random.randint(0, 6)
        target = WEEKDAYS[target_idx]
        full_weeks, remainder = divmod(length, 7)
        extra = 0
        steps = [
            step("CAL_SETUP", f"{start.isoformat()} through {end.isoformat()}",
                 f"count {target}", "inclusive"),
            step("S", end.toordinal(), start.toordinal(), length - 1),
            step("A", length - 1, 1, length),
            step("CAL_DIVMOD", length, 7, f"{full_weeks} R{remainder}"),
        ]
        for offset in range(remainder):
            cur_idx = (start.weekday() + offset) % 7
            cur_day = WEEKDAYS[cur_idx]
            hit = 1 if cur_idx == target_idx else 0
            extra += hit
            steps.append(step("WEEKDAY_SCAN", f"extra day {offset + 1}",
                              cur_day, f"hit {hit}"))
        count = full_weeks + extra
        target_word = target if count == 1 else f"{target}s"
        steps.extend([
            step("A", full_weeks, extra, count),
            step("Z", f"{count} {target_word}"),
        ])
        problem = (
            f"How many {target}s occur from {start.isoformat()} to "
            f"{end.isoformat()}, inclusive?"
        )
        return "count_weekday", problem, steps, f"{count} {target_word}"

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "days_between":
            op_suffix, problem, steps, answer = self._days_between()
        elif variant == "weekday_after":
            op_suffix, problem, steps, answer = self._weekday_after()
        else:
            op_suffix, problem, steps, answer = self._count_weekday()

        return dict(
            problem_id=jid(),
            operation=f"calendar_arithmetic_{op_suffix}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
