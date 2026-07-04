import ast
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.backprop_generator import BackpropGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For a 2-2-1 ReLU network with x=(\([^)]+\)), y=(-?\d+), "
    r"eta=([^,]+), W1=(\[\[.*?\]\]), b1=(\([^)]+\)), "
    r"v=(\([^)]+\)), c=(-?\d+)\. Do one SGD backprop step using "
    r"L=1/2\*\(y_hat-y\)\^2\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def vector_text(values):
    return "(" + ",".join(fraction_text(value) for value in values) + ")"


def matrix_text(matrix):
    rows = ["[" + ",".join(fraction_text(value) for value in row) + "]"
            for row in matrix]
    return "[" + ", ".join(rows) + "]"


def relu(value):
    value = Fraction(value)
    return value if value > 0 else Fraction(0)


def relu_derivative(value):
    return 1 if value > 0 else 0


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    if not match:
        raise AssertionError(problem)
    x_values = [Fraction(value) for value in ast.literal_eval(match.group(1))]
    target = Fraction(match.group(2))
    eta = Fraction(match.group(3))
    w1 = [
        [Fraction(value) for value in row]
        for row in ast.literal_eval(match.group(4))
    ]
    b1 = [Fraction(value) for value in ast.literal_eval(match.group(5))]
    v = [Fraction(value) for value in ast.literal_eval(match.group(6))]
    c = Fraction(match.group(7))
    return x_values, target, eta, w1, b1, v, c


def append_update(steps, eta, old_value, gradient):
    scaled = eta * gradient
    new_value = old_value - scaled
    steps.append(make_step("M", fraction_text(eta), fraction_text(gradient),
                           fraction_text(scaled)))
    steps.append(make_step("S", fraction_text(old_value),
                           fraction_text(scaled), fraction_text(new_value)))
    return new_value


