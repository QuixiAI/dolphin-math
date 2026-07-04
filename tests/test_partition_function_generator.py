import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.partition_function_generator import PartitionFunctionGenerator
from helpers import DELIM


TWO_LEVEL_RE = re.compile(
    r"A two-level system has ground degeneracy g0=(\d+), excited degeneracy "
    r"g1=(\d+), excited energy epsilon=(\d+), and Boltzmann factor b=([^ ]+) "
    r"for the excited level\. Compute Z, excited occupancy, and mean energy\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_flow(example):
    g0_raw, g1_raw, epsilon_raw, boltzmann_raw = (
        TWO_LEVEL_RE.fullmatch(example["problem"]).groups()
    )
    g0 = int(g0_raw)
    g1 = int(g1_raw)
    epsilon = int(epsilon_raw)
    boltzmann = Fraction(boltzmann_raw)
    variant = "two_level" if g0 == 1 and g1 == 1 else "degenerate_two_level"
    excited_weight = g1 * boltzmann
    partition = Fraction(g0) + excited_weight
    p_ground = Fraction(g0, 1) / partition
    p_excited = excited_weight / partition
    mean_energy = epsilon * p_excited
    steps = [
        make_step("PARTITION_SETUP", variant,
                  f"g0={g0}, g1={g1}",
                  f"epsilon={epsilon}, b={fraction_text(boltzmann)}"),
        make_step("PARTITION_FORMULA", "Z=g0+g1*b"),
        make_step("M", g1, fraction_text(boltzmann),
                  fraction_text(excited_weight)),
        make_step("A", g0, fraction_text(excited_weight),
                  fraction_text(partition)),
        make_step("D", g0, fraction_text(partition), fraction_text(p_ground)),
        make_step("D", fraction_text(excited_weight),
                  fraction_text(partition), fraction_text(p_excited)),
        make_step("PARTITION_FORMULA", "mean_energy=epsilon*p_excited"),
        make_step("M", epsilon, fraction_text(p_excited),
                  fraction_text(mean_energy)),
    ]
    answer = (
        f"Z={fraction_text(partition)}; "
        f"p_excited={fraction_text(p_excited)}; "
        f"mean_energy={fraction_text(mean_energy)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestPartitionFunctionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = PartitionFunctionGenerator()

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
        for variant in PartitionFunctionGenerator.VARIANTS:
            result = PartitionFunctionGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"partition_function_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PartitionFunctionGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
