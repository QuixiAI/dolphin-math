import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.entropy_change_generator import EntropyChangeGenerator
from helpers import DELIM


ISOTHERMAL_RE = re.compile(
    r"An ideal gas undergoes isothermal expansion with n=(\d+) mol, R=1, "
    r"V1=(\d+) L, and V2=(\d+) L\. Find DeltaS exactly\."
)
CV_RE = re.compile(
    r"An ideal gas is heated at constant volume with n=(\d+) mol, Cv=(\d+), "
    r"T1=(\d+) K, and T2=(\d+) K\. Find DeltaS exactly\."
)
MIX_RE = re.compile(
    r"Two ideal gases mix at the same temperature: nA=(\d+) mol and "
    r"nB=(\d+) mol\. With R=1, find DeltaS_mix exactly\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def log_term(coeff, arg):
    coeff = Fraction(coeff)
    if coeff == 1:
        return f"ln({arg})"
    if coeff.denominator == 1:
        return f"{coeff.numerator}*ln({arg})"
    return f"({coeff})*ln({arg})"


def expected_isothermal(problem):
    moles, v1, v2 = (
        int(value) for value in ISOTHERMAL_RE.fullmatch(problem).groups()
    )
    ratio = Fraction(v2, v1)
    assert ratio.denominator == 1
    coeff = moles
    value = log_term(coeff, ratio.numerator)
    steps = [
        make_step("ENTROPY_SETUP", "isothermal_expansion",
                  f"n={moles}, R=1", f"V1={v1}, V2={v2}"),
        make_step("ENTROPY_FORMULA", "DeltaS=nR*ln(V2/V1)"),
        make_step("D", v2, v1, ratio.numerator),
        make_step("M", moles, 1, coeff),
        make_step("LOG_TERM", coeff, f"ln({ratio.numerator})", value),
    ]
    answer = f"DeltaS={value} J/K"
    return steps, answer


def expected_cv(problem):
    moles, cv, t1, t2 = (
        int(value) for value in CV_RE.fullmatch(problem).groups()
    )
    ratio = Fraction(t2, t1)
    assert ratio.denominator == 1
    coeff = moles * cv
    value = log_term(coeff, ratio.numerator)
    steps = [
        make_step("ENTROPY_SETUP", "constant_volume_heating",
                  f"n={moles}, Cv={cv}", f"T1={t1}, T2={t2}"),
        make_step("ENTROPY_FORMULA", "DeltaS=nCv*ln(T2/T1)"),
        make_step("M", moles, cv, coeff),
        make_step("D", t2, t1, ratio.numerator),
        make_step("LOG_TERM", coeff, f"ln({ratio.numerator})", value),
    ]
    answer = f"DeltaS={value} J/K"
    return steps, answer


def expected_mix(problem):
    each_a, each_b = (int(value) for value in MIX_RE.fullmatch(problem).groups())
    assert each_a == each_b
    total = each_a + each_b
    mole_fraction = Fraction(each_a, total)
    coeff = 2 * each_a
    value = log_term(coeff, 2)
    steps = [
        make_step("ENTROPY_SETUP", "equal_gas_mixing",
                  f"nA={each_a}, nB={each_b}", "R=1"),
        make_step("ENTROPY_FORMULA", "DeltaS_mix=-sum n_i ln(x_i)"),
        make_step("A", each_a, each_b, total),
        make_step("D", each_a, total, fraction_text(mole_fraction)),
        make_step("ENTROPY_FORMULA", "-ln(1/2)=ln(2)"),
        make_step("M", 2, each_a, coeff),
        make_step("LOG_TERM", coeff, "ln(2)", value),
    ]
    answer = f"DeltaS_mix={value} J/K"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if ISOTHERMAL_RE.fullmatch(problem):
        steps, answer = expected_isothermal(problem)
    elif CV_RE.fullmatch(problem):
        steps, answer = expected_cv(problem)
    else:
        steps, answer = expected_mix(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestEntropyChangeGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = EntropyChangeGenerator()

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
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "LOG_TERM":
                    coeff = Fraction(fields[1])
                    arg = int(fields[2].removeprefix("ln(").removesuffix(")"))
                    self.assertEqual(log_term(coeff, arg), fields[3], raw_step)

    def test_variants_are_available(self):
        for variant in EntropyChangeGenerator.VARIANTS:
            result = EntropyChangeGenerator(variant).generate()
            self.assertEqual(result["operation"], f"entropy_change_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            EntropyChangeGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
