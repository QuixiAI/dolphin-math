import random

from base_generator import ProblemGenerator
from helpers import step, jid


def poly2_text(b_value, c_value):
    return f"s^2+{b_value}s+{c_value}"


class TransferFunctionGenerator(ProblemGenerator):
    """
    Transfer functions from ODEs and simple feedback block diagrams.

    Variants:
    - ode: zero-initial-condition Laplace transform, zero, and poles
    - block_feedback: two series blocks with unity negative feedback

    Op-codes used:
    - TF_SETUP: ODE or block diagram inputs
    - LAPLACE: transformed ODE terms
    - SERIES / FEEDBACK: block reduction steps
    - TRANSFER: transfer function
    - FACTOR / ZERO / POLES: pole-zero extraction
    - A / M (established/shared): exact coefficient arithmetic
    - Z: reduced transfer function and requested pole/zero data
    """

    VARIANTS = ["ode", "block_feedback"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "ode":
            problem, steps, answer = self._generate_ode()
        else:
            problem, steps, answer = self._generate_block_feedback()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"transfer_function_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_ode(self):
        p1, p2 = sorted((random.randint(1, 12), random.randint(1, 12)))
        zero = random.randint(1, 12)
        gain = random.randint(1, 8)
        b_value = p1 + p2
        c_value = p1 * p2
        numerator_constant = gain * zero
        numerator = f"{gain}s+{numerator_constant}"
        denominator = poly2_text(b_value, c_value)
        steps = [
            step("TF_SETUP", "ode",
                 f"y''+{b_value}y'+{c_value}y={gain}x'+{numerator_constant}x",
                 "zero initial conditions"),
            step("A", p1, p2, b_value),
            step("M", p1, p2, c_value),
            step("M", gain, zero, numerator_constant),
            step("LAPLACE", "Y terms",
                 f"({denominator})Y(s)"),
            step("LAPLACE", "X terms", f"({numerator})X(s)"),
            step("TRANSFER", f"H(s)=({numerator})/({denominator})"),
            step("FACTOR", f"{denominator}=(s+{p1})(s+{p2})"),
            step("ZERO", f"s=-{zero}"),
            step("POLES", f"s=-{p1}, -{p2}"),
        ]
        answer = (
            f"H(s)=({numerator})/({denominator}); "
            f"zero=-{zero}; poles=-{p1},-{p2}"
        )
        problem = (
            f"With zero initial conditions, find the transfer function, zero, "
            f"and poles for y''+{b_value}y'+{c_value}y={gain}x'+"
            f"{numerator_constant}x."
        )
        return problem, steps, answer

    def _generate_block_feedback(self):
        a = random.randint(1, 12)
        b = random.randint(1, 12)
        p = random.randint(1, 12)
        q = random.randint(1, 12)
        gain_product = a * b
        sum_pq = p + q
        product_pq = p * q
        closed_constant = product_pq + gain_product
        forward_den = poly2_text(sum_pq, product_pq)
        closed_den = poly2_text(sum_pq, closed_constant)
        steps = [
            step("TF_SETUP", "block_feedback",
                 f"G1={a}/(s+{p}), G2={b}/(s+{q})", "H=1"),
            step("SERIES", "G=G1*G2"),
            step("M", a, b, gain_product),
            step("A", p, q, sum_pq),
            step("M", p, q, product_pq),
            step("TRANSFER", f"G(s)={gain_product}/({forward_den})"),
            step("FEEDBACK", "T=G/(1+G)"),
            step("A", product_pq, gain_product, closed_constant),
            step("TRANSFER", f"T(s)={gain_product}/({closed_den})"),
        ]
        answer = f"T(s)={gain_product}/({closed_den})"
        problem = (
            f"Reduce a unity negative-feedback block diagram with "
            f"G1={a}/(s+{p}) and G2={b}/(s+{q})."
        )
        return problem, steps, answer
