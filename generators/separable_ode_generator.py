import random
from base_generator import ProblemGenerator
from helpers import step, jid


class SeparableODEGenerator(ProblemGenerator):
    """
    Separable differential equations solved by the full ritual:
    separate, integrate both sides, resolve the constant from the
    initial condition, and isolate y. Answers stay exact and
    symbolic.

    Variants:
    - exponential: dy/dt = ky, y(0) = y0 -> y = y0·e^(kt)
    - find_k:      y doubles (or halves) in T -> k = ln(2)/T exactly
    - power:       dy/dx = x²/y², y(0) = c -> y = ∛(x³ + c³)
    - reciprocal:  dy/dx = y², y(0) = a -> y = a/(1 - ax)

    Op-codes used:
    - ODE_SETUP: the equation and initial condition
    - SEPARATE: variables to their own sides (equation)
    - INTEG_RULE / ANTIDERIV / REWRITE / SUBST / EVAL (established)
    - Z: the particular solution or the exact k
    """

    VARIANTS = ["exponential", "find_k", "power", "reciprocal"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "exponential":
            k = random.choice([v for v in range(-5, 6) if v != 0])
            y0 = random.choice([2, 3, 4, 5, 7, 10])
            kt = "t" if k == 1 else f"{k}t"
            answer = f"y = {y0}e^({kt})"
            steps = [
                step("ODE_SETUP", f"dy/dt = {k}y, y(0) = {y0}", "solve"),
                step("SEPARATE", f"dy/y = {k} dt"),
                step("INTEG_RULE", "both sides",
                     f"∫ dy/y = ∫ {k} dt"),
                step("ANTIDERIV", "dy/y", "ln(abs(y))"),
                step("ANTIDERIV", f"{k} dt", f"{kt} + C"),
                step("REWRITE", f"ln(abs(y)) = {kt} + C"),
                step("REWRITE", f"y = A·e^({kt}) with A = ±e^C"),
                step("SUBST", "t", 0, f"y(0) = A = {y0}"),
            ]
            problem = f"Solve dy/dt = {k}y with y(0) = {y0}."
        elif variant == "find_k":
            T = random.choice([2, 3, 4, 5, 8, 10, 12])
            double = random.random() < 0.6
            word = "doubles" if double else "halves"
            answer = (f"k = ln(2)/{T}" if double
                      else f"k = -ln(2)/{T}")
            steps = [
                step("ODE_SETUP", f"dy/dt = ky; y {word} every {T} "
                     f"hours", "find k exactly"),
                step("REWRITE", "y = y0·e^(kt)"),
                step("SUBST", "t", T,
                     f"y(T)/y0 = {'2' if double else '1/2'} = "
                     f"e^({T}k)"),
                step("LOG_BOTH_SIDES",
                     f"ln({'2' if double else '1/2'}) = {T}k"),
                step("EQ_OP_BOTH", "divide", T, "k",
                     answer.replace("k = ", "")),
            ]
            problem = (f"A quantity satisfies dy/dt = ky and {word} "
                       f"every {T} hours. Find k exactly.")
        elif variant == "power":
            c = random.choice([1, 2, 3, 4])
            answer = f"y = ∛(x^3 + {c ** 3})"
            steps = [
                step("ODE_SETUP", f"dy/dx = x^2/y^2, y(0) = {c}",
                     "solve"),
                step("SEPARATE", "y^2 dy = x^2 dx"),
                step("INTEG_RULE", "both sides",
                     "∫ y^2 dy = ∫ x^2 dx"),
                step("ANTIDERIV", "y^2 dy", "(1/3)y^3"),
                step("ANTIDERIV", "x^2 dx", "(1/3)x^3 + C"),
                step("REWRITE", "y^3 = x^3 + C'"),
                step("SUBST", "x", 0,
                     f"{c}^3 = C', so C' = {c ** 3}"),
                step("REWRITE", f"y^3 = x^3 + {c ** 3}"),
            ]
            problem = f"Solve dy/dx = x^2/y^2 with y(0) = {c}."
        else:
            a = random.choice([1, 2, 3, 4, 5])
            ax = "x" if a == 1 else f"{a}x"
            answer = f"y = {a}/(1 - {ax})"
            steps = [
                step("ODE_SETUP", f"dy/dx = y^2, y(0) = {a}", "solve"),
                step("SEPARATE", "y^(-2) dy = dx"),
                step("INTEG_RULE", "both sides",
                     "∫ y^(-2) dy = ∫ dx"),
                step("ANTIDERIV", "y^(-2) dy", "-1/y"),
                step("ANTIDERIV", "dx", "x + C"),
                step("REWRITE", "-1/y = x + C"),
                step("SUBST", "x", 0, f"-1/{a} = C"),
                step("REWRITE", f"-1/y = x - 1/{a}"),
                step("REWRITE", f"y = {a}/(1 - {ax})"),
            ]
            problem = f"Solve dy/dx = y^2 with y(0) = {a}."
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"separable_ode_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
