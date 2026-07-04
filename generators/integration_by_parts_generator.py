import random
from base_generator import ProblemGenerator
from helpers import step, jid


def cm(c, body):
    """Coefficient times a symbolic body, unit-aware."""
    if c == 1:
        return body
    if c == -1:
        return f"-{body}"
    return f"{c}{body}" if not body[0].isdigit() else f"{c}·{body}"


class IntegrationByPartsGenerator(ProblemGenerator):
    """
    Integration by parts with the u/dv choice and both du and v
    written out, the boundary term formed, and the leftover integral
    finished.

    Variants:
    - x_exp:  ∫ cx·e^(±x) dx
    - x_trig: ∫ cx·cos(x) dx and ∫ cx·sin(x) dx
    - ln:     ∫ c·ln(x) dx (u = ln x, dv = dx)

    Op-codes used:
    - INTEG_SETUP / ANTIDERIV / REWRITE (established)
    - PARTS_FORMULA: ∫ u dv = uv - ∫ v du
    - PARTS_CHOOSE: the u/dv split and the resulting du/v
    - Z: F(x) + C
    """

    VARIANTS = ["x_exp", "x_trig", "ln"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        c = random.choice([v for v in range(-5, 6) if v != 0])

        if variant == "x_exp":
            neg = random.random() < 0.4
            ex = "e^(-x)" if neg else "e^x"
            body = f"{cm(c, 'x')} {ex}"
            if not neg:
                F = f"{cm(c, 'x')} e^x - {cm(abs(c), ex)}" if c > 0 \
                    else f"{cm(c, 'x')} e^x + {cm(abs(c), ex)}"
                v_txt, leftover = "e^x", f"{cm(c, ex)}"
            else:
                # ∫ cx e^(-x) = -cx e^(-x) + c∫e^(-x) = -cx e^(-x) - c e^(-x)
                F = (f"{cm(-c, 'x')} {ex} - {cm(abs(c), ex)}" if c > 0
                     else f"{cm(-c, 'x')} {ex} + {cm(abs(c), ex)}")
                v_txt = "-e^(-x)"
                leftover = f"{cm(-c, ex)}"
            steps = [
                step("INTEG_SETUP", f"∫ {body} dx",
                     "integration by parts"),
                step("PARTS_FORMULA", "∫ u dv = uv - ∫ v du"),
                step("PARTS_CHOOSE",
                     f"u = {cm(c, 'x')}, dv = {ex} dx",
                     f"du = {c} dx, v = {v_txt}"),
                step("REWRITE",
                     f"{cm(c, 'x')}({v_txt}) - ∫ {c}({v_txt}) dx"),
                step("ANTIDERIV", f"{c}({v_txt})",
                     leftover if not neg else f"{cm(c, ex)}"),
                step("REWRITE", F),
            ]
            answer = f"{F} + C"
            problem = f"Find ∫ {body} dx."
        elif variant == "x_trig":
            fn = random.choice(["cos", "sin"])
            body = f"{cm(c, 'x')} {fn}(x)"
            if fn == "cos":
                # c x sin x + c cos x
                F = (f"{cm(c, 'x')} sin(x) + {cm(abs(c), 'cos(x)')}"
                     if c > 0 else
                     f"{cm(c, 'x')} sin(x) - {cm(abs(c), 'cos(x)')}")
                v_txt = "sin(x)"
                left_anti = cm(-c, "cos(x)")
            else:
                # -c x cos x + c sin x
                F = (f"{cm(-c, 'x')} cos(x) + {cm(abs(c), 'sin(x)')}"
                     if c > 0 else
                     f"{cm(-c, 'x')} cos(x) - {cm(abs(c), 'sin(x)')}")
                v_txt = "-cos(x)"
                left_anti = cm(-c, "sin(x)")
            steps = [
                step("INTEG_SETUP", f"∫ {body} dx",
                     "integration by parts"),
                step("PARTS_FORMULA", "∫ u dv = uv - ∫ v du"),
                step("PARTS_CHOOSE",
                     f"u = {cm(c, 'x')}, dv = {fn}(x) dx",
                     f"du = {c} dx, v = {v_txt}"),
                step("REWRITE",
                     f"{cm(c, 'x')}({v_txt}) - ∫ {c}({v_txt}) dx"),
                step("ANTIDERIV", f"{c}({v_txt})", left_anti),
                step("REWRITE", F),
            ]
            answer = f"{F} + C"
            problem = f"Find ∫ {body} dx."
        else:
            body = f"{cm(c, 'ln(x)')}" if abs(c) != 1 else \
                ("ln(x)" if c == 1 else "-ln(x)")
            F = (f"{cm(c, 'x')} ln(x) - {cm(abs(c), 'x')}" if c > 0
                 else f"{cm(c, 'x')} ln(x) + {cm(abs(c), 'x')}")
            steps = [
                step("INTEG_SETUP", f"∫ {body} dx",
                     "integration by parts"),
                step("PARTS_FORMULA", "∫ u dv = uv - ∫ v du"),
                step("PARTS_CHOOSE",
                     f"u = ln(x), dv = {c} dx",
                     f"du = dx/x, v = {cm(c, 'x')}"),
                step("REWRITE",
                     f"{cm(c, 'x')} ln(x) - ∫ {c} dx"),
                step("ANTIDERIV", f"{c} dx", cm(c, "x")),
                step("REWRITE", F),
            ]
            answer = f"{F} + C"
            problem = f"Find ∫ {body} dx."
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"integration_by_parts_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
