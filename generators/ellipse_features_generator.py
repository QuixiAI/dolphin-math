import math
import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.parabola_features_generator import shift


class EllipseFeaturesGenerator(ProblemGenerator):
    """
    Center, vertices, and foci of an ellipse in standard form. The
    larger denominator names the major axis; c^2 = a^2 - b^2 is
    computed explicitly, with integer c from Pythagorean triples and
    exact √ forms otherwise.

    Op-codes used:
    - CONIC_SETUP: the equation and the goal (established)
    - FORM_IDENTIFY: which axis is major and why (established)
    - CENTER: the center (point)
    - E / EVAL: read a and b from the denominators (established)
    - S / A: coordinate and c^2 arithmetic (established)
    - VERTEX: each major-axis vertex (established)
    - FOCUS: each focus (established)
    - Z: 'center ...; vertices ... and ...; foci ... and ...'
    """

    TRIPLES = [(5, 4, 3), (5, 3, 4), (13, 12, 5), (13, 5, 12),
               (10, 8, 6), (10, 6, 8), (17, 15, 8), (15, 12, 9),
               (20, 16, 12), (25, 24, 7)]

    def generate(self) -> dict:
        h = random.randint(-6, 6)
        k = random.randint(-6, 6)
        if random.random() < 0.6:
            a, b, c = random.choice(self.TRIPLES)
            c_txt = str(c)
            f_lo, f_hi = -c, c
        else:
            while True:
                a = random.randint(3, 7)
                b = random.randint(2, a - 1)
                c2 = a * a - b * b
                r = math.isqrt(c2)
                # squarefree and non-square keeps c an irreducible root
                if r * r != c2 and all(c2 % (f * f) for f in range(2, 6)):
                    break
            c_txt = f"√{a * a - b * b}"
            f_lo, f_hi = None, None
        horizontal = random.random() < 0.5
        a2, b2 = a * a, b * b

        xs = shift("x", h) if h else "x"
        ys = shift("y", k) if k else "y"
        if horizontal:
            eq = f"{xs}^2/{a2} + {ys}^2/{b2} = 1"
            verts = [(h - a, k), (h + a, k)]
            if f_lo is not None:
                foci = [f"({h - c}, {k})", f"({h + c}, {k})"]
            else:
                foci = [f"({h} - {c_txt}, {k})", f"({h} + {c_txt}, {k})"]
            axis_note = f"major axis horizontal ({a2} > {b2})"
        else:
            eq = f"{xs}^2/{b2} + {ys}^2/{a2} = 1"
            verts = [(h, k - a), (h, k + a)]
            if f_lo is not None:
                foci = [f"({h}, {k - c})", f"({h}, {k + c})"]
            else:
                foci = [f"({h}, {k} - {c_txt})", f"({h}, {k} + {c_txt})"]
            axis_note = f"major axis vertical ({a2} > {b2})"

        steps = [
            step("CONIC_SETUP", eq, "center, vertices, foci"),
            step("FORM_IDENTIFY",
                 "(x - h)^2/a^2 + (y - k)^2/b^2 = 1 (ellipse)",
                 axis_note),
            step("CENTER", f"({h}, {k})"),
            step("E", a, 2, a2),
            step("EVAL", "a", a),
            step("E", b, 2, b2),
            step("EVAL", "b", b),
        ]
        if horizontal:
            steps.append(step("S", h, a, h - a))
            steps.append(step("A", h, a, h + a))
        else:
            steps.append(step("S", k, a, k - a))
            steps.append(step("A", k, a, k + a))
        for v in verts:
            steps.append(step("VERTEX", f"({v[0]}, {v[1]})"))
        steps.append(step("S", a2, b2, a2 - b2))
        steps.append(step("EVAL", "c^2", a2 - b2))
        steps.append(step("EVAL", "c", c_txt))
        for f in foci:
            steps.append(step("FOCUS", f))

        answer = (f"center ({h}, {k}); vertices ({verts[0][0]}, "
                  f"{verts[0][1]}) and ({verts[1][0]}, {verts[1][1]}); "
                  f"foci {foci[0]} and {foci[1]}")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="ellipse_features",
            problem=(f"Find the center, vertices, and foci of the "
                     f"ellipse {eq}."),
            steps=steps,
            final_answer=answer,
        )
