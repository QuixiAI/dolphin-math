import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


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


def random_nonzero(low=-2, high=2):
    return random.choice([value for value in range(low, high + 1)
                          if value != 0])


def update_param(steps, eta, old_value, gradient):
    scaled = eta * gradient
    new_value = old_value - scaled
    steps.append(step("M", fraction_text(eta), fraction_text(gradient),
                      fraction_text(scaled)))
    steps.append(step("S", fraction_text(old_value), fraction_text(scaled),
                      fraction_text(new_value)))
    return new_value


class BackpropGenerator(ProblemGenerator):
    """
    One exact backpropagation step for a tiny 2-2-1 ReLU network.

    The network has two inputs, two ReLU hidden units, and one linear output.
    A single squared-error training example keeps every forward and backward
    value rational and directly checkable.

    Op-codes used:
    - BACKPROP_SETUP / PARAMS / HIDDEN_PRE / RELU / OUTPUT
    - BACKPROP_GRAD / BACKPROP_DELTA / UPDATE
    - A / S / M / D / E (established/shared): exact forward, gradient,
      loss, and update arithmetic
    - Z: prediction, loss, and updated parameters
    """

    def generate(self) -> dict:
        for _ in range(100):
            x_values = [random_nonzero(-3, 3), random_nonzero(-3, 3)]
            target = random.randint(-4, 4)
            w1 = [
                [random.randint(-2, 2), random.randint(-2, 2)],
                [random.randint(-2, 2), random.randint(-2, 2)],
            ]
            b1 = [random.randint(-2, 2), random.randint(-2, 2)]
            v = [random_nonzero(-2, 2), random_nonzero(-2, 2)]
            c = random.randint(-2, 2)
            eta = Fraction(1, random.randint(3, 8))
            pre = [
                w1[row][0] * x_values[0] + w1[row][1] * x_values[1] + b1[row]
                for row in range(2)
            ]
            hidden = [relu(value) for value in pre]
            prediction = v[0] * hidden[0] + v[1] * hidden[1] + c
            error = prediction - target
            if all(value != 0 for value in pre) and any(hidden) and error != 0:
                break

        steps = [
            step("BACKPROP_SETUP", f"x={vector_text(x_values)}",
                 f"y={target}", f"eta={fraction_text(eta)}"),
            step("PARAMS", f"W1={matrix_text(w1)}", f"b1={vector_text(b1)}",
                 f"v={vector_text(v)}, c={c}"),
        ]

        hidden = []
        relu_primes = []
        pre_values = []
        for row in range(2):
            term0 = Fraction(w1[row][0]) * x_values[0]
            term1 = Fraction(w1[row][1]) * x_values[1]
            partial = term0 + term1
            pre_value = partial + b1[row]
            activation = relu(pre_value)
            derivative = relu_derivative(pre_value)
            steps.extend([
                step("M", w1[row][0], x_values[0], fraction_text(term0)),
                step("M", w1[row][1], x_values[1], fraction_text(term1)),
                step("A", fraction_text(term0), fraction_text(term1),
                     fraction_text(partial)),
                step("A", fraction_text(partial), b1[row],
                     fraction_text(pre_value)),
                step("HIDDEN_PRE", f"h{row + 1}", f"z={fraction_text(pre_value)}"),
                step("RELU", f"z={fraction_text(pre_value)}",
                     f"h={fraction_text(activation)}", f"deriv={derivative}"),
            ])
            pre_values.append(pre_value)
            hidden.append(activation)
            relu_primes.append(derivative)

        out_term0 = Fraction(v[0]) * hidden[0]
        out_term1 = Fraction(v[1]) * hidden[1]
        out_partial = out_term0 + out_term1
        prediction = out_partial + c
        error = prediction - target
        squared_error = error ** 2
        loss = squared_error / 2
        steps.extend([
            step("M", v[0], fraction_text(hidden[0]),
                 fraction_text(out_term0)),
            step("M", v[1], fraction_text(hidden[1]),
                 fraction_text(out_term1)),
            step("A", fraction_text(out_term0), fraction_text(out_term1),
                 fraction_text(out_partial)),
            step("A", fraction_text(out_partial), c, fraction_text(prediction)),
            step("OUTPUT", f"y_hat={fraction_text(prediction)}"),
            step("S", fraction_text(prediction), target, fraction_text(error)),
            step("E", fraction_text(error), 2, fraction_text(squared_error)),
            step("D", fraction_text(squared_error), 2, fraction_text(loss)),
            step("BACKPROP_GRAD", "dL/dy_hat", fraction_text(error)),
        ])

        grad_v = []
        for index, activation in enumerate(hidden):
            grad = error * activation
            steps.append(step("M", fraction_text(error),
                              fraction_text(activation), fraction_text(grad)))
            steps.append(step("BACKPROP_GRAD", f"dv{index + 1}",
                              fraction_text(grad)))
            grad_v.append(grad)
        grad_c = error
        steps.append(step("BACKPROP_GRAD", "dc", fraction_text(grad_c)))

        deltas = []
        grad_w1 = []
        grad_b1 = []
        for row in range(2):
            upstream = error * v[row]
            delta = upstream * relu_primes[row]
            steps.extend([
                step("M", fraction_text(error), v[row],
                     fraction_text(upstream)),
                step("M", fraction_text(upstream), relu_primes[row],
                     fraction_text(delta)),
                step("BACKPROP_DELTA", f"h{row + 1}",
                     f"delta={fraction_text(delta)}"),
            ])
            deltas.append(delta)
            row_grads = []
            for col, x_value in enumerate(x_values):
                grad = delta * x_value
                steps.append(step("M", fraction_text(delta), x_value,
                                  fraction_text(grad)))
                steps.append(step("BACKPROP_GRAD",
                                  f"dW1_{row + 1}{col + 1}",
                                  fraction_text(grad)))
                row_grads.append(grad)
            steps.append(step("BACKPROP_GRAD", f"db1_{row + 1}",
                              fraction_text(delta)))
            grad_w1.append(row_grads)
            grad_b1.append(delta)

        new_w1 = [[Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)]]
        new_b1 = [Fraction(0), Fraction(0)]
        new_v = [Fraction(0), Fraction(0)]
        for row in range(2):
            for col in range(2):
                new_w1[row][col] = update_param(
                    steps, eta, Fraction(w1[row][col]), grad_w1[row][col]
                )
                steps.append(step("UPDATE", f"W1_{row + 1}{col + 1}",
                                  fraction_text(new_w1[row][col])))
            new_b1[row] = update_param(
                steps, eta, Fraction(b1[row]), grad_b1[row]
            )
            steps.append(step("UPDATE", f"b1_{row + 1}",
                              fraction_text(new_b1[row])))
        for index in range(2):
            new_v[index] = update_param(
                steps, eta, Fraction(v[index]), grad_v[index]
            )
            steps.append(step("UPDATE", f"v{index + 1}",
                              fraction_text(new_v[index])))
        new_c = update_param(steps, eta, Fraction(c), grad_c)
        steps.append(step("UPDATE", "c", fraction_text(new_c)))

        answer = (
            f"y_hat={fraction_text(prediction)}; loss={fraction_text(loss)}; "
            f"W1_new={matrix_text(new_w1)}; b1_new={vector_text(new_b1)}; "
            f"v_new={vector_text(new_v)}; c_new={fraction_text(new_c)}"
        )
        steps.append(step("Z", answer))
        problem = (
            "For a 2-2-1 ReLU network with "
            f"x={vector_text(x_values)}, y={target}, eta={fraction_text(eta)}, "
            f"W1={matrix_text(w1)}, b1={vector_text(b1)}, "
            f"v={vector_text(v)}, c={c}. Do one SGD backprop step using "
            "L=1/2*(y_hat-y)^2."
        )
        return dict(
            problem_id=jid(),
            operation="backprop_relu_step",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
