import math
import random

from base_generator import ProblemGenerator
from helpers import step, jid


GEOMETRIC_PAIRS = [(2, 3), (2, 5), (3, 4), (3, 5), (4, 5)]


def add_step(steps, running, value):
    total = running + value
    steps.append(step("A", running, value, total))
    return total


class GeneratingFunctionGenerator(ProblemGenerator):
    """
    Coefficient extraction from simple generating-function products.

    Variants:
    - binomial_product: [x^n](1+x)^a(1+x)^b by matching exponents
    - geometric_product: [x^n] 1/((1-x^a)(1-x^b)) by solution counts

    Op-codes used:
    - GF_SETUP: target coefficient and product
    - GF_EXPAND: expansion rule for a factor
    - NCR: binomial coefficient
    - COEFF_PAIR: exponent pair contributing to the target coefficient
    - GF_DIV_CHECK: divisibility check for geometric-series exponents
    - A / S / M / D (established): arithmetic
    - Z: exact coefficient
    """

    VARIANTS = ["binomial_product", "geometric_product"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "binomial_product":
            a = random.randint(3, 8)
            b = random.randint(3, 8)
            target = random.randint(2, a + b - 2)
            product = f"(1 + x)^{a}(1 + x)^{b}"
            steps = [
                step("GF_SETUP", f"[x^{target}]", product),
                step("GF_EXPAND", f"(1 + x)^{a}",
                     "sum C(a,i)x^i"),
                step("GF_EXPAND", f"(1 + x)^{b}",
                     "sum C(b,j)x^j"),
            ]
            running = 0
            lo = max(0, target - b)
            hi = min(a, target)
            for i in range(lo, hi + 1):
                j = target - i
                ci = math.comb(a, i)
                cj = math.comb(b, j)
                term = ci * cj
                steps.extend([
                    step("NCR", f"C({a}, {i})", ci),
                    step("NCR", f"C({b}, {j})", cj),
                    step("M", ci, cj, term),
                    step("COEFF_PAIR", f"i={i}, j={j}",
                         f"{i}+{j}={target}", term),
                ])
                running = add_step(steps, running, term)
            problem = (
                f"Find the coefficient of x^{target} in {product}."
            )
            value = running
        else:
            a, b = random.choice(GEOMETRIC_PAIRS)
            i0 = random.randint(1, 5)
            j0 = random.randint(1, 5)
            target = a * i0 + b * j0
            product = f"1/((1 - x^{a})(1 - x^{b}))"
            steps = [
                step("GF_SETUP", f"[x^{target}]", product),
                step("GF_EXPAND", f"1/(1 - x^{a})",
                     f"sum x^({a}i), i >= 0"),
                step("GF_EXPAND", f"1/(1 - x^{b})",
                     f"sum x^({b}j), j >= 0"),
            ]
            running = 0
            for i in range(target // a + 1):
                ai = a * i
                rem = target - ai
                steps.append(step("M", a, i, ai))
                steps.append(step("S", target, ai, rem))
                if rem % b == 0:
                    j = rem // b
                    steps.append(step("D", rem, b, j))
                    steps.append(step("COEFF_PAIR", f"i={i}, j={j}",
                                      f"{a}i + {b}j = {target}",
                                      "accepted"))
                    running = add_step(steps, running, 1)
                else:
                    steps.append(step("GF_DIV_CHECK", f"{rem} / {b}",
                                      "not integer", "reject"))
            problem = (
                f"Find the coefficient of x^{target} in {product}."
            )
            value = running

        answer = f"coefficient = {value}"
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"generating_function_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
