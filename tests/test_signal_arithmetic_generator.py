import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.signal_arithmetic_generator import SignalArithmeticGenerator
from helpers import DELIM


NYQUIST_RE = re.compile(
    r"For a signal with maximum frequency (\d+) Hz sampled at (\d+) Hz, "
    r"compute the Nyquist rate and sampling margin\."
)
DB_RE = re.compile(
    r"For a power ratio P2/P1=([^,]+), use supplied log10\(P2/P1\)=(-?\d+) "
    r"to compute gain in dB\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_nyquist(problem):
    f_max, sample_rate = (
        int(value) for value in NYQUIST_RE.fullmatch(problem).groups()
    )
    nyquist = 2 * f_max
    margin = sample_rate - nyquist
    status = "above Nyquist" if margin >= 0 else "below Nyquist"
    steps = [
        make_step("SIGNAL_SETUP", "sampling", f"f_max={f_max} Hz",
                  f"f_s={sample_rate} Hz"),
        make_step("NYQUIST", "required rate = 2*f_max"),
        make_step("M", 2, f_max, nyquist),
        make_step("S", sample_rate, nyquist, margin),
        make_step("CHECK", f"margin={margin} Hz", status),
    ]
    answer = f"Nyquist rate={nyquist} Hz; margin={margin} Hz; {status}"
    return steps, answer


def expected_db(problem):
    ratio_raw, log_raw = DB_RE.fullmatch(problem).groups()
    ratio = Fraction(ratio_raw)
    log_value = int(log_raw)
    db_value = 10 * log_value
    steps = [
        make_step("SIGNAL_SETUP", "dB power ratio",
                  f"P2/P1={fraction_text(ratio)}"),
        make_step("DB_FORMULA", "G_dB=10*log10(P2/P1)"),
        make_step("LOG_SUPPLIED", f"log10({fraction_text(ratio)})",
                  log_value),
        make_step("M", 10, log_value, db_value),
        make_step("CHECK", "positive is gain, negative is loss",
                  f"{db_value} dB"),
    ]
    answer = f"G={db_value} dB"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if NYQUIST_RE.fullmatch(problem):
        steps, answer = expected_nyquist(problem)
    else:
        steps, answer = expected_db(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestSignalArithmeticGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SignalArithmeticGenerator()

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

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in SignalArithmeticGenerator.VARIANTS:
            result = SignalArithmeticGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"signal_arithmetic_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SignalArithmeticGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
