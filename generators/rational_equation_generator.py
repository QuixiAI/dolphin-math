import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


class RationalEquationGenerator(ProblemGenerator):
    """
    Solves rational equations. The domain restriction is noted FIRST, the
    denominators are cleared, and every candidate is tested against the
    original — a candidate equal to a restricted value is rejected as
    extraneous, even when it is the only candidate (No solution).

    Variants:
    - proportion:  a/x = b/c — cross multiply, one valid solution
    - sum_form:    a/x + b = c — isolate and solve, one valid solution
    - no_solution: (x + c)/(x − r) = (r + c)/(x − r) — the only candidate
      is the restricted value r
    - mixed:       x²/(x − r) = r²/(x − r) — candidates ±r; r is extraneous

    Op-codes used:
    - EQ_SETUP / REWRITE / EQ_OP_BOTH / EQ_RESULT (established)
    - DOMAIN_NOTE: the restriction and why (restriction, reason)
    - FORM_IDENTIFY: cross-multiplication rule (name, formula)
    - MUL_TERM: multiply one side by the LCD (factor, term, result)
    - M: cross-multiplication arithmetic (a, c, product)
    - SQRT_BOTH_SIDES / PLUS_MINUS: the x² = r² finish (mixed variant)
    - TRY / ACCEPT / REJECT: test candidates against the original
    - Z: 'x = v' or 'No solution'
    """

    VARIANTS = ["proportion", "sum_form", "no_solution", "mixed"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        return getattr(self, f"_{variant}")()

    def _proportion(self):
        while True:
            x0 = random.choice([v for v in range(-12, 13) if v != 0])
            b = random.randint(2, 9)
            product = b * x0
            divisors = [d for d in range(2, 10)
                        if product % d == 0 and product // d != 0]
            if divisors:
                a = random.choice(divisors)
                c = product // a
                break
        original = f"{a}/x = {b}/{c}"
        steps = [
            step("EQ_SETUP", original),
            step("DOMAIN_NOTE", "x ≠ 0", "denominator cannot be zero"),
            step("FORM_IDENTIFY", "cross_multiply", "a/b = c/d → ad = bc"),
            step("M", a, c, a * c),
            step("REWRITE", f"{b}x = {a * c}"),
            step("EQ_OP_BOTH", "divide", b, "x", x0),
            step("EQ_RESULT", "x", x0),
            step("TRY", f"x = {x0}",
                 f"lhs: {Fraction(a, x0)}, rhs: {Fraction(b, c)}"),
            step("ACCEPT", f"x = {x0}", f"both sides {Fraction(a, x0)} ✓"),
            step("Z", f"x = {x0}"),
        ]
        return self._pack(original, steps, f"x = {x0}")

    def _sum_form(self):
        while True:
            x0 = random.choice([v for v in range(-12, 13) if v != 0])
            d = random.choice([v for v in range(-6, 7) if v != 0])
            a = d * x0
            if abs(a) <= 60:
                break
        b = random.randint(1, 9)
        c = b + d
        b_txt = f"+ {b}"
        original = f"{a}/x {b_txt} = {c}"
        steps = [
            step("EQ_SETUP", original),
            step("DOMAIN_NOTE", "x ≠ 0", "denominator cannot be zero"),
            step("EQ_OP_BOTH", "subtract", b, f"{a}/x", d),
            step("REWRITE", f"{a}/x = {d}"),
            step("MUL_TERM", "x", f"{a}/x", str(a)),
            step("REWRITE", f"{a} = {d}x"),
            step("EQ_OP_BOTH", "divide", d, "x", x0),
            step("EQ_RESULT", "x", x0),
            step("TRY", f"x = {x0}",
                 f"lhs: {Fraction(a, x0) + b}, rhs: {c}"),
            step("ACCEPT", f"x = {x0}", f"both sides {c} ✓"),
            step("Z", f"x = {x0}"),
        ]
        return self._pack(original, steps, f"x = {x0}")

    def _no_solution(self):
        r = random.choice([v for v in range(-8, 9) if v != 0])
        c = random.randint(1, 9)
        den = f"x - {r}" if r > 0 else f"x + {-r}"
        rhs_num = r + c
        original = f"(x + {c})/({den}) = {rhs_num}/({den})"
        steps = [
            step("EQ_SETUP", original),
            step("DOMAIN_NOTE", f"x ≠ {r}", "denominator cannot be zero"),
            step("MUL_TERM", f"({den})", f"(x + {c})/({den})", f"x + {c}"),
            step("MUL_TERM", f"({den})", f"{rhs_num}/({den})", str(rhs_num)),
            step("REWRITE", f"x + {c} = {rhs_num}"),
            step("EQ_OP_BOTH", "subtract", c, "x", r),
            step("EQ_RESULT", "x", r),
            step("TRY", f"x = {r}",
                 f"x = {r} makes {den} = 0"),
            step("REJECT", f"x = {r}",
                 "makes a denominator zero — extraneous"),
            step("Z", "No solution"),
        ]
        return self._pack(original, steps, "No solution")

    def _mixed(self):
        r = random.randint(2, 9)
        den = f"x - {r}"
        original = f"x^2/({den}) = {r * r}/({den})"
        steps = [
            step("EQ_SETUP", original),
            step("DOMAIN_NOTE", f"x ≠ {r}", "denominator cannot be zero"),
            step("MUL_TERM", f"({den})", f"x^2/({den})", "x^2"),
            step("MUL_TERM", f"({den})", f"{r * r}/({den})", str(r * r)),
            step("REWRITE", f"x^2 = {r * r}"),
            step("ROOT", r * r, r),
            step("SQRT_BOTH_SIDES", f"x^2 = {r * r}", f"x = ±{r}"),
            step("PLUS_MINUS", f"x = ±{r}", f"x = {r} or x = {-r}"),
            step("TRY", f"x = {r}", f"x = {r} makes {den} = 0"),
            step("REJECT", f"x = {r}",
                 "makes a denominator zero — extraneous"),
            step("TRY", f"x = {-r}",
                 f"lhs: {Fraction(r * r, -2 * r)}, "
                 f"rhs: {Fraction(r * r, -2 * r)}"),
            step("ACCEPT", f"x = {-r}",
                 f"both sides {Fraction(r * r, -2 * r)} ✓"),
            step("Z", f"x = {-r}"),
        ]
        return self._pack(original, steps, f"x = {-r}")

    @staticmethod
    def _pack(original, steps, answer):
        return dict(
            problem_id=jid(),
            operation="rational_equation",
            problem=f"Solve: {original}",
            steps=steps,
            final_answer=answer,
        )
