import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.cauchy_riemann_generator import CauchyRiemannGenerator
from helpers import DELIM


VERIFY_RE = re.compile(
    r"For a=(-?\d+), b=(-?\d+), c=(-?\d+), let "
    r"u=a\(x\^2-y\^2\)\+b\*x-c\*y and "
    r"v=2a\*x\*y\+c\*x\+\(b([+-]\d+)\)\*y\. "
    r"Verify the Cauchy-Riemann equations\."
)
HARMONIC_RE = re.compile(
    r"For a=(-?\d+), b=(-?\d+), c=(-?\d+), let "
    r"u=a\(x\^2-y\^2\)\+b\*x-c\*y\. Find a harmonic conjugate v "
    r"with constant 0\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def expr_text(terms):
    parts = []
    for coef, var in terms:
        if coef == 0:
            continue
        abs_coef = abs(coef)
        if var:
            body = var if abs_coef == 1 else f"{abs_coef}{var}"
        else:
            body = str(abs_coef)
        if not parts:
            parts.append(body if coef > 0 else f"-{body}")
        else:
            parts.append(f"+ {body}" if coef > 0 else f"- {body}")
    return " ".join(parts) if parts else "0"


def u_text(a, b, c):
    return expr_text([(a, "x^2"), (-a, "y^2"), (b, "x"), (-c, "y")])


def v_text(a, b, c, delta=0):
    return expr_text([(2 * a, "xy"), (c, "x"), (b + delta, "y")])


def ux_text(a, b):
    return expr_text([(2 * a, "x"), (b, "")])


def uy_text(a, c):
    return expr_text([(-2 * a, "y"), (-c, "")])


def vx_text(a, c):
    return expr_text([(2 * a, "y"), (c, "")])


def vy_text(a, b, delta=0):
    return expr_text([(2 * a, "x"), (b + delta, "")])


def parse_problem(problem):
    match = VERIFY_RE.fullmatch(problem)
    if match:
        a, b, c = map(int, match.groups()[:3])
        delta = int(match.group(4))
        return {"variant": "verify", "a": a, "b": b, "c": c,
                "delta": delta}
    match = HARMONIC_RE.fullmatch(problem)
    assert match is not None, problem
    a, b, c = map(int, match.groups())
    return {"variant": "harmonic_conjugate", "a": a, "b": b, "c": c}


def expected_verify(a, b, c, delta):
    u = u_text(a, b, c)
    v = v_text(a, b, c, delta)
    first_ok = delta == 0
    second_ok = True
    verdict = "yes" if first_ok and second_ok else "no"
    steps = [
        make_step("CR_SETUP", f"u={u}", f"v={v}"),
        make_step("PARTIAL", "u_x", ux_text(a, b)),
        make_step("PARTIAL", "u_y", uy_text(a, c)),
        make_step("PARTIAL", "v_x", vx_text(a, c)),
        make_step("PARTIAL", "v_y", vy_text(a, b, delta)),
        make_step("CHECK", "u_x = v_y", "yes" if first_ok else "no"),
        make_step("CHECK", "u_y = -v_x", "yes" if second_ok else "no"),
    ]
    answer = (f"Cauchy-Riemann = {verdict} "
              f"(u_x = v_y: {'yes' if first_ok else 'no'}; "
              f"u_y = -v_x: {'yes' if second_ok else 'no'})")
    return steps, answer


def expected_harmonic(a, b, c):
    u = u_text(a, b, c)
    v = v_text(a, b, c)
    steps = [
        make_step("HARMONIC_SETUP", f"u={u}"),
        make_step("PARTIAL", "u_x", ux_text(a, b)),
        make_step("PARTIAL", "u_y", uy_text(a, c)),
        make_step("INTEGRATE", "v_y = u_x", f"v={v} + phi(x)"),
        make_step("PARTIAL", "v_x", vx_text(a, c)),
        make_step("CHECK", "v_x = -u_y", "yes"),
    ]
    return steps, f"v = {v}"


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "verify":
        steps, answer = expected_verify(parts["a"], parts["b"], parts["c"],
                                        parts["delta"])
    else:
        steps, answer = expected_harmonic(parts["a"], parts["b"],
                                          parts["c"])
    steps.append(make_step("Z", answer))
    return steps, answer


class TestCauchyRiemannGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CauchyRiemannGenerator()

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

    def test_harmonic_conjugate_satisfies_cr(self):
        gen = CauchyRiemannGenerator("harmonic_conjugate")
        for _ in range(200):
            result = gen.generate()
            parts = parse_problem(result["problem"])
            self.assertEqual(result["final_answer"],
                             f"v = {v_text(parts['a'], parts['b'], parts['c'])}")

    def test_variants_are_available(self):
        for variant in ("verify", "harmonic_conjugate"):
            gen = CauchyRiemannGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"cauchy_riemann_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CauchyRiemannGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
