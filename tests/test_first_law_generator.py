import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.first_law_generator import FirstLawGenerator
from helpers import DELIM


ISOCHORIC_RE = re.compile(
    r"An isochoric process has heat Q=(-?\d+) J added to the gas\. Using W "
    r"as work done by the gas, find W and DeltaU\."
)
ADIABATIC_RE = re.compile(
    r"An adiabatic process has work W=(-?\d+) J done by the gas\. Using "
    r"DeltaU=Q-W, find Q and DeltaU\."
)
ISOTHERMAL_RE = re.compile(
    r"An isothermal ideal-gas process has work W=(-?\d+) J done by the gas\. "
    r"Find Q and DeltaU\."
)
ISOBARIC_RE = re.compile(
    r"An isobaric process has pressure P=(\d+) Pa, volume changes from "
    r"V1=(\d+) m\^3 to V2=(\d+) m\^3, and heat Q=(-?\d+) J\. Using "
    r"W=P\(V2-V1\) and DeltaU=Q-W, find W and DeltaU\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def expected_isochoric(problem):
    (heat_raw,) = ISOCHORIC_RE.fullmatch(problem).groups()
    heat = int(heat_raw)
    work = 0
    delta_u = heat - work
    steps = [
        make_step("FIRSTLAW_SETUP", "isochoric", f"Q={heat}", "W=0"),
        make_step("FIRSTLAW_FORMULA", "DeltaU=Q-W"),
        make_step("S", heat, work, delta_u),
    ]
    answer = f"W=0 J; DeltaU={delta_u} J"
    return steps, answer


def expected_adiabatic(problem):
    (work_raw,) = ADIABATIC_RE.fullmatch(problem).groups()
    work = int(work_raw)
    heat = 0
    delta_u = heat - work
    steps = [
        make_step("FIRSTLAW_SETUP", "adiabatic", "Q=0", f"W={work}"),
        make_step("FIRSTLAW_FORMULA", "DeltaU=Q-W"),
        make_step("S", heat, work, delta_u),
    ]
    answer = f"Q=0 J; DeltaU={delta_u} J"
    return steps, answer


def expected_isothermal(problem):
    (work_raw,) = ISOTHERMAL_RE.fullmatch(problem).groups()
    work = int(work_raw)
    heat = work
    delta_u = heat - work
    steps = [
        make_step("FIRSTLAW_SETUP", "isothermal", f"W={work}", "ideal gas"),
        make_step("FIRSTLAW_FORMULA", "isothermal ideal gas: DeltaU=0"),
        make_step("FIRSTLAW_FORMULA", "DeltaU=Q-W so Q=W"),
        make_step("S", heat, work, delta_u),
    ]
    answer = f"Q={heat} J; DeltaU=0 J"
    return steps, answer


def expected_isobaric(problem):
    pressure, v1, v2, heat = (
        int(value) for value in ISOBARIC_RE.fullmatch(problem).groups()
    )
    delta_v = v2 - v1
    work = pressure * delta_v
    delta_u = heat - work
    steps = [
        make_step("FIRSTLAW_SETUP", "isobaric",
                  f"P={pressure}, V1={v1}, V2={v2}", f"Q={heat}"),
        make_step("FIRSTLAW_FORMULA", "W=P*(V2-V1)"),
        make_step("S", v2, v1, delta_v),
        make_step("M", pressure, delta_v, work),
        make_step("FIRSTLAW_FORMULA", "DeltaU=Q-W"),
        make_step("S", heat, work, delta_u),
    ]
    answer = f"W={work} J; DeltaU={delta_u} J"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if ISOCHORIC_RE.fullmatch(problem):
        steps, answer = expected_isochoric(problem)
    elif ADIABATIC_RE.fullmatch(problem):
        steps, answer = expected_adiabatic(problem)
    elif ISOTHERMAL_RE.fullmatch(problem):
        steps, answer = expected_isothermal(problem)
    else:
        steps, answer = expected_isobaric(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestFirstLawGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = FirstLawGenerator()

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
                if fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in FirstLawGenerator.VARIANTS:
            result = FirstLawGenerator(variant).generate()
            self.assertEqual(result["operation"], f"first_law_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FirstLawGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
