import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.complex_log_generator import ComplexLogGenerator
from helpers import DELIM


LOG_RE = re.compile(
    r"Find the principal Log and all logarithms of z = (\d+) "
    r"cis\((\d+) deg\)\."
)
POWER_II = "Compute i^i using the principal logarithm."

ARG_TEXT = {
    0: "0",
    30: "pi/6",
    45: "pi/4",
    60: "pi/3",
    90: "pi/2",
    120: "2pi/3",
    135: "3pi/4",
    150: "5pi/6",
    180: "pi",
    -150: "-5pi/6",
    -135: "-3pi/4",
    -120: "-2pi/3",
    -90: "-pi/2",
    -60: "-pi/3",
    -45: "-pi/4",
    -30: "-pi/6",
}


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def principal_degrees(theta):
    return theta - 360 if theta > 180 else theta


def ln_text(radius):
    return "0" if radius == 1 else f"ln({radius})"


def principal_log_text(radius, arg):
    ln_part = ln_text(radius)
    if arg == "0":
        return ln_part
    if arg.startswith("-"):
        arg_abs = arg.lstrip("-")
        if ln_part == "0":
            return f"-i*{arg_abs}"
        return f"{ln_part} - i*{arg_abs}"
    if ln_part == "0":
        return f"i*{arg}"
    return f"{ln_part} + i*{arg}"


def multivalued_log_text(radius, arg):
    ln_part = ln_text(radius)
    angle = "2pi*k" if arg == "0" else f"{arg} + 2pi*k"
    if ln_part == "0":
        return f"i*({angle})"
    return f"{ln_part} + i*({angle})"


def parse_problem(problem):
    if problem == POWER_II:
        return {"variant": "power_ii"}
    match = LOG_RE.fullmatch(problem)
    assert match is not None, problem
    radius, theta = map(int, match.groups())
    return {"variant": "log", "radius": radius, "theta": theta}


def expected_log(radius, theta):
    principal = principal_degrees(theta)
    arg = ARG_TEXT[principal]
    steps = [
        make_step("LOG_SETUP", f"z={radius} cis({theta} deg)"),
    ]
    if theta > 180:
        steps.append(make_step("S", theta, 360, principal))
        steps.append(make_step("ANGLE_WRAP", f"{theta} deg",
                               f"{principal} deg"))
    else:
        steps.append(make_step("ARGUMENT", f"{theta} deg",
                               f"{principal} deg"))
    principal_text = principal_log_text(radius, arg)
    multivalued_text = multivalued_log_text(radius, arg)
    steps.extend([
        make_step("LOG_FORMULA", "log z = ln r + i(arg + 2pi*k)"),
        make_step("PRINCIPAL_LOG", principal_text),
        make_step("MULTIVALUED_LOG", multivalued_text, "k in Z"),
    ])
    answer = (
        f"Log(z) = {principal_text}; "
        f"log(z) = {multivalued_text}, k in Z"
    )
    return steps, answer


def expected_power_ii():
    steps = [
        make_step("POWER_SETUP", "i^i", "principal logarithm"),
        make_step("REWRITE", "i = cis(90 deg)"),
        make_step("PRINCIPAL_LOG", "Log(i) = i*pi/2"),
        make_step("REWRITE", "i^i = exp(i*Log(i))",
                  "exp(i*i*pi/2)"),
        make_step("I_SQUARE", "i^2", "-1"),
        make_step("REWRITE", "exp(-pi/2)", "e^(-pi/2)"),
    ]
    return steps, "e^(-pi/2)"


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "log":
        steps, answer = expected_log(parts["radius"], parts["theta"])
    else:
        steps, answer = expected_power_ii()
    steps.append(make_step("Z", answer))
    return steps, answer


class TestComplexLogGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ComplexLogGenerator()

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

    def test_principal_argument_range(self):
        gen = ComplexLogGenerator("log")
        for _ in range(300):
            result = gen.generate()
            parts = parse_problem(result["problem"])
            principal = principal_degrees(parts["theta"])
            self.assertGreater(principal, -180)
            self.assertLessEqual(principal, 180)
            if principal != 0:
                self.assertIn(ARG_TEXT[principal], result["final_answer"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("log", "power_ii"):
            gen = ComplexLogGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"complex_log_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ComplexLogGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
