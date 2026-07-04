import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


class LinearApproxGenerator(ProblemGenerator):
    """
    Linear approximation L(x) = f(a) + f'(a)(x - a) at the nearest
    nice point, with the tangent line built and evaluated exactly.

    Variants:
    - sqrt:  √(a² + ε) ≈ a + ε/(2a), answer a reduced fraction
    - cbrt:  ∛(a³ + ε) ≈ a + ε/(3a²)
    - power: (a + δ)³ with a small decimal δ, answer an exact decimal

    Op-codes used:
    - APPROX_SETUP: the quantity and the linearization point
    - DERIV_RULE / POWER_RULE / EVAL / REWRITE / SUBST / M / A
      (established)
    - Z: '√26 ≈ 51/10' or '(4.02)^3 ≈ 64.96'
    """

    VARIANTS = ["sqrt", "cbrt", "power"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "sqrt":
            a = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
            # keep a² the strictly nearest square: eps ≤ a, -eps ≤ a-1
            choices = [e for e in (1, 2, 3, -1, -2)
                       if e <= a and -e <= a - 1]
            eps = random.choice(choices)
            N = a * a + eps
            slope = Fraction(1, 2 * a)
            approx = a + slope * eps
            steps = [
                step("APPROX_SETUP", f"estimate √{N}",
                     f"linearize f(x) = √x at a = {a * a}"),
                step("DERIV_RULE", "d/dx √x = 1/(2√x)",
                     f"f'({a * a}) = 1/{2 * a}"),
                step("EVAL", f"f({a * a})", a),
                step("EVAL", f"f'({a * a})", slope),
                step("REWRITE", f"L(x) = {a} + (1/{2 * a})(x - {a * a})"),
                step("SUBST", "x", N, f"{a} + (1/{2 * a})({eps})"),
                step("M", slope, eps, slope * eps),
                step("A", a, slope * eps, approx),
            ]
            answer = f"√{N} ≈ {approx}"
            problem = (f"Use a linear approximation to estimate √{N}. "
                       f"Give the answer as a fraction.")
        elif variant == "cbrt":
            a = random.choice([2, 3, 4])
            eps = random.choice([1, 2, 3, -1, -2, -3])
            N = a ** 3 + eps
            slope = Fraction(1, 3 * a * a)
            approx = a + slope * eps
            steps = [
                step("APPROX_SETUP", f"estimate ∛{N}",
                     f"linearize f(x) = ∛x at a = {a ** 3}"),
                step("DERIV_RULE", "d/dx ∛x = 1/(3·∛x²)",
                     f"f'({a ** 3}) = 1/{3 * a * a}"),
                step("EVAL", f"f({a ** 3})", a),
                step("EVAL", f"f'({a ** 3})", slope),
                step("REWRITE",
                     f"L(x) = {a} + (1/{3 * a * a})(x - {a ** 3})"),
                step("SUBST", "x", N,
                     f"{a} + (1/{3 * a * a})({eps})"),
                step("M", slope, eps, slope * eps),
                step("A", a, slope * eps, approx),
            ]
            answer = f"∛{N} ≈ {approx}"
            problem = (f"Use a linear approximation to estimate ∛{N}. "
                       f"Give the answer as a fraction.")
        else:
            a = random.choice([2, 3, 4, 5, 10])
            delta = Fraction(random.choice([1, 2, 5, -1, -2]), 100)
            x_val = a + delta
            fa = a ** 3
            fp = 3 * a * a
            approx = fa + fp * delta
            steps = [
                step("APPROX_SETUP", f"estimate ({dec(x_val)})^3",
                     f"linearize f(x) = x^3 at a = {a}"),
                step("EVAL", f"f({a})", fa),
                step("POWER_RULE", "x^3", "3x^2"),
                step("EVAL", f"f'({a})", fp),
                step("REWRITE", f"L(x) = {fa} + {fp}(x - {a})"),
                step("SUBST", "x", dec(x_val),
                     f"{fa} + {fp}({dec(delta)})"),
                step("M", fp, dec(delta), dec(fp * delta)),
                step("A", fa, dec(fp * delta), dec(approx)),
            ]
            answer = f"({dec(x_val)})^3 ≈ {dec(approx)}"
            problem = (f"Use a linear approximation to estimate "
                       f"({dec(x_val)})^3.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"linear_approx_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
