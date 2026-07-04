import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.factor_trinomial_generator import binomial, pair_search
from generators.polynomial_long_division_generator import poly_txt


class LimitEvaluationGenerator(ProblemGenerator):
    """
    Limits by the standard toolbox, one technique per record.

    Variants:
    - direct:        polynomial at a point - substitute
    - factor_cancel: 0/0 rational form - detect the indeterminate
                     form, factor (pair sweep), cancel, substitute
    - rationalize:   (√(x + m²) - m)/x at 0 - multiply by the
                     conjugate, cancel, substitute
    - infinity:      rational function at ∞ by degree comparison
    - one_sided:     abs(x - a)/(x - a) from the left or right

    Op-codes used:
    - LIMIT_SETUP: the limit and the chosen technique (limit, plan)
    - CHECK: the 0/0 detection (established)
    - FACTOR_PAIR_GOAL / TRY / REJECT / ACCEPT / REWRITE / CANCEL /
      RATIONALIZE / DEGREE_COMPARE / FRAC_REDUCE (established)
    - SUBST / E / M / A / S / D: arithmetic (established)
    - Z: value, fraction, ∞, or -∞
    """

    VARIANTS = ["direct", "factor_cancel", "rationalize", "infinity",
                "one_sided"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        return getattr(self, f"_{variant}")()

    def _direct(self):
        a = random.randint(-4, 4)
        c2, c1, c0 = (random.choice([v for v in range(-5, 6) if v != 0])
                      for _ in range(3))
        expr = poly_txt([c2, c1, c0], "x")
        val = c2 * a * a + c1 * a + c0
        wa = f"({a})" if a < 0 else str(a)
        steps = [
            step("LIMIT_SETUP", f"lim x→{a} of {expr}",
                 "polynomial: direct substitution"),
            step("SUBST", "x", a,
                 f"{c2}{wa}^2 {'+' if c1 > 0 else '-'} {abs(c1)}{wa} "
                 f"{'+' if c0 > 0 else '-'} {abs(c0)}"),
            step("E", wa, 2, a * a),
            step("M", c2, a * a, c2 * a * a),
            step("M", c1, a, c1 * a),
            step("A", c2 * a * a, c1 * a, c2 * a * a + c1 * a),
            step("A", c2 * a * a + c1 * a, c0, val),
        ]
        answer = str(val)
        steps.append(step("Z", answer))
        return self._pack("limit_direct",
                          f"Evaluate lim x→{a} of {expr}.",
                          steps, answer)

    def _factor_cancel(self):
        r, s = random.sample([v for v in range(-6, 7) if v != 0], 2)
        B, C = -(r + s), r * s
        num = poly_txt([1, B, C], "x")
        den = binomial("x", -r)
        limit_txt = f"lim x→{r} of ({num})/{den}"
        steps = [
            step("LIMIT_SETUP", limit_txt, "0/0: factor and cancel"),
            step("CHECK", "substitution",
                 f"numerator and denominator are both 0 at x = {r}",
                 "indeterminate 0/0"),
        ]
        m, n = pair_search(steps, C, B)
        f1, f2 = binomial("x", m), binomial("x", n)
        # order the factors so the cancelling one is first
        if f1 != den:
            f1, f2 = f2, f1
        steps.append(step("REWRITE", f"({f1}{f2})/{den}"))
        steps.append(step("CANCEL", den, f2))
        wa = f"({r})" if r < 0 else str(r)
        steps.append(step("SUBST", "x", r, f2.replace("x", wa)[1:-1]))
        steps.append(step("A", r, -s, r - s))
        val = r - s
        answer = str(val)
        steps.append(step("Z", answer))
        return self._pack("limit_factor_cancel",
                          f"Evaluate {limit_txt}.", steps, answer)

    def _rationalize(self):
        mroot = random.randint(2, 7)
        k = mroot * mroot
        limit_txt = f"lim x→0 of (√(x + {k}) - {mroot})/x"
        steps = [
            step("LIMIT_SETUP", limit_txt, "0/0: rationalize"),
            step("CHECK", "substitution",
                 f"√{k} - {mroot} = 0 and x = 0", "indeterminate 0/0"),
            step("RATIONALIZE", f"(√(x + {k}) + {mroot})/"
                 f"(√(x + {k}) + {mroot})"),
            step("REWRITE", f"(x + {k} - {k})/"
                 f"(x(√(x + {k}) + {mroot}))"),
            step("CANCEL", "x", f"1/(√(x + {k}) + {mroot})"),
            step("SUBST", "x", 0, f"1/(√{k} + {mroot})"),
            step("EVAL", f"√{k}", mroot),
            step("A", mroot, mroot, 2 * mroot),
        ]
        answer = f"1/{2 * mroot}"
        steps.append(step("Z", answer))
        return self._pack("limit_rationalize",
                          f"Evaluate {limit_txt}.", steps, answer)

    def _infinity(self):
        kind = random.choice(["less", "equal", "greater"])
        a2 = random.choice([v for v in range(-6, 7) if v != 0])
        b2 = random.choice([v for v in range(1, 7)])
        if kind == "less":
            num = poly_txt([a2, random.randint(-5, 5)], "x")
            den = poly_txt([b2, random.randint(-5, 5),
                            random.randint(-5, 5)], "x")
            note = "deg num = 1 < deg den = 2"
            answer = "0"
        elif kind == "equal":
            num = poly_txt([a2, random.randint(-5, 5),
                            random.randint(-5, 5)], "x")
            den = poly_txt([b2, random.randint(-5, 5),
                            random.randint(-5, 5)], "x")
            note = "deg num = deg den = 2"
            answer = str(Fraction(a2, b2))
        else:
            num = poly_txt([a2, random.randint(-5, 5),
                            random.randint(-5, 5)], "x")
            den = poly_txt([b2, random.randint(-5, 5)], "x")
            note = "deg num = 2 > deg den = 1"
            answer = "∞" if a2 > 0 else "-∞"
        limit_txt = f"lim x→∞ of ({num})/({den})"
        steps = [
            step("LIMIT_SETUP", limit_txt, "compare degrees"),
            step("DEGREE_COMPARE", note,
                 answer if kind != "equal"
                 else f"ratio of leading coefficients {a2}/{b2}"),
        ]
        if kind == "equal":
            steps.append(step("D", a2, b2, answer))
        steps.append(step("Z", answer))
        return self._pack("limit_infinity",
                          f"Evaluate {limit_txt}.", steps, answer)

    def _one_sided(self):
        a = random.randint(-6, 6)
        left = random.random() < 0.5
        side = "⁻" if left else "⁺"
        inner = f"x - {a}" if a >= 0 else f"x + {-a}"
        limit_txt = f"lim x→{a}{side} of abs({inner})/({inner})"
        if left:
            reason = (f"for x < {a}, {inner} < 0, so "
                      f"abs({inner}) = -({inner})")
            answer = "-1"
        else:
            reason = (f"for x > {a}, {inner} > 0, so "
                      f"abs({inner}) = {inner}")
            answer = "1"
        steps = [
            step("LIMIT_SETUP", limit_txt,
                 f"one-sided: approach from the "
                 f"{'left' if left else 'right'}"),
            step("REWRITE", reason),
            step("CANCEL", inner, answer),
            step("Z", answer),
        ]
        return self._pack("limit_one_sided",
                          f"Evaluate {limit_txt}.", steps, answer)

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
