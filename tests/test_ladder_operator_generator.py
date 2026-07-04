import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.ladder_operator_generator import LadderOperatorGenerator
from helpers import DELIM


SINGLE_RE = re.compile(
    r"For harmonic oscillator state ket(\d+) with hbar=(\d+) and "
    r"omega=(\d+), apply (a|adag) once and compute the new energy\."
)
NUMBER_RE = re.compile(
    r"For harmonic oscillator state ket(\d+) with hbar=(\d+) and "
    r"omega=(\d+), compute N=adag\*a and E_(\d+)\."
)
COMM_RE = re.compile(
    r"For harmonic oscillator state ket(\d+) with hbar=(\d+) and "
    r"omega=(\d+), compare a\*adag and adag\*a, then compute E_(\d+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def ket(n):
    return f"ket{n}"


def sqrt_text(value):
    if value == 0:
        return "0"
    if value == 1:
        return "1"
    return f"sqrt({value})"


def sqrt_ket(coeff, n):
    root = sqrt_text(coeff)
    if root == "0":
        return "0"
    if root == "1":
        return ket(n)
    return f"{root} {ket(n)}"


def scaled_ket(coeff, n):
    if coeff == 0:
        return "0"
    if coeff == 1:
        return ket(n)
    if coeff == -1:
        return f"-{ket(n)}"
    return f"{coeff} {ket(n)}"


def rule_steps(variant, n, hbar, omega):
    return [
        make_step("LADDER_SETUP", variant, f"state={ket(n)}",
                  f"hbar={hbar}, omega={omega}"),
        make_step("LADDER_RULE", "a ketn=sqrt(n) ket(n-1)",
                  "adag ketn=sqrt(n+1) ket(n+1)"),
    ]


def energy_steps(n, hbar, omega):
    two_n = 2 * n
    odd = two_n + 1
    hbar_omega = hbar * omega
    numerator = hbar_omega * odd
    energy = Fraction(numerator, 2)
    steps = [
        make_step("M", 2, n, two_n),
        make_step("A", two_n, 1, odd),
        make_step("M", hbar, omega, hbar_omega),
        make_step("M", hbar_omega, odd, numerator),
        make_step("D", numerator, 2, fraction_text(energy)),
        make_step("ENERGY_LEVEL", f"E_{n}=hbar*omega*(n+1/2)",
                  fraction_text(energy)),
    ]
    return steps, energy


def expected_single(n, hbar, omega, operator):
    if operator == "a":
        new_n = n - 1
        coeff = n
        move_step = make_step("S", n, 1, new_n)
        applied = sqrt_ket(coeff, new_n)
    else:
        new_n = n + 1
        coeff = new_n
        move_step = make_step("A", n, 1, new_n)
        applied = sqrt_ket(coeff, new_n)
    steps = rule_steps("single_step_energy", n, hbar, omega)
    steps.extend([
        move_step,
        make_step("LADDER_APPLY", f"{operator} {ket(n)}", applied),
    ])
    e_steps, energy = energy_steps(new_n, hbar, omega)
    steps.extend(e_steps)
    answer = (
        f"{operator} {ket(n)}={applied}; "
        f"E_{new_n}={fraction_text(energy)}"
    )
    return steps, answer


def expected_number(n, hbar, omega):
    lowered = sqrt_ket(n, n - 1)
    product = n * n
    steps = rule_steps("number_energy", n, hbar, omega)
    steps.extend([
        make_step("LADDER_APPLY", f"a {ket(n)}", lowered),
        make_step("LADDER_APPLY", f"adag {lowered}",
                  f"sqrt({n})*sqrt({n}) {ket(n)}"),
        make_step("M", n, n, product),
        make_step("ROOT", product, n),
        make_step("NUMBER_OPERATOR", f"N {ket(n)}", scaled_ket(n, n)),
    ])
    e_steps, energy = energy_steps(n, hbar, omega)
    steps.extend(e_steps)
    answer = f"N {ket(n)}={scaled_ket(n, n)}; E_{n}={fraction_text(energy)}"
    return steps, answer


def expected_commutator(n, hbar, omega):
    up_n = n + 1
    raised = sqrt_ket(up_n, up_n)
    lowered = sqrt_ket(n, n - 1)
    diff = up_n - n
    steps = rule_steps("commutator_energy", n, hbar, omega)
    steps.extend([
        make_step("A", n, 1, up_n),
        make_step("LADDER_APPLY", f"adag {ket(n)}", raised),
        make_step("LADDER_APPLY", f"a {raised}",
                  f"sqrt({up_n})*sqrt({up_n}) {ket(n)}"),
        make_step("M", up_n, up_n, up_n * up_n),
        make_step("ROOT", up_n * up_n, up_n),
        make_step("LADDER_APPLY", f"a {ket(n)}", lowered),
        make_step("LADDER_APPLY", f"adag {lowered}",
                  f"sqrt({n})*sqrt({n}) {ket(n)}"),
        make_step("M", n, n, n * n),
        make_step("ROOT", n * n, n),
        make_step("S", up_n, n, diff),
        make_step("LADDER_COMM", "[a,adag] ketn", scaled_ket(diff, n)),
        make_step("CHECK", "identity", "[a,adag]=1", "matches ketn"),
    ])
    e_steps, energy = energy_steps(n, hbar, omega)
    steps.extend(e_steps)
    answer = f"[a,adag] {ket(n)}={scaled_ket(diff, n)}; E_{n}={fraction_text(energy)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    match = SINGLE_RE.fullmatch(problem)
    if match:
        n, hbar, omega = (int(value) for value in match.groups()[:3])
        steps, answer = expected_single(n, hbar, omega, match.group(4))
    else:
        match = NUMBER_RE.fullmatch(problem)
        if match:
            n, hbar, omega, label_n = (
                int(value) for value in match.groups()
            )
            assert n == label_n
            steps, answer = expected_number(n, hbar, omega)
        else:
            match = COMM_RE.fullmatch(problem)
            assert match is not None, problem
            n, hbar, omega, label_n = (
                int(value) for value in match.groups()
            )
            assert n == label_n
            steps, answer = expected_commutator(n, hbar, omega)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestLadderOperatorGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = LadderOperatorGenerator()

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
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    self.assertEqual(int(fields[2]) ** 2,
                                     int(fields[1]), raw_step)

    def test_variants_are_available(self):
        for variant in LadderOperatorGenerator.VARIANTS:
            result = LadderOperatorGenerator(variant).generate()
            self.assertEqual(result["operation"], f"ladder_operator_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            LadderOperatorGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
