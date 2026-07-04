import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


class SimilarTrianglesGenerator(ProblemGenerator):
    """
    Similar triangles: set up the ratio of corresponding sides, cross
    multiply, and solve for the missing side. A CHECK confirms the
    scale factor agrees on both known pairs (A1).

    Directions:
    - forward: the missing side is on the larger triangle
    - reverse: the missing side is on the smaller triangle

    Op-codes used:
    - SIM_SETUP: the similarity statement and known sides (given, goal)
    - PROP_SETUP: the proportion with the unknown (established)
    - CROSS_MULT: cross multiplication (equation)
    - M / D: solve (established)
    - CHECK: scale factor consistent across pairs (established)
    - Z: 'EF = 15'
    """

    def generate(self) -> dict:
        q = random.choice([1, 2, 2, 3, 4])
        p = random.choice([v for v in range(q + 1, q + 6)])
        k = Fraction(p, q)
        # small triangle sides: multiples of q, valid triangle
        while True:
            a = q * random.randint(2, 8)
            b = q * random.randint(2, 8)
            c = q * random.randint(2, 8)
            if a + b > c and a + c > b and b + c > a and \
                    len({a, b, c}) >= 2:
                break
        A, B = int(a * k), int(b * k)

        reverse = random.random() < 0.4
        if reverse:
            # know A (big), a (small), B (big); find b (small)
            given = f"DE = {A}, AB = {a}, EF = {B}"
            goal = "BC"
            prop = f"{a}/{A} = BC/{B}"
            cross = f"{A}·BC = {a}·{B}"
            num = a * B
            den = A
            missing = b
        else:
            given = f"AB = {a}, DE = {A}, BC = {b}"
            goal = "EF"
            prop = f"{a}/{A} = {b}/EF"
            cross = f"{a}·EF = {A}·{b}"
            num = A * b
            den = a
            missing = int(b * k) if not reverse else b
        assert Fraction(num, den) == missing

        scale = f"{A}/{a} = {k}, " + \
            (f"{B}/{missing} = {k}" if reverse else
             f"{missing}/{b} = {k}")
        steps = [
            step("SIM_SETUP", f"△ABC ~ △DEF; {given}", f"find {goal}"),
            step("PROP_SETUP", prop),
            step("CROSS_MULT", cross),
            step("M", num // (B if reverse else b),
                 B if reverse else b, num),
            step("D", num, den, missing),
            step("CHECK", "scale factor", scale, str(k)),
            step("Z", f"{goal} = {missing}"),
        ]

        problem = (f"Triangle ABC is similar to triangle DEF, with "
                   f"{given}. Find {goal}.")
        return dict(
            problem_id=jid(),
            operation="similar_triangles",
            problem=problem,
            steps=steps,
            final_answer=f"{goal} = {missing}",
        )
