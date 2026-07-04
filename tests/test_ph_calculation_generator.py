import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.ph_calculation_generator import PHCalculationGenerator
from helpers import DELIM


H_POWER_RE = re.compile(
    r"A solution has \[H\+\]=10\^-(\d+) M\. Find pH\."
)
OH_POWER_RE = re.compile(
    r"A solution has \[OH-\]=10\^-(\d+) M\. Find pOH and pH using "
    r"pH\+pOH=14\."
)
H_LOG_RE = re.compile(
    r"A solution has \[H\+\]=(\d+)\*10\^-(\d+) M\. Use provided "
    r"log10\(\1\)=([^ ]+) to find pH\."
)
OH_LOG_RE = re.compile(
    r"A solution has \[OH-\]=(\d+)\*10\^-(\d+) M\. Use provided "
    r"log10\(\1\)=([^ ]+) to find pOH and pH with pH\+pOH=14\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def dec(value):
    value = Fraction(value)
    num, den = value.numerator, value.denominator
    p10 = 0
    while den % 2 == 0:
        den //= 2
        num *= 5
        p10 += 1
    while den % 5 == 0:
        den //= 5
        num *= 2
        p10 += 1
    assert den == 1, value
    if p10 == 0:
        return str(num)
    s = str(abs(num)).rjust(p10 + 1, "0")
    out = f"{s[:-p10]}.{s[-p10:]}".rstrip("0").rstrip(".")
    return ("-" if num < 0 else "") + out


def expected_h_power(problem):
    exponent = int(H_POWER_RE.fullmatch(problem).group(1))
    log_h = -exponent
    ph = exponent
    steps = [
        make_step("PH_SETUP", "hydronium_power", f"[H+]=10^-{exponent}"),
        make_step("PH_FORMULA", "pH=-log10([H+])"),
        make_step("LOG_POWER", f"log10(10^-{exponent})", log_h),
        make_step("S", 0, log_h, ph),
    ]
    return steps, f"pH={ph}"


def expected_oh_power(problem):
    exponent = int(OH_POWER_RE.fullmatch(problem).group(1))
    log_oh = -exponent
    poh = exponent
    ph = 14 - poh
    steps = [
        make_step("PH_SETUP", "hydroxide_power", f"[OH-]=10^-{exponent}"),
        make_step("PH_FORMULA", "pOH=-log10([OH-]), pH=14-pOH"),
        make_step("LOG_POWER", f"log10(10^-{exponent})", log_oh),
        make_step("S", 0, log_oh, poh),
        make_step("S", 14, poh, ph),
    ]
    return steps, f"pOH={poh}; pH={ph}"


def expected_h_log(problem):
    coefficient_raw, exponent_raw, log_raw = H_LOG_RE.fullmatch(problem).groups()
    coefficient = int(coefficient_raw)
    exponent = int(exponent_raw)
    log_value = Fraction(log_raw)
    log_h = log_value - exponent
    ph = 0 - log_h
    steps = [
        make_step("PH_SETUP", "hydronium_with_log",
                  f"[H+]={coefficient}*10^-{exponent}",
                  f"log10({coefficient})={dec(log_value)}"),
        make_step("PH_FORMULA", "pH=-log10([H+])"),
        make_step(
            "LOG_PRODUCT",
            f"log10({coefficient}*10^-{exponent})=log10({coefficient})-{exponent}",
        ),
        make_step("S", dec(log_value), exponent, dec(log_h)),
        make_step("S", 0, dec(log_h), dec(ph)),
    ]
    return steps, f"pH={dec(ph)}"


def expected_oh_log(problem):
    coefficient_raw, exponent_raw, log_raw = OH_LOG_RE.fullmatch(problem).groups()
    coefficient = int(coefficient_raw)
    exponent = int(exponent_raw)
    log_value = Fraction(log_raw)
    log_oh = log_value - exponent
    poh = 0 - log_oh
    ph = 14 - poh
    steps = [
        make_step("PH_SETUP", "hydroxide_with_log",
                  f"[OH-]={coefficient}*10^-{exponent}",
                  f"log10({coefficient})={dec(log_value)}"),
        make_step("PH_FORMULA", "pOH=-log10([OH-]), pH=14-pOH"),
        make_step(
            "LOG_PRODUCT",
            f"log10({coefficient}*10^-{exponent})=log10({coefficient})-{exponent}",
        ),
        make_step("S", dec(log_value), exponent, dec(log_oh)),
        make_step("S", 0, dec(log_oh), dec(poh)),
        make_step("S", 14, dec(poh), dec(ph)),
    ]
    return steps, f"pOH={dec(poh)}; pH={dec(ph)}"


def expected_flow(example):
    problem = example["problem"]
    if H_POWER_RE.fullmatch(problem):
        steps, answer = expected_h_power(problem)
    elif OH_POWER_RE.fullmatch(problem):
        steps, answer = expected_oh_power(problem)
    elif H_LOG_RE.fullmatch(problem):
        steps, answer = expected_h_log(problem)
    elif OH_LOG_RE.fullmatch(problem):
        steps, answer = expected_oh_log(problem)
    else:
        raise AssertionError(f"unrecognized problem: {problem}")
    steps.append(make_step("Z", answer))
    return steps, answer


class TestPHCalculationGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = PHCalculationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_subtraction_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in PHCalculationGenerator.VARIANTS:
            result = PHCalculationGenerator(variant).generate()
            self.assertEqual(result["operation"], f"ph_calculation_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PHCalculationGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