def expected_flow(example):
    x_values, target, eta, w1, b1, v, c = parse_problem(example["problem"])
    steps = [
        make_step("BACKPROP_SETUP", f"x={vector_text(x_values)}",
                  f"y={fraction_text(target)}", f"eta={fraction_text(eta)}"),
        make_step("PARAMS", f"W1={matrix_text(w1)}",
                  f"b1={vector_text(b1)}",
                  f"v={vector_text(v)}, c={fraction_text(c)}"),
    ]

    hidden = []
    relu_primes = []
    for row in range(2):
        term0 = w1[row][0] * x_values[0]
        term1 = w1[row][1] * x_values[1]
        partial = term0 + term1
        pre_value = partial + b1[row]
        activation = relu(pre_value)
        derivative = relu_derivative(pre_value)
        steps.extend([
            make_step("M", fraction_text(w1[row][0]),
                      fraction_text(x_values[0]), fraction_text(term0)),
            make_step("M", fraction_text(w1[row][1]),
                      fraction_text(x_values[1]), fraction_text(term1)),
            make_step("A", fraction_text(term0), fraction_text(term1),
                      fraction_text(partial)),
            make_step("A", fraction_text(partial), fraction_text(b1[row]),
                      fraction_text(pre_value)),
            make_step("HIDDEN_PRE", f"h{row + 1}",
                      f"z={fraction_text(pre_value)}"),
            make_step("RELU", f"z={fraction_text(pre_value)}",
                      f"h={fraction_text(activation)}",
                      f"deriv={derivative}"),
        ])
        hidden.append(activation)
        relu_primes.append(derivative)

    out_term0 = v[0] * hidden[0]
    out_term1 = v[1] * hidden[1]
    out_partial = out_term0 + out_term1
    prediction = out_partial + c
    error = prediction - target
    squared_error = error ** 2
    loss = squared_error / 2
    steps.extend([
        make_step("M", fraction_text(v[0]), fraction_text(hidden[0]),
                  fraction_text(out_term0)),
        make_step("M", fraction_text(v[1]), fraction_text(hidden[1]),
                  fraction_text(out_term1)),
        make_step("A", fraction_text(out_term0), fraction_text(out_term1),
                  fraction_text(out_partial)),
        make_step("A", fraction_text(out_partial), fraction_text(c),
                  fraction_text(prediction)),
        make_step("OUTPUT", f"y_hat={fraction_text(prediction)}"),
        make_step("S", fraction_text(prediction), fraction_text(target),
                  fraction_text(error)),
        make_step("E", fraction_text(error), 2, fraction_text(squared_error)),
        make_step("D", fraction_text(squared_error), 2, fraction_text(loss)),
        make_step("BACKPROP_GRAD", "dL/dy_hat", fraction_text(error)),
    ])

    grad_v = []
    for index, activation in enumerate(hidden):
        grad = error * activation
        steps.append(make_step("M", fraction_text(error),
                               fraction_text(activation),
                               fraction_text(grad)))
        steps.append(make_step("BACKPROP_GRAD", f"dv{index + 1}",
                               fraction_text(grad)))
        grad_v.append(grad)
    grad_c = error
    steps.append(make_step("BACKPROP_GRAD", "dc", fraction_text(grad_c)))

    grad_w1 = []
    grad_b1 = []
    for row in range(2):
        upstream = error * v[row]
        delta = upstream * relu_primes[row]
        steps.extend([
            make_step("M", fraction_text(error), fraction_text(v[row]),
                      fraction_text(upstream)),
            make_step("M", fraction_text(upstream), relu_primes[row],
                      fraction_text(delta)),
            make_step("BACKPROP_DELTA", f"h{row + 1}",
                      f"delta={fraction_text(delta)}"),
        ])
        row_grads = []
        for col, x_value in enumerate(x_values):
            grad = delta * x_value
            steps.append(make_step("M", fraction_text(delta),
                                   fraction_text(x_value),
                                   fraction_text(grad)))
            steps.append(make_step("BACKPROP_GRAD",
                                   f"dW1_{row + 1}{col + 1}",
                                   fraction_text(grad)))
            row_grads.append(grad)
        steps.append(make_step("BACKPROP_GRAD", f"db1_{row + 1}",
                               fraction_text(delta)))
        grad_w1.append(row_grads)
        grad_b1.append(delta)

    new_w1 = [[Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)]]
    new_b1 = [Fraction(0), Fraction(0)]
    new_v = [Fraction(0), Fraction(0)]
    for row in range(2):
        for col in range(2):
            new_w1[row][col] = append_update(
                steps, eta, w1[row][col], grad_w1[row][col]
            )
            steps.append(make_step("UPDATE", f"W1_{row + 1}{col + 1}",
                                   fraction_text(new_w1[row][col])))
        new_b1[row] = append_update(steps, eta, b1[row], grad_b1[row])
        steps.append(make_step("UPDATE", f"b1_{row + 1}",
                               fraction_text(new_b1[row])))
    for index in range(2):
        new_v[index] = append_update(steps, eta, v[index], grad_v[index])
        steps.append(make_step("UPDATE", f"v{index + 1}",
                               fraction_text(new_v[index])))
    new_c = append_update(steps, eta, c, grad_c)
    steps.append(make_step("UPDATE", "c", fraction_text(new_c)))

    answer = (
        f"y_hat={fraction_text(prediction)}; loss={fraction_text(loss)}; "
        f"W1_new={matrix_text(new_w1)}; b1_new={vector_text(new_b1)}; "
        f"v_new={vector_text(new_v)}; c_new={fraction_text(new_c)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestBackpropGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = BackpropGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "backprop_relu_step")
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

    def test_arithmetic_steps_and_relu_derivatives(self):
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
                elif fields[0] == "RELU":
                    z_value = Fraction(fields[1].split("=")[1])
                    h_value = Fraction(fields[2].split("=")[1])
                    deriv = int(fields[3].split("=")[1])
                    self.assertEqual(h_value, relu(z_value), raw_step)
                    self.assertEqual(deriv, relu_derivative(z_value), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
