import random
from base_generator import ProblemGenerator
from helpers import step, jid


def pt(p):
    return f"({p[0]}, {p[1]})"


class TransformationGenerator(ProblemGenerator):
    """
    Coordinate-rule transformations of a point: translations,
    reflections (axes and y = x), rotations about the origin
    (90/180/270 CCW), dilations, and two-step compositions applied in
    order. Each transform states its rule before applying it;
    translations and dilations show the arithmetic.

    Op-codes used:
    - TRANSFORM_SETUP: the point and the transformation(s) (point, plan)
    - TRANSFORM_RULE: the coordinate rule (rule)
    - A / S / M: translation and dilation arithmetic (established)
    - TRANSFORM_APPLY: substituted coordinates and the image
      (work, image)
    - Z: the final image point
    """

    def _catalog(self):
        a = random.choice([v for v in range(-6, 7) if v != 0])
        b = random.choice([v for v in range(-6, 7) if v != 0])
        k = random.choice([2, 3, 4])
        return [
            (f"translation by ({a}, {b})",
             f"(x, y) → (x {'+' if a > 0 else '-'} {abs(a)}, "
             f"y {'+' if b > 0 else '-'} {abs(b)})",
             lambda p: (p[0] + a, p[1] + b), ("translate", a, b)),
            ("reflection over the x-axis", "(x, y) → (x, -y)",
             lambda p: (p[0], -p[1]), None),
            ("reflection over the y-axis", "(x, y) → (-x, y)",
             lambda p: (-p[0], p[1]), None),
            ("reflection over the line y = x", "(x, y) → (y, x)",
             lambda p: (p[1], p[0]), None),
            ("rotation 90° counterclockwise about the origin",
             "(x, y) → (-y, x)", lambda p: (-p[1], p[0]), None),
            ("rotation 180° about the origin", "(x, y) → (-x, -y)",
             lambda p: (-p[0], -p[1]), None),
            ("rotation 270° counterclockwise about the origin",
             "(x, y) → (y, -x)", lambda p: (p[1], -p[0]), None),
            (f"dilation by factor {k} centered at the origin",
             f"(x, y) → ({k}x, {k}y)",
             lambda p: (k * p[0], k * p[1]), ("dilate", k)),
        ]

    def _apply(self, steps, p, name, rule, fn, arith):
        steps.append(step("TRANSFORM_RULE", rule))
        q = fn(p)
        if arith and arith[0] == "translate":
            _, a, b = arith
            steps.append(step("A" if a > 0 else "S", p[0], abs(a), q[0]))
            steps.append(step("A" if b > 0 else "S", p[1], abs(b), q[1]))
        elif arith and arith[0] == "dilate":
            k = arith[1]
            steps.append(step("M", k, p[0], q[0]))
            steps.append(step("M", k, p[1], q[1]))
        wx, wy = f"({p[0]})", f"({p[1]})"
        steps.append(step("TRANSFORM_APPLY",
                          rule.split("→ ")[1]
                          .replace("x", wx).replace("y", wy), pt(q)))
        return q

    def generate(self) -> dict:
        p = (random.choice([v for v in range(-8, 9) if v != 0]),
             random.choice([v for v in range(-8, 9) if v != 0]))
        composition = random.random() < 0.4
        cat = self._catalog()

        if composition:
            (n1, r1, f1, a1), (n2, r2, f2, a2) = random.sample(cat, 2)
            plan = f"{n1}, then {n2}"
            steps = [step("TRANSFORM_SETUP", f"P{pt(p)}", plan)]
            mid = self._apply(steps, p, n1, r1, f1, a1)
            final = self._apply(steps, mid, n2, r2, f2, a2)
            problem = (f"Find the image of P{pt(p)} under a {n1} "
                       f"followed by a {n2}.")
            op = "transformation_composition"
        else:
            n1, r1, f1, a1 = random.choice(cat)
            steps = [step("TRANSFORM_SETUP", f"P{pt(p)}", n1)]
            final = self._apply(steps, p, n1, r1, f1, a1)
            problem = f"Find the image of P{pt(p)} under a {n1}."
            op = "transformation_single"

        answer = pt(final)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
