import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.gas_law_generator import GasLawGenerator
from helpers import DELIM


IDEAL_RE = re.compile(
    r"An ideal gas has pressure P=(\d+) atm, volume V=(\d+) L, and "
    r"temperature T=(\d+) K\. Use R=1 to find moles n\."
)
COMBINED_RE = re.compile(
    r"A gas changes from P1=(\d+) atm, V1=(\d+) L, T1=(\d+) K to "
    r"V2=(\d+) L and T2=(\d+) K\. Use the combined gas law to find P2\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_ideal(problem):
    pressure, volume, temperature = (
        int(value) for value in IDEAL_RE.fullmatch(problem).groups()
    )
    pv = pressure * volume
    moles = Fraction(pv, temperature)
    steps = [
        make_step("GAS_SETUP", "ideal_moles",
                  f"P={pressure}, V={volume}", f"T={temperature}, R=1"),
        make_step("GAS_FORMULA", "PV=nRT so n=PV/T"),
        make_step("M", pressure, volume, pv),
        make_step("D", pv, temperature, fraction_text(moles)),
    ]
    answer = f"n={fraction_text(moles)} mol"
    return steps, answer


def expected_combined(problem):
    p1, v1, t1, v2, t2 = (
        int(value) for value in COMBINED_RE.fullmatch(problem).groups()
    )
    p1v1 = p1 * v1
    numerator = p1v1 * t2
    denominator = t1 * v2
    p2 = Fraction(numerator, denominator)
    steps = [
        make_step("GAS_SETUP", "combined_pressure",
                  f"P1={p1}, V1={v1}, T1={t1}", f"V2={v2}, T2={t2}"),
        make_step("GAS_FORMULA", "P1*V1/T1=P2*V2/T2"),
        make_step("GAS_FORMULA", "P2=P1*V1*T2/(T1*V2)"),
        make_step("M", p1, v1, p1v1),
        make_step("M", p1v1, t2, numerator),
        make_step("M", t1, v2, denominator),
        make_step("D", numerator, denominator, fraction_text(p2)),
    ]
    answer = f"P2={fraction_text(p2)} atm"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if IDEAL_RE.fullmatch(problem):
        steps, answer = expected_ideal(problem)
    else:
        steps, answer = expected_combined(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestGasLawGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = GasLawGenerator()

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
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in GasLawGenerator.VARIANTS:
            result = GasLawGenerator(variant).generate()
            self.assertEqual(result["operation"], f"gas_law_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GasLawGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
