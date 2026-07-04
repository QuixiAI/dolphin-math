import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.polynomial_long_division_generator import poly_txt


def line_txt(m, k):
    """y = mx + k with Fraction slope/intercept, tidy rendering."""
    if m == 0:
        return f"y = {k}"
    if m == 1:
        head = "y = x"
    elif m == -1:
        head = "y = -x"
    elif m.denominator == 1:
        head = f"y = {m}x"
    else:
        head = f"y = ({m})x"
    if k == 0:
        return head
    return f"{head} + {k}" if k > 0 else f"{head} - {-k}"


class TangentLineGenerator(ProblemGenerator):
    """
    Tangent and normal lines to a quadratic at a lattice point:
    evaluate f(a), differentiate, evaluate f'(a), then build the line
    from point-slope form and simplify to slope-intercept. Normal
    lines flip to the negative reciprocal first.

    Op-codes used:
    - DERIV_SETUP / POWER_RULE / REWRITE / SUBST / M / A / E / EVAL
      (established)
    - NORMAL_SLOPE: -1/f'(a) for the normal variant (work, slope)
    - DIST: expanding the point-slope form (established)
    - Z: 'y = mx + k'
    """

    VARIANTS = ["tangent", "normal"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or \
            random.choice(["tangent", "tangent", "normal"])
        while True:
            A = random.choice([1, 1, 2, -1])
            b = random.choice([v for v in range(-6, 7) if v != 0])
            c = random.randint(-8, 8)
            a_pt = random.randint(-3, 3)
            fp = 2 * A * a_pt + b       # f'(a)
            if fp != 0:
                break
        fa = A * a_pt * a_pt + b * a_pt + c
        f_txt = poly_txt([A, b, c], "x")

        wa = f"({a_pt})" if a_pt < 0 else str(a_pt)
        steps = [
            step("DERIV_SETUP", f"f(x) = {f_txt}, at x = {a_pt}",
                 f"{variant} line"),
            step("SUBST", "x", a_pt,
                 f"{'' if A == 1 else '-' if A == -1 else A}{wa}^2 "
                 f"{'+' if b > 0 else '-'} "
                 f"{'' if abs(b) == 1 else abs(b)}{wa}" +
                 (f" {'+' if c > 0 else '-'} {abs(c)}" if c else "")),
            step("E", wa, 2, a_pt * a_pt),
            step("M", A, a_pt * a_pt, A * a_pt * a_pt),
            step("M", b, a_pt, b * a_pt),
            step("A", A * a_pt * a_pt + b * a_pt, c, fa),
            step("EVAL", f"f({a_pt})", fa),
            step("POWER_RULE", f_txt, poly_txt([2 * A, b], "x")),
            step("SUBST", "x", a_pt,
                 f"{2 * A}{wa} {'+' if b > 0 else '-'} {abs(b)}"),
            step("M", 2 * A, a_pt, 2 * A * a_pt),
            step("A", 2 * A * a_pt, b, fp),
            step("EVAL", f"f'({a_pt})", fp),
        ]
        if variant == "normal":
            m = Fraction(-1, fp)
            steps.append(step("NORMAL_SLOPE", f"-1/({fp})", m))
        else:
            m = Fraction(fp)
        k = fa - m * a_pt
        wfa = f"({fa})" if fa < 0 else str(fa)
        m_txt = str(m) if m.denominator == 1 else f"({m})"
        steps.append(step("REWRITE",
                          f"y - {wfa} = {m_txt}(x - {wa})"
                          .replace(f"(x - ({a_pt}))",
                                   f"(x + {-a_pt})" if a_pt < 0
                                   else f"(x - {a_pt})")))
        steps.append(step("DIST", str(m), f"x - {a_pt}"
                          if a_pt >= 0 else f"x + {-a_pt}",
                          line_txt(m, -m * a_pt).replace("y = ", "")))
        steps.append(step("A", str(-m * a_pt), fa, str(k)))
        answer = line_txt(m, k)
        steps.append(step("REWRITE", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"{variant}_line",
            problem=(f"Find the equation of the {variant} line to "
                     f"f(x) = {f_txt} at x = {a_pt}."),
            steps=steps,
            final_answer=answer,
        )
