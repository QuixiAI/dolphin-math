import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

# angle label -> exact value used for it (Principle 5: given in text)
SINES = {30: Fraction(1, 2), 37: Fraction(3, 5), 53: Fraction(4, 5),
         90: Fraction(1)}
COSINES = {60: Fraction(1, 2), 120: Fraction(-1, 2), 90: Fraction(0),
           53: Fraction(3, 5), 37: Fraction(4, 5)}


def _cos_catalog():
    """(a, b, C, cosC, c) with integer c, brute-forced once."""
    out = []
    for C, cv in COSINES.items():
        for a in range(2, 13):
            for b in range(a, 13):
                c2 = a * a + b * b - 2 * a * b * cv
                if c2.denominator != 1:
                    continue
                n = c2.numerator
                r = math.isqrt(n)
                if r * r == n and r > 0 and a + b > r and a + r > b:
                    out.append((a, b, C, cv, r))
    return out


COS_CATALOG = _cos_catalog()


class TriangleSolveGenerator(ProblemGenerator):
    """
    Law of Sines and Law of Cosines with every trig value given in the
    problem and integer results by construction. The SSA ambiguous
    case is excluded (AAS only for the sine law).

    Variants:
    - sines_aas:  two angles and a side; find the side opposite the
                  second angle via the proportion
    - cosines_side:  SAS; c² = a² + b² - 2ab cos C, c integer
    - cosines_angle: SSS; cos C = (a² + b² - c²)/(2ab), matched to the
                  given table value

    Op-codes used:
    - TRI_SETUP / THEOREM / PROP_SETUP / CROSS_MULT / TABLE_LOOKUP
      (established)
    - E / M / A / S / D: exact arithmetic (established)
    - EVAL: the found side or ratio (established)
    - Z: 'b = 12', 'c = 7', or 'C = 60°'
    """

    VARIANTS = ["sines_aas", "cosines_side", "cosines_angle"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "sines_aas":
            A, B = random.sample(list(SINES), 2)
            sA, sB = SINES[A], SINES[B]
            ratio = sB / sA
            a = ratio.denominator * random.randint(2, 8)
            b = a * ratio
            assert b.denominator == 1
            b = b.numerator
            given = (f"sin {A}° = {dec(sA)}, sin {B}° = {dec(sB)}")
            steps = [
                step("TRI_SETUP",
                     f"A = {A}°, B = {B}°, a = {a}; given {given}",
                     "side b"),
                step("THEOREM", "law of sines",
                     "a/sin A = b/sin B"),
                step("PROP_SETUP", f"{a}/{dec(sA)} = b/{dec(sB)}"),
                step("CROSS_MULT", f"{dec(sA)}·b = {a}·{dec(sB)}"),
                step("M", a, dec(sB), dec(a * sB)),
                step("D", dec(a * sB), dec(sA), b),
            ]
            answer = f"b = {b}"
            problem = (f"In triangle ABC, angle A = {A}°, angle "
                       f"B = {B}°, and side a = {a} (opposite A). "
                       f"Given {given}, find side b.")
        elif variant == "cosines_side":
            a, b, C, cv, c = random.choice(COS_CATALOG)
            given = f"cos {C}° = {dec(cv)}"
            two_ab = 2 * a * b
            prod = two_ab * cv
            steps = [
                step("TRI_SETUP",
                     f"a = {a}, b = {b}, C = {C}°; given {given}",
                     "side c"),
                step("THEOREM", "law of cosines",
                     "c^2 = a^2 + b^2 - 2ab cos C"),
                step("E", a, 2, a * a),
                step("E", b, 2, b * b),
                step("A", a * a, b * b, a * a + b * b),
                step("M", 2, a, 2 * a),
                step("M", 2 * a, b, two_ab),
                step("M", two_ab, dec(cv), dec(prod)),
                step("S", a * a + b * b, dec(prod), c * c),
                step("E", c, 2, c * c),
                step("EVAL", "c", c),
            ]
            answer = f"c = {c}"
            problem = (f"In triangle ABC, a = {a}, b = {b}, and the "
                       f"included angle C = {C}°. Given {given}, "
                       f"find side c.")
        else:
            a, b, C, cv, c = random.choice(COS_CATALOG)
            given = f"cos {C}° = {dec(cv)}"
            num = a * a + b * b - c * c
            den = 2 * a * b
            steps = [
                step("TRI_SETUP", f"a = {a}, b = {b}, c = {c}",
                     f"angle C; given {given}"),
                step("THEOREM", "law of cosines (angle form)",
                     "cos C = (a^2 + b^2 - c^2)/(2ab)"),
                step("E", a, 2, a * a),
                step("E", b, 2, b * b),
                step("E", c, 2, c * c),
                step("A", a * a, b * b, a * a + b * b),
                step("S", a * a + b * b, c * c, num),
                step("M", 2, a, 2 * a),
                step("M", 2 * a, b, den),
                step("D", num, den, dec(cv)),
                step("TABLE_LOOKUP", f"cos {C}° = {dec(cv)}",
                     f"C = {C}°"),
            ]
            answer = f"C = {C}°"
            problem = (f"In triangle ABC, a = {a}, b = {b}, and "
                       f"c = {c}. Given {given}, find angle C.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"triangle_solve_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
