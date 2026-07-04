import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class AdamStepGenerator(ProblemGenerator):
    """
    One exact Adam optimizer step.

    Uses t=1, m0=v0=0, beta1=9/10, beta2=99/100, and epsilon=0. With a nonzero
    integer gradient, bias correction gives m_hat=g and v_hat=g^2, so the
    square root is exact.

    Op-codes used:
    - ADAM_SETUP / MOMENT / BIAS_CORRECT / ADAM_UPDATE
    - M / A / S / D / E / ROOT (established/shared): moment and update math
    - Z: moments, bias-corrected moments, updated parameter
    """

    def generate(self) -> dict:
        theta = Fraction(random.randint(-20, 20), random.choice([1, 2, 4]))
        gradient = random.choice([value for value in range(-10, 11)
                                  if value != 0])
        beta1 = Fraction(9, 10)
        beta2 = Fraction(99, 100)
        lr = random.choice([Fraction(1, 10), Fraction(1, 20), Fraction(1, 100)])
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
            step("ADAM_SETUP", f"theta={fraction_text(theta)},g={gradient}",
                 "beta1=9/10,beta2=99/100",
                 f"lr={fraction_text(lr)},epsilon=0"),
            step("M", fraction_text(beta1), 0, fraction_text(beta1_m0)),
            step("S", 1, fraction_text(beta1), fraction_text(one_minus_beta1)),
            step("M", fraction_text(one_minus_beta1), gradient,
                 fraction_text(m_add)),
            step("A", fraction_text(beta1_m0), fraction_text(m_add),
                 fraction_text(m)),
            step("MOMENT", "m1", fraction_text(m)),
            step("M", fraction_text(beta2), 0, fraction_text(beta2_v0)),
            step("S", 1, fraction_text(beta2), fraction_text(one_minus_beta2)),
            step("E", gradient, 2, grad_sq),
            step("M", fraction_text(one_minus_beta2), grad_sq,
                 fraction_text(v_add)),
            step("A", fraction_text(beta2_v0), fraction_text(v_add),
                 fraction_text(v)),
            step("MOMENT", "v1", fraction_text(v)),
            step("D", fraction_text(m), fraction_text(one_minus_beta1),
                 fraction_text(m_hat)),
            step("BIAS_CORRECT", "m_hat", fraction_text(m_hat)),
            step("D", fraction_text(v), fraction_text(one_minus_beta2),
                 fraction_text(v_hat)),
            step("BIAS_CORRECT", "v_hat", fraction_text(v_hat)),
            step("ROOT", f"sqrt({fraction_text(v_hat)})", root),
            step("A", root, fraction_text(epsilon), fraction_text(denom)),
            step("D", fraction_text(m_hat), fraction_text(denom),
                 fraction_text(direction)),
            step("M", fraction_text(lr), fraction_text(direction),
                 fraction_text(delta)),
            step("S", fraction_text(theta), fraction_text(delta),
                 fraction_text(theta_new)),
            step("ADAM_UPDATE", "theta_new", fraction_text(theta_new)),
        ]
        answer = (
            f"m={fraction_text(m)}; v={fraction_text(v)}; "
            f"m_hat={fraction_text(m_hat)}; v_hat={fraction_text(v_hat)}; "
            f"theta_new={fraction_text(theta_new)}"
        )
        steps.append(step("Z", answer))
        problem = (
            "Perform one Adam update at t=1 with "
            f"theta={fraction_text(theta)}, gradient g={gradient}, m0=0, "
            "v0=0, beta1=9/10, beta2=99/100, "
            f"lr={fraction_text(lr)}, and epsilon=0."
        )
        return dict(
            problem_id=jid(),
            operation="adam_step_exact_t1",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
