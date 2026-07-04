import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.geometric_mean_generator import sqrt_txt

TRIPLES_2D = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17),
              (9, 12, 15), (7, 24, 25)]


def vec(comps):
    return "⟨" + ", ".join(str(c) for c in comps) + "⟩"


class VectorOpsGenerator(ProblemGenerator):
    """
    Vector arithmetic in components: linear combinations a·u + b·v
    worked component by component, magnitudes via the root of the sum
    of squares, and unit vectors from Pythagorean-triple vectors so the
    components come out as exact fractions.

    Op-codes used:
    - VEC_SETUP: the vectors and the goal (given, goal)
    - M / A / S / E / D: component arithmetic (established)
    - REWRITE: each scaled vector, written out (established)
    - MAG_FORMULA: magnitude = √(x² + y² [+ z²])
    - ROOT_SIMPLIFY / FRAC_REDUCE: exact forms (established)
    - Z: vector, scalar, or unit vector
    """

    VARIANTS = ["combine", "magnitude", "unit_vector"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "combine":
            u = [random.randint(-6, 6) for _ in range(2)]
            v = [random.randint(-6, 6) for _ in range(2)]
            a = random.choice([2, 3, 4, 5])
            b = random.choice([2, 3, 4, 5])
            minus = random.random() < 0.5
            op = "-" if minus else "+"
            au = [a * c for c in u]
            bv = [b * c for c in v]
            res = [au[i] - bv[i] if minus else au[i] + bv[i]
                   for i in range(2)]
            expr = f"{a}u {op} {b}v"
            steps = [step("VEC_SETUP", f"u = {vec(u)}, v = {vec(v)}",
                          expr)]
            for i in range(2):
                steps.append(step("M", a, u[i], au[i]))
            steps.append(step("REWRITE", f"{a}u = {vec(au)}"))
            for i in range(2):
                steps.append(step("M", b, v[i], bv[i]))
            steps.append(step("REWRITE", f"{b}v = {vec(bv)}"))
            for i in range(2):
                steps.append(step("S" if minus else "A", au[i], bv[i],
                                  res[i]))
            answer = vec(res)
            steps.append(step("Z", answer))
            problem = (f"Given u = {vec(u)} and v = {vec(v)}, "
                       f"compute {expr}.")
        elif variant == "magnitude":
            three_d = random.random() < 0.3
            n = 3 if three_d else 2
            comps = [random.randint(-7, 7) for _ in range(n)]
            if all(c == 0 for c in comps):
                return self.generate()
            total = sum(c * c for c in comps)
            steps = [step("VEC_SETUP", f"v = {vec(comps)}",
                          "magnitude"),
                     step("MAG_FORMULA",
                          "magnitude = √(" +
                          " + ".join(f"{ax}^2" for ax in
                                     "xyz"[:n]) + ")")]
            for c in comps:
                steps.append(step("E", f"({c})" if c < 0 else str(c),
                                  2, c * c))
            acc = comps[0] ** 2
            for c in comps[1:]:
                steps.append(step("A", acc, c * c, acc + c * c))
                acc += c * c
            val = sqrt_txt(total)
            if "√" in val:
                steps.append(step("ROOT_SIMPLIFY", f"√{total} = {val}"))
            else:
                steps.append(step("E", val, 2, total))
            answer = val
            steps.append(step("Z", answer))
            problem = (f"Find the magnitude of v = {vec(comps)}. "
                       f"Give an exact answer.")
        else:
            a, b, c = random.choice(TRIPLES_2D)
            k = random.choice([1, 1, 2])
            sx = random.choice([1, -1])
            sy = random.choice([1, -1])
            comps = [sx * a * k, sy * b * k]
            mag = c * k
            ux = Fraction(comps[0], mag)
            uy = Fraction(comps[1], mag)
            steps = [
                step("VEC_SETUP", f"v = {vec(comps)}", "unit vector"),
                step("MAG_FORMULA", "magnitude = √(x^2 + y^2)"),
                step("E", f"({comps[0]})" if comps[0] < 0
                     else str(comps[0]), 2, comps[0] ** 2),
                step("E", f"({comps[1]})" if comps[1] < 0
                     else str(comps[1]), 2, comps[1] ** 2),
                step("A", comps[0] ** 2, comps[1] ** 2, mag * mag),
                step("E", mag, 2, mag * mag),
                step("EVAL", "magnitude", mag),
                step("D", comps[0], mag, ux),
                step("D", comps[1], mag, uy),
            ]
            answer = f"⟨{ux}, {uy}⟩"
            steps.append(step("Z", answer))
            problem = (f"Find the unit vector in the direction of "
                       f"v = {vec(comps)}.")

        return dict(
            problem_id=jid(),
            operation=f"vector_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
