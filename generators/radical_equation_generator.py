import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.factor_trinomial_generator import pair_search, xterm


def isqrt(n):
    r = int(n ** 0.5)
    while r * r < n:
        r += 1
    return r


class RadicalEquationGenerator(ProblemGenerator):
    """
    Solves radical equations. Squaring both sides produces CANDIDATES, not
    solutions — every candidate is tested in the ORIGINAL equation with
    TRY/ACCEPT/REJECT, and extraneous roots are rejected with the
    disagreement shown (the A1 discipline this skill exists to teach).

    Variants:
    - simple:      √(ax + b) = c — squaring gives a linear solve, always valid
    - one_extraneous: √(x + k) = x + m — the quadratic yields one valid and
      one extraneous candidate
    - both_valid:  the adjacent-root case where both candidates survive
    - no_solution: √(ax + b) = negative — impossible before any algebra

    Op-codes used:
    - EQ_SETUP / MOVE_TERM / REWRITE / EQ_OP_BOTH / EQ_RESULT (established)
    - SQUARE_BOTH_SIDES: square both sides (before, after)
    - E: expand the squared binomial (base, 2, expansion)
    - FACTOR_PAIR_GOAL / TRY / REJECT / ACCEPT + ZERO_PRODUCT (established)
    - SPECIAL_SOLUTION: the impossible case (equation, classification)
    - Z: final answer
    """

    VARIANTS = ["simple", "one_extraneous", "both_valid", "no_solution"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choices(
            self.VARIANTS, weights=[25, 35, 25, 15])[0]
        return getattr(self, f"_{variant}")()

    @staticmethod
    def _rad_arg(k, var="x"):
        return f"{var} + {k}" if k >= 0 else f"{var} - {-k}"

    def _simple(self):
        a = random.randint(2, 6)
        x0 = random.randint(-6, 9)
        c = random.randint(1, 9)
        b = c * c - a * x0
        arg = f"{a}x + {b}" if b >= 0 else f"{a}x - {-b}"
        original = f"√({arg}) = {c}"
        steps = [
            step("EQ_SETUP", original),
            step("SQUARE_BOTH_SIDES", original, f"{arg} = {c * c}"),
            step("EQ_OP_BOTH", "subtract" if b >= 0 else "add", abs(b),
                 f"{a}x", c * c - b),
            step("EQ_OP_BOTH", "divide", a, "x", x0),
            step("EQ_RESULT", "x", x0),
            step("TRY", f"x = {x0}",
                 f"lhs: √{a * x0 + b} = {c}, rhs: {c}"),
            step("ACCEPT", f"x = {x0}", f"both sides {c} ✓"),
            step("Z", f"x = {x0}"),
        ]
        return self._pack(original, steps, f"x = {x0}")

    def _no_solution(self):
        a = random.randint(2, 6)
        b = random.randint(1, 15)
        c = -random.randint(1, 9)
        original = f"√({a}x + {b}) = {c}"
        steps = [
            step("EQ_SETUP", original),
            step("SPECIAL_SOLUTION", original,
                 "contradiction: a square root cannot be negative"),
            step("Z", "No solution"),
        ]
        return self._pack(original, steps, "No solution")

    def _quadratic_family(self, r, s, a_in=1):
        """√(a·x + k) = x + m built from valid root r with r + m = s ≥ 0."""
        m = s - r
        k = s * s - a_in * r
        other = a_in - 2 * m - r       # the second candidate root
        var = "x"

        arg = (self._rad_arg(k) if a_in == 1 else
               (f"{a_in}x + {k}" if k >= 0 else f"{a_in}x - {-k}"))
        rhs = f"x + {m}" if m >= 0 else f"x - {-m}"
        original = f"√({arg}) = {rhs}"

        # squared: ax + k = x² + 2m x + m²  →  x² + (2m−a)x + (m²−k) = 0
        b_coef = 2 * m - a_in
        c_coef = m * m - k
        exp_txt = (f"x^2 {xterm(2 * m, var)} + {m * m}" if m != 0
                   else "x^2")
        std = f"x^2 {xterm(b_coef, var)} "
        std += f"+ {c_coef} = 0" if c_coef >= 0 else f"- {-c_coef} = 0"

        steps = [
            step("EQ_SETUP", original),
            step("SQUARE_BOTH_SIDES", original,
                 f"{arg} = ({rhs})^2"),
            step("E", f"({rhs})", 2, exp_txt),
            step("REWRITE", f"{arg} = {exp_txt}"),
            step("MOVE_TERM", arg, "right", std),
        ]
        pair_search(steps, c_coef, b_coef)
        lo, hi = sorted((r, other))
        b1 = f"(x + {-lo})" if lo < 0 else f"(x - {lo})"
        b2 = f"(x + {-hi})" if hi < 0 else f"(x - {hi})"
        factored = f"{b1}{b2} = 0"
        steps.append(step("REWRITE", factored))
        steps.append(step("ZERO_PRODUCT", factored,
                          f"x = {lo} or x = {hi}"))

        valid = []
        for cand in (lo, hi):
            lhs_val = isqrt(a_in * cand + k)
            rhs_val = cand + m
            work = f"lhs: √{a_in * cand + k} = {lhs_val}, rhs: {rhs_val}"
            steps.append(step("TRY", f"x = {cand}", work))
            if lhs_val == rhs_val:
                steps.append(step("ACCEPT", f"x = {cand}",
                                  f"both sides {lhs_val} ✓"))
                valid.append(cand)
            else:
                steps.append(step("REJECT", f"x = {cand}",
                                  f"{lhs_val} ≠ {rhs_val}, extraneous"))

        if len(valid) == 2:
            answer = f"x = {valid[0]} or x = {valid[1]}"
        else:
            answer = f"x = {valid[0]}"
        steps.append(step("Z", answer))
        return self._pack(original, steps, answer)

    def _one_extraneous(self):
        # a=1: the second candidate's rhs value is 1−s, so s ≥ 2 forces it
        # negative → extraneous.
        while True:
            r = random.randint(0, 8)
            s = random.randint(2, 9)
            m = s - r
            other = 1 - 2 * m - r
            c_coef = m * m - (s * s - r)
            if (other != r and c_coef != 0 and 2 * m != 1
                    and abs(c_coef) <= 81):
                return self._quadratic_family(r, s, a_in=1)

    def _both_valid(self):
        # a=2: the second candidate's rhs value is 2−s, so s ∈ {0, 2} keeps
        # both candidates valid (s=1 would be a double root).
        while True:
            r = random.randint(1, 12)
            a_in = random.choice([2, 3])
            s = random.randint(0, a_in)
            if 2 * s == a_in:            # double root
                continue
            m = s - r
            b_coef = 2 * m - a_in
            c_coef = m * m - (s * s - a_in * r)
            other = a_in - 2 * m - r
            if b_coef == 0 or c_coef == 0 or other == r:
                continue
            return self._quadratic_family(r, s, a_in=a_in)

    @staticmethod
    def _pack(original, steps, answer):
        return dict(
            problem_id=jid(),
            operation="radical_equation",
            problem=f"Solve: {original}",
            steps=steps,
            final_answer=answer,
        )
