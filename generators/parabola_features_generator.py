import random
from base_generator import ProblemGenerator
from helpers import step, jid


def shift(v, s):
    """(x - h) rendering: shift('x', 3) -> '(x - 3)'."""
    if s == 0:
        return v
    return f"({v} - {s})" if s > 0 else f"({v} + {-s})"


class ParabolaFeaturesGenerator(ProblemGenerator):
    """
    Vertex, focus, and directrix from the standard form of a parabola:
    identify the form and orientation, solve 4p, then shift from the
    vertex with explicit coordinate arithmetic.

    Variants:
    - origin:     x^2 = 4py or y^2 = 4px
    - vertical:   (x - h)^2 = 4p(y - k)
    - horizontal: (y - k)^2 = 4p(x - h)

    Op-codes used:
    - CONIC_SETUP: the equation and the goal (equation, goal)
    - FORM_IDENTIFY: which standard form and orientation (established)
    - D / EVAL: solve 4p = C for p (established)
    - VERTEX: the vertex (point)
    - A / S: the focus / directrix coordinate arithmetic (established)
    - FOCUS: the focus (point)
    - DIRECTRIX: the directrix (line equation)
    - Z: 'vertex (h, k); focus (a, b); directrix ...'
    """

    VARIANTS = ["origin", "vertical", "horizontal"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        p = random.choice([v for v in range(-5, 6) if v != 0])
        C = 4 * p
        if variant == "origin":
            h = k = 0
            vertical = random.random() < 0.5
        else:
            h = random.randint(-6, 6)
            k = random.randint(-6, 6)
            if h == 0 and k == 0:
                return self.generate()
            vertical = variant == "vertical"

        if vertical:
            lhs = f"{shift('x', h)}^2" if h != 0 else "x^2"
            rhs = f"{C}{shift('y', k)}" if k != 0 else f"{C}y"
            form = "(x - h)^2 = 4p(y - k)" if (h or k) else "x^2 = 4py"
            direction = "opens up" if p > 0 else "opens down"
            focus = (h, k + p)
            directrix = f"y = {k - p}"
        else:
            lhs = f"{shift('y', k)}^2" if k != 0 else "y^2"
            rhs = f"{C}{shift('x', h)}" if h != 0 else f"{C}x"
            form = "(y - k)^2 = 4p(x - h)" if (h or k) else "y^2 = 4px"
            direction = "opens right" if p > 0 else "opens left"
            focus = (h + p, k)
            directrix = f"x = {h - p}"
        eq = f"{lhs} = {rhs}"

        steps = [
            step("CONIC_SETUP", eq, "vertex, focus, directrix"),
            step("FORM_IDENTIFY", form,
                 f"{'vertical' if vertical else 'horizontal'} parabola, "
                 f"{direction}"),
            step("D", C, 4, p),
            step("EVAL", "p", p),
            step("VERTEX", f"({h}, {k})"),
        ]
        if vertical:
            steps.append(step("A", k, p, k + p))
            steps.append(step("FOCUS", f"({h}, {k + p})"))
            steps.append(step("S", k, p, k - p))
        else:
            steps.append(step("A", h, p, h + p))
            steps.append(step("FOCUS", f"({h + p}, {k})"))
            steps.append(step("S", h, p, h - p))
        steps.append(step("DIRECTRIX", directrix))

        answer = (f"vertex ({h}, {k}); focus ({focus[0]}, {focus[1]}); "
                  f"directrix {directrix}")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="parabola_features",
            problem=(f"Find the vertex, focus, and directrix of "
                     f"{eq}."),
            steps=steps,
            final_answer=answer,
        )
