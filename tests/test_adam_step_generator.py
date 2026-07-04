import math
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.adam_step_generator import AdamStepGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Perform one Adam update at t=1 with theta=([-0-9/]+), gradient "
    r"g=([-0-9]+), m0=0, v0=0, beta1=9/10, beta2=99/100, "
    r"lr=([-0-9/]+), and epsilon=0\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    theta = Fraction(match.group(1))
    gradient = int(match.group(2))
    lr = Fraction(match.group(3))
    beta1 = Fraction(9, 10)
    beta2 = Fraction(99, 100)
    epsilon = Fraction(0)
    one_minus_beta1 = 1 - beta1
    one_minus_beta2 = 1 - beta2
    beta1_m0 = beta1 * 0
    m_add = one_minus_beta1 * gradient
    m = beta1_m0 + m_add
    beta2_v0 = beta2 * 0
    grad_sq = gradient ** 2
    v_add = one_minus_beta2 * grad_sq
    v = beta2_v0 + v_add
    m_hat = m / one_minus_beta1
    v_hat = v / one_minus_beta2
    root = abs(gradient)
    denom = root + epsilon
    direction = m_hat / denom
    delta = lr * direction
    theta_new = theta - delta
    steps = [
        make_step("ADAM_SETUP", f"theta={fraction_text(theta)},g={gradient}",
                  "beta1=9/10,beta2=99/100",
                  f"lr={fraction_text(lr)},epsilon=0"),
        make_step("M", fraction_text(beta1), 0, fraction_text(beta1_m0)),
        make_step("S", 1, fraction_text(beta1),
                  fraction_text(one_minus_beta1)),
        make_step("M", fraction_text(one_minus_beta1), gradient,
                  fraction_text(m_add)),
        make_step("A", fraction_text(beta1_m0), fraction_text(m_add),
                  fraction_text(m)),
        make_step("MOMENT", "m1", fraction_text(m)),
        make_step("M", fraction_text(beta2), 0, fraction_text(beta2_v0)),
        make_step("S", 1, fraction_text(beta2),
                  fraction_text(one_minus_beta2)),
        make_step("E", gradient, 2, grad_sq),
        make_step("M", fraction_text(one_minus_beta2), grad_sq,
                  fraction_text(v_add)),
        make_step("A", fraction_text(beta2_v0), fraction_text(v_add),
                  fraction_text(v)),
        make_step("MOMENT", "v1", fraction_text(v)),
        make_step("D", fraction_text(m), fraction_text(one_minus_beta1),
                  fraction_text(m_hat)),
        make_step("BIAS_CORRECT", "m_hat", fraction_text(m_hat)),
        make_step("D", fraction_text(v), fraction_text(one_minus_beta2),
                  fraction_text(v_hat)),
        make_step("BIAS_CORRECT", "v_hat", fraction_text(v_hat)),
        make_step("ROOT", f"sqrt({fraction_text(v_hat)})", root),
        make_step("A", root, fraction_text(epsilon), fraction_text(denom)),
        make_step("D", fraction_text(m_hat), fraction_text(denom),
                  fraction_text(direction)),
        make_step("M", fraction_text(lr), fraction_text(direction),
                  fraction_text(delta)),
        make_step("S", fraction_text(theta), fraction_text(delta),
                  fraction_text(theta_new)),
        make_step("ADAM_UPDATE", "theta_new", fraction_text(theta_new)),
    ]
    answer = (
        f"m={fraction_text(m)}; v={fraction_text(v)}; "
        f"m_hat={fraction_text(m_hat)}; v_hat={fraction_text(v_hat)}; "
        f"theta_new={fraction_text(theta_new)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestAdamStepGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = AdamStepGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "adam_step_exact_t1")
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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    radicand = Fraction(fields[1][5:-1])
                    self.assertEqual(math.isqrt(radicand.numerator),
                                     int(fields[2]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
