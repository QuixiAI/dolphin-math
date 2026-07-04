import os
import random
import re
import sys
import unittest
from datetime import date, timedelta

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.calendar_arithmetic_generator import (
    CalendarArithmeticGenerator, WEEKDAYS,
)
from helpers import DELIM


def parse_date(text):
    return date.fromisoformat(text)


def oracle_answer(example):
    """A9 oracle: recompute calendar result from the prompt."""
    problem = example["problem"]
    m = re.search(r"from (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})\?", problem)
    if m and "Do not include" in problem:
        start, end = (parse_date(v) for v in m.groups())
        return f"{(end - start).days} days"

    m = re.search(
        r"(\d{4}-\d{2}-\d{2}) is a \w+\. What weekday is it after "
        r"(\d+) days",
        problem,
    )
    if m:
        start = parse_date(m.group(1))
        days = int(m.group(2))
        return WEEKDAYS[(start.weekday() + days) % 7]

    m = re.search(
        r"How many (\w+)s occur from (\d{4}-\d{2}-\d{2}) to "
        r"(\d{4}-\d{2}-\d{2}), inclusive",
        problem,
    )
    target, start_txt, end_txt = m.groups()
    start = parse_date(start_txt)
    end = parse_date(end_txt)
    count = 0
    cur = start
    while cur <= end:
        if WEEKDAYS[cur.weekday()] == target:
            count += 1
        cur += timedelta(days=1)
    word = target if count == 1 else f"{target}s"
    return f"{count} {word}"


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        code = parts[0]
        if code == "DATE_ORDINAL":
            if parse_date(parts[1]).toordinal() != int(parts[2]):
                return False
        elif code == "A":
            if int(parts[1]) + int(parts[2]) != int(parts[3]):
                return False
        elif code == "S":
            if int(parts[1]) - int(parts[2]) != int(parts[3]):
                return False
        elif code == "MOD_REDUCE":
            modulus = int(parts[2].split()[1])
            if int(parts[1]) % modulus != int(parts[3]):
                return False
        elif code == "CAL_DIVMOD":
            n = int(parts[1])
            d = int(parts[2])
            q, r = (int(v) for v in re.fullmatch(r"(\d+) R(\d+)",
                                                  parts[3]).groups())
            if divmod(n, d) != (q, r):
                return False
    return True


class TestCalendarArithmeticGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CalendarArithmeticGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_weekday_answers_valid(self):
        gen = CalendarArithmeticGenerator("weekday_after")
        for _ in range(100):
            self.assertIn(gen.generate()["final_answer"], WEEKDAYS)

    def test_count_variant_scans_remainder(self):
        gen = CalendarArithmeticGenerator("count_weekday")
        for _ in range(100):
            result = gen.generate()
            self.assertTrue(any(s.startswith(f"CAL_DIVMOD{DELIM}")
                                for s in result["steps"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            CalendarArithmeticGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
