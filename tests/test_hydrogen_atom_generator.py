import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.hydrogen_atom_generator import HydrogenAtomGenerator
from helpers import DELIM


ENERGY_RE = re.compile(
    r"In a hydrogen atom with R_E=(\d+) eV, an electron drops from n=(\d+) "
    r"to n=(\d+)\. Find the photon energy Delta_E\."
)
WAVELENGTH_RE = re.compile(
    r"For hydrogen with R_L=(\d+) 1/m, an electron drops from n=(\d+) to "
    r"n=(\d+)\. Use the Rydberg formula to find lambda\."
)
ION_RE = re.compile(
    r"Hydrogen has ionization constant R_E=(\d+) eV\. Find the ionization "
    r"energy from n=(\d+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def level_difference_steps(n_low, n_high):
    low_sq = n_low ** 2
    high_sq = n_high ** 2
    low_recip = Fraction(1, low_sq)
    high_recip = Fraction(1, high_sq)
    diff = low_recip - high_recip
    return [
        make_step("E", n_low, 2, low_sq),
        make_step("E", n_high, 2, high_sq),
        make_step("D", 1, low_sq, fraction_text(low_recip)),
        make_step("D", 1, high_sq, fraction_text(high_recip)),
        make_step("S", fraction_text(low_recip), fraction_text(high_recip),
                  fraction_text(diff)),
    ], diff


def expected_transition_energy(problem):
    rydberg_raw, n_high_raw, n_low_raw = ENERGY_RE.fullmatch(problem).groups()
    rydberg_energy = int(rydberg_raw)
    n_high = int(n_high_raw)
    n_low = int(n_low_raw)
    diff_steps, diff = level_difference_steps(n_low, n_high)
    energy = rydberg_energy * diff
    steps = [
        make_step("HYDROGEN_SETUP", "transition_energy",
                  f"n_low={n_low}, n_high={n_high}",
                  f"R_E={rydberg_energy} eV"),
        make_step("HYDROGEN_FORMULA",
                  "Delta_E=R_E*(1/n_low^2-1/n_high^2)"),
    ]
    steps.extend(diff_steps)
    steps.append(make_step("M", rydberg_energy, fraction_text(diff),
                           fraction_text(energy)))
    answer = f"Delta_E={fraction_text(energy)} eV"
    return steps, answer


def expected_transition_wavelength(problem):
    rydberg_raw, n_high_raw, n_low_raw = WAVELENGTH_RE.fullmatch(
        problem
    ).groups()
    rydberg_length = int(rydberg_raw)
    n_high = int(n_high_raw)
    n_low = int(n_low_raw)
    diff_steps, diff = level_difference_steps(n_low, n_high)
    inverse_lambda = rydberg_length * diff
    wavelength = Fraction(1, inverse_lambda)
    steps = [
        make_step("HYDROGEN_SETUP", "transition_wavelength",
                  f"n_low={n_low}, n_high={n_high}",
                  f"R_L={rydberg_length} 1/m"),
        make_step("HYDROGEN_FORMULA",
                  "1/lambda=R_L*(1/n_low^2-1/n_high^2)"),
    ]
    steps.extend(diff_steps)
    steps.extend([
        make_step("M", rydberg_length, fraction_text(diff),
                  fraction_text(inverse_lambda)),
        make_step("D", 1, fraction_text(inverse_lambda),
                  fraction_text(wavelength)),
    ])
    answer = f"lambda={fraction_text(wavelength)} m"
    return steps, answer


def expected_ionization(problem):
    rydberg_raw, n_raw = ION_RE.fullmatch(problem).groups()
    rydberg_energy = int(rydberg_raw)
    n = int(n_raw)
    n_sq = n ** 2
    energy = Fraction(rydberg_energy, n_sq)
    steps = [
        make_step("HYDROGEN_SETUP", "ionization_energy", f"n={n}",
                  f"R_E={rydberg_energy} eV"),
        make_step("HYDROGEN_FORMULA", "E_ion=R_E/n^2"),
        make_step("E", n, 2, n_sq),
        make_step("D", rydberg_energy, n_sq, fraction_text(energy)),
    ]
    answer = f"E_ion={fraction_text(energy)} eV"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if ENERGY_RE.fullmatch(problem):
        steps, answer = expected_transition_energy(problem)
    elif WAVELENGTH_RE.fullmatch(problem):
        steps, answer = expected_transition_wavelength(problem)
    else:
        steps, answer = expected_ionization(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestHydrogenAtomGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = HydrogenAtomGenerator()

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
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in HydrogenAtomGenerator.VARIANTS:
            result = HydrogenAtomGenerator(variant).generate()
            self.assertEqual(result["operation"], f"hydrogen_atom_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            HydrogenAtomGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
