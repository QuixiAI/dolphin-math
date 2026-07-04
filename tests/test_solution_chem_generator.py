import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.solution_chem_generator import SolutionChemGenerator
from helpers import DELIM


FINAL_RE = re.compile(
    r"A dilution uses stock molarity M1=([^ ]+) M and stock volume V1=(\d+) "
    r"mL, diluted to final volume V2=(\d+) mL\. Find final molarity M2\."
)
STOCK_RE = re.compile(
    r"A stock solution has molarity M1=([^ ]+) M\. Prepare V2=(\d+) mL at "
    r"M2=([^ ]+) M\. Find stock volume V1\."
)
MIX_RE = re.compile(
    r"Mix Va=(\d+) mL of Ma=([^ ]+) M solution with Vb=(\d+) mL of "
    r"Mb=([^ ]+) M solution\. Find final molarity M_final\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_final(problem):
    m1_raw, v1_raw, v2_raw = FINAL_RE.fullmatch(problem).groups()
    m1 = Fraction(m1_raw)
    v1 = int(v1_raw)
    v2 = int(v2_raw)
    amount_units = m1 * v1
    m2 = amount_units / v2
    steps = [
        make_step("SOLUTION_SETUP", "dilution_final_molarity",
                  f"M1={fraction_text(m1)}, V1={v1}", f"V2={v2}"),
        make_step("SOLUTION_FORMULA", "M1*V1=M2*V2"),
        make_step("M", fraction_text(m1), v1, fraction_text(amount_units)),
        make_step("D", fraction_text(amount_units), v2, fraction_text(m2)),
    ]
    answer = f"M2={fraction_text(m2)} M"
    return steps, answer


def expected_stock(problem):
    m1_raw, v2_raw, m2_raw = STOCK_RE.fullmatch(problem).groups()
    m1 = Fraction(m1_raw)
    v2 = int(v2_raw)
    m2 = Fraction(m2_raw)
    amount_units = m2 * v2
    v1 = amount_units / m1
    steps = [
        make_step("SOLUTION_SETUP", "dilution_stock_volume",
                  f"M1={fraction_text(m1)}", f"M2={fraction_text(m2)}, V2={v2}"),
        make_step("SOLUTION_FORMULA", "M1*V1=M2*V2"),
        make_step("M", fraction_text(m2), v2, fraction_text(amount_units)),
        make_step("D", fraction_text(amount_units), fraction_text(m1),
                  fraction_text(v1)),
    ]
    answer = f"V1={fraction_text(v1)} mL"
    return steps, answer


def expected_mix(problem):
    va_raw, ma_raw, vb_raw, mb_raw = MIX_RE.fullmatch(problem).groups()
    va = int(va_raw)
    ma = Fraction(ma_raw)
    vb = int(vb_raw)
    mb = Fraction(mb_raw)
    amount_a = ma * va
    amount_b = mb * vb
    total_amount = amount_a + amount_b
    total_volume = va + vb
    final_molarity = total_amount / total_volume
    steps = [
        make_step("SOLUTION_SETUP", "mixing_molarity",
                  f"Ma={fraction_text(ma)}, Va={va}",
                  f"Mb={fraction_text(mb)}, Vb={vb}"),
        make_step("SOLUTION_FORMULA",
                  "M_final=(Ma*Va+Mb*Vb)/(Va+Vb)"),
        make_step("M", fraction_text(ma), va, fraction_text(amount_a)),
        make_step("M", fraction_text(mb), vb, fraction_text(amount_b)),
        make_step("A", fraction_text(amount_a), fraction_text(amount_b),
                  fraction_text(total_amount)),
        make_step("A", va, vb, total_volume),
        make_step("D", fraction_text(total_amount), total_volume,
                  fraction_text(final_molarity)),
    ]
    answer = f"M_final={fraction_text(final_molarity)} M"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if FINAL_RE.fullmatch(problem):
        steps, answer = expected_final(problem)
    elif STOCK_RE.fullmatch(problem):
        steps, answer = expected_stock(problem)
    elif MIX_RE.fullmatch(problem):
        steps, answer = expected_mix(problem)
    else:
        raise AssertionError(f"unrecognized problem: {problem}")
    steps.append(make_step("Z", answer))
    return steps, answer


class TestSolutionChemGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SolutionChemGenerator()

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

    def test_variants_are_available(self):
        for variant in SolutionChemGenerator.VARIANTS:
            result = SolutionChemGenerator(variant).generate()
            self.assertEqual(result["operation"], f"solution_chem_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SolutionChemGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
