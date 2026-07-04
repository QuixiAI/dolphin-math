import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


COORDS = [
    Fraction(-3), Fraction(-2), Fraction(-3, 2), Fraction(-1),
    Fraction(-1, 2), Fraction(0), Fraction(1, 2), Fraction(1),
    Fraction(3, 2), Fraction(2), Fraction(3),
]


def fraction_text(value):
    return str(Fraction(value))


def sphere_from_plane(u, v):
    u2 = u ** 2
    v2 = v ** 2
    sum_sq = u2 + v2
    denom = sum_sq + 1
    x = 2 * u / denom
    y = 2 * v / denom
    z = (sum_sq - 1) / denom
    return x, y, z, u2, v2, sum_sq, denom


class StereographicGenerator(ProblemGenerator):
    """
    Stereographic projection between the plane and the unit sphere,
    using the north pole and the plane z=0.

    Variants:
    - plane_to_sphere: (u,v) -> (X,Y,Z)
    - sphere_to_plane: (X,Y,Z) -> (u,v)

    Op-codes used:
    - STEREO_SETUP / FORMULA / CHECK
    - E / A / S / M / D (established/shared): exact arithmetic
    - Z: mapped point
    """

    VARIANTS = ["plane_to_sphere", "sphere_to_plane"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        u = random.choice(COORDS)
        v = random.choice(COORDS)
        if variant == "plane_to_sphere":
            problem, steps, answer = self._generate_plane_to_sphere(u, v)
        else:
            problem, steps, answer = self._generate_sphere_to_plane(u, v)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"stereographic_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_plane_to_sphere(self, u, v):
        x, y, z, u2, v2, sum_sq, denom = sphere_from_plane(u, v)
        two_u = 2 * u
        two_v = 2 * v
        z_num = sum_sq - 1
        x2 = x ** 2
        y2 = y ** 2
        z2 = z ** 2
        xy_sq = x2 + y2
        unit_sum = xy_sq + z2
        steps = [
            step("STEREO_SETUP", "plane_to_sphere",
                 f"u={fraction_text(u)}", f"v={fraction_text(v)}"),
            step("FORMULA",
                 "D=u^2+v^2+1; X=2u/D; Y=2v/D; Z=(u^2+v^2-1)/D"),
            step("E", fraction_text(u), 2, fraction_text(u2)),
            step("E", fraction_text(v), 2, fraction_text(v2)),
            step("A", fraction_text(u2), fraction_text(v2),
                 fraction_text(sum_sq)),
            step("A", fraction_text(sum_sq), 1, fraction_text(denom)),
            step("M", 2, fraction_text(u), fraction_text(two_u)),
            step("D", fraction_text(two_u), fraction_text(denom),
                 fraction_text(x)),
            step("M", 2, fraction_text(v), fraction_text(two_v)),
            step("D", fraction_text(two_v), fraction_text(denom),
                 fraction_text(y)),
            step("S", fraction_text(sum_sq), 1, fraction_text(z_num)),
            step("D", fraction_text(z_num), fraction_text(denom),
                 fraction_text(z)),
            step("E", fraction_text(x), 2, fraction_text(x2)),
            step("E", fraction_text(y), 2, fraction_text(y2)),
            step("E", fraction_text(z), 2, fraction_text(z2)),
            step("A", fraction_text(x2), fraction_text(y2),
                 fraction_text(xy_sq)),
            step("A", fraction_text(xy_sq), fraction_text(z2),
                 fraction_text(unit_sum)),
            step("CHECK", "X^2+Y^2+Z^2", fraction_text(unit_sum),
                 "unit sphere"),
        ]
        answer = (
            f"sphere point = ({fraction_text(x)}, {fraction_text(y)}, "
            f"{fraction_text(z)})"
        )
        problem = (
            f"Map plane point (u,v)=({fraction_text(u)},{fraction_text(v)}) "
            f"to the unit sphere by stereographic projection from the "
            f"north pole."
        )
        return problem, steps, answer

    def _generate_sphere_to_plane(self, u, v):
        x, y, z, _, _, _, _ = sphere_from_plane(u, v)
        denom = 1 - z
        recovered_u = x / denom
        recovered_v = y / denom
        steps = [
            step("STEREO_SETUP", "sphere_to_plane",
                 f"X={fraction_text(x)}", f"Y={fraction_text(y)}",
                 f"Z={fraction_text(z)}"),
            step("FORMULA", "u=X/(1-Z); v=Y/(1-Z)"),
            step("S", 1, fraction_text(z), fraction_text(denom)),
            step("D", fraction_text(x), fraction_text(denom),
                 fraction_text(recovered_u)),
            step("D", fraction_text(y), fraction_text(denom),
                 fraction_text(recovered_v)),
        ]
        answer = (
            f"plane point = ({fraction_text(recovered_u)}, "
            f"{fraction_text(recovered_v)})"
        )
        problem = (
            f"Map sphere point (X,Y,Z)=({fraction_text(x)},"
            f"{fraction_text(y)},{fraction_text(z)}) with Z != 1 to "
            f"the plane by inverse stereographic projection from the "
            f"north pole."
        )
        return problem, steps, answer
