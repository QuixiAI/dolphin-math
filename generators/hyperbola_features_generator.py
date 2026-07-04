import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.parabola_features_generator import shift


def slope_txt(fr):
    """±slope factor: '(3/4)', '2', leaves off 1."""
    if fr.denominator == 1:
        return "" if fr == 1 else str(fr)
    return f"({fr})"


class HyperbolaFeaturesGenerator(ProblemGenerator):
    """
    Center, vertices, foci, and asymptotes of a hyperbola in standard
    form. The positive term names the transverse axis; c^2 = a^2 + b^2
    (the plus is the classic contrast with the ellipse), and the
    asymptote slope is reduced to lowest terms.

    Op-codes used:
    - CONIC_SETUP / FORM_IDENTIFY / CENTER / E / EVAL / S / A /
      VERTEX / FOCUS: as the other conic generators (established)
    - FRAC_REDUCE: the asymptote slope b/a in lowest terms (established)
    - ASYMPTOTE: both asymptote lines in ± form (equation)
    - Z: 'center ...; vertices ...; foci ...; asymptotes ...'
    """

    TRIPLES = [(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10),
               (5, 12, 13), (12, 5, 13), (9, 12, 15), (8, 15, 17)]

    def generate(self) -> dict:
        h = random.randint(-6, 6)
        k = random.randint(-6, 6)
        if random.random() < 0.6:
            a, b, c = random.choice(self.TRIPLES)
            c_txt = str(c)
            c_int = True
        else:
            while True:
                a = random.randint(1, 6)
                b = random.randint(1, 6)
                c2 = a * a + b * b
                r = math.isqrt(c2)
                if r * r != c2 and all(c2 % (f * f) for f in range(2, 6)):
                    break
            c_txt = f"√{a * a + b * b}"
            c_int = False
        horizontal = random.random() < 0.5
        a2, b2 = a * a, b * b

        xs = shift("x", h) if h else "x"
        ys = shift("y", k) if k else "y"
        slope = Fraction(b, a) if horizontal else Fraction(a, b)
        if horizontal:
            eq = f"{xs}^2/{a2} - {ys}^2/{b2} = 1"
            verts = [(h - a, k), (h + a, k)]
            if c_int:
                foci = [f"({h - c}, {k})", f"({h + c}, {k})"]
            else:
                foci = [f"({h} - {c_txt}, {k})", f"({h} + {c_txt}, {k})"]
            note = "opens left-right (x term positive)"
        else:
            eq = f"{ys}^2/{a2} - {xs}^2/{b2} = 1"
            verts = [(h, k - a), (h, k + a)]
            if c_int:
                foci = [f"({h}, {k - c})", f"({h}, {k + c})"]
            else:
                foci = [f"({h}, {k} - {c_txt})", f"({h}, {k} + {c_txt})"]
            note = "opens up-down (y term positive)"

        st = slope_txt(slope)
        x_part = f"{st}{shift('x', h)}" if h else f"{st}x"
        if k == 0:
            asym = f"y = ±{x_part}"
        else:
            asym = f"y = {k} ± {x_part}"

        steps = [
            step("CONIC_SETUP", eq, "center, vertices, foci, asymptotes"),
            step("FORM_IDENTIFY", "hyperbola in standard form", note),
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
        steps.append(step("A", a2, b2, a2 + b2))
        steps.append(step("EVAL", "c^2", a2 + b2))
        steps.append(step("EVAL", "c", c_txt))
        for f in foci:
            steps.append(step("FOCUS", f))
        raw = Fraction(b, a) if horizontal else Fraction(a, b)
        raw_txt = f"{b}/{a}" if horizontal else f"{a}/{b}"
        if str(raw) != raw_txt:
            steps.append(step("FRAC_REDUCE", raw_txt, raw))
        steps.append(step("ASYMPTOTE", asym))

        answer = (f"center ({h}, {k}); vertices ({verts[0][0]}, "
                  f"{verts[0][1]}) and ({verts[1][0]}, {verts[1][1]}); "
                  f"foci {foci[0]} and {foci[1]}; asymptotes {asym}")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="hyperbola_features",
            problem=(f"Find the center, vertices, foci, and asymptotes "
                     f"of the hyperbola {eq}."),
            steps=steps,
            final_answer=answer,
        )
