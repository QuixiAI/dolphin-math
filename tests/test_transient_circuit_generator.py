import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.transient_circuit_generator import TransientCircuitGenerator
from helpers import DELIM


RC_RE = re.compile(
    r"An RC circuit has R=(\d+) ohm, C=(\d+) F, source Vs=(\d+) V, and "
    r"starts uncharged\. Find capacitor voltage at t=(\d+) s in exact "
    r"exponential form\."
)
RL_RE = re.compile(
    r"An RL circuit has R=(\d+) ohm, L=(\d+) H, source V=(\d+) V, and "
    r"starts with zero current\. Find current at t=(\d+) s in exact "
    r"exponential form\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def scale_expr(scale, body):
    scale = Fraction(scale)
    if scale == 1:
        return body
    if scale.denominator == 1:
        return f"{scale.numerator}*{body}"
    return f"({scale})*{body}"


def expected_rc(problem):
    resistance, capacitance, source, time = (
        int(value) for value in RC_RE.fullmatch(problem).groups()
    )
    tau = resistance * capacitance
    multiple = Fraction(time, tau)
    assert multiple.denominator == 1
    multiple = multiple.numerator
    body = f"(1-e^-{multiple})"
    voltage = scale_expr(source, body)
    steps = [
        make_step("TRANSIENT_SETUP", "rc_charging",
                  f"R={resistance}, C={capacitance}",
                  f"Vs={source}, t={time}"),
        make_step("TRANSIENT_FORMULA", "tau=R*C"),
        make_step("M", resistance, capacitance, tau),
        make_step("D", time, tau, multiple),
        make_step("TRANSIENT_FORMULA", "V_C=Vs*(1-e^(-t/tau))"),
        make_step("EXP_SUB", "t/tau", multiple, f"e^-{multiple}"),
        make_step("TRANSIENT_FORMULA", f"V_C={source}*(1-e^-{multiple})"),
    ]
    answer = f"V_C={voltage} V"
    return steps, answer


def expected_rl(problem):
    resistance, inductance, source, time = (
        int(value) for value in RL_RE.fullmatch(problem).groups()
    )
    tau = Fraction(inductance, resistance)
    assert tau.denominator == 1
    steady_current = Fraction(source, resistance)
    multiple = Fraction(time, tau.numerator)
    assert multiple.denominator == 1
    multiple = multiple.numerator
    body = f"(1-e^-{multiple})"
    current = scale_expr(steady_current, body)
    steps = [
        make_step("TRANSIENT_SETUP", "rl_rise",
                  f"R={resistance}, L={inductance}",
                  f"V={source}, t={time}"),
        make_step("TRANSIENT_FORMULA", "tau=L/R"),
        make_step("D", inductance, resistance, tau.numerator),
        make_step("TRANSIENT_FORMULA", "I_inf=V/R"),
        make_step("D", source, resistance, fraction_text(steady_current)),
        make_step("D", time, tau.numerator, multiple),
        make_step("TRANSIENT_FORMULA", "I=I_inf*(1-e^(-t/tau))"),
        make_step("EXP_SUB", "t/tau", multiple, f"e^-{multiple}"),
        make_step("TRANSIENT_FORMULA",
                  f"I={fraction_text(steady_current)}*(1-e^-{multiple})"),
    ]
    answer = f"I={current} A"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if RC_RE.fullmatch(problem):
        steps, answer = expected_rc(problem)
    else:
        steps, answer = expected_rl(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestTransientCircuitGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = TransientCircuitGenerator()

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
                elif fields[0] == "EXP_SUB":
                    self.assertEqual(fields[1], "t/tau", raw_step)
                    self.assertEqual(fields[3], f"e^-{fields[2]}", raw_step)

    def test_variants_are_available(self):
        for variant in TransientCircuitGenerator.VARIANTS:
            result = TransientCircuitGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"transient_circuit_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            TransientCircuitGenerator("bogus")

    def test_answers_stay_symbolic(self):
        for _ in range(300):
            answer = self.gen.generate()["final_answer"]
            self.assertIn("e^-", answer)
            self.assertNotRegex(answer, r"\d+\.\d+")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
