import random
from base_generator import ProblemGenerator
from helpers import step, jid


def lin_n(a, b):
    """Renders an + b sign-aware with variable n."""
    head = {1: "n", -1: "-n"}.get(a, f"{a}n")
    if b == 0:
        return head
    return f"{head} + {b}" if b > 0 else f"{head} - {-b}"


def geo_txt(a, r):
    """Renders a·r^(n-1), parenthesizing a negative ratio."""
    rt = f"({r})" if r < 0 else str(r)
    return f"{a}·{rt}^(n-1)"


class RecursiveExplicitGenerator(ProblemGenerator):
    """
    Converts between recursive and explicit sequence definitions, both
    directions, for arithmetic and geometric sequences.

    Recursive -> explicit: unroll the first four terms by hand, name the
    pattern, apply the closed form, simplify, and check one term against
    the unrolled list. Explicit -> recursive: compute a_1 and a_2 from
    the formula, extract d (or r), state the recursion, and check a_3
    both ways.

    Op-codes used:
    - SEQ_SETUP: the given definition and the goal
    - A / S / M / D / E / SUBST / EVAL / DIST: arithmetic (established)
    - UNROLL: the terms produced so far and the pattern they reveal
      (terms, classification)
    - COMMON_DIFF / COMMON_RATIO: extracted from computed terms
    - SEQ_FORMULA / SEQ_APPLY / REWRITE: closed form work (established)
    - CHECK: one term computed from both representations (established)
    - Z: the converted definition
    """

    VARIANTS = ["rec_to_exp_arith", "rec_to_exp_geo",
                "exp_to_rec_arith", "exp_to_rec_geo"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        return getattr(self, f"_{variant}")()

    def _rec_to_exp_arith(self):
        a1 = random.randint(-9, 9)
        d = random.choice([v for v in range(-9, 10) if v not in (-1, 0, 1)])
        terms = [a1 + i * d for i in range(4)]
        rec_rule = f"a_n = a_(n-1) + {d}" if d > 0 \
            else f"a_n = a_(n-1) - {-d}"
        const = a1 - d
        answer = f"a_n = {lin_n(d, const)}"
        steps = [step("SEQ_SETUP", f"a_1 = {a1}; {rec_rule}",
                      "explicit formula")]
        for i in range(3):
            steps.append(step("A", terms[i], d, terms[i + 1]))
        steps.append(step("UNROLL", ", ".join(str(v) for v in terms),
                          f"arithmetic, d = {d}"))
        steps.append(step("SEQ_FORMULA", "a_n = a_1 + (n - 1)d"))
        steps.append(step("SEQ_APPLY", f"a_n = {a1} + (n - 1)·{d}"))
        steps.append(step("DIST", d, "n - 1", lin_n(d, -d)))
        steps.append(step("A", a1, -d, const))
        steps.append(step("REWRITE", answer))
        check_val = d * 4 + const
        steps.append(step("CHECK", "term 4",
                          f"{d}·4 {'+' if const >= 0 else '-'} "
                          f"{abs(const)} = {check_val}", terms[3]))
        steps.append(step("Z", answer))
        problem = (f"The sequence is defined by a_1 = {a1} and {rec_rule} "
                   f"for n > 1. Write an explicit formula for a_n.")
        return self._pack("recursive_to_explicit", problem, steps, answer)

    def _rec_to_exp_geo(self):
        a1 = random.choice([v for v in range(-6, 7) if v != 0])
        r = random.choice([2, 3, 4, -2])
        terms = [a1 * r ** i for i in range(4)]
        rec_rule = f"a_n = {r}·a_(n-1)"
        answer = f"a_n = {geo_txt(a1, r)}"
        steps = [step("SEQ_SETUP", f"a_1 = {a1}; {rec_rule}",
                      "explicit formula")]
        for i in range(3):
            steps.append(step("M", r, terms[i], terms[i + 1]))
        steps.append(step("UNROLL", ", ".join(str(v) for v in terms),
                          f"geometric, r = {r}"))
        steps.append(step("SEQ_FORMULA", "a_n = a_1·r^(n - 1)"))
        steps.append(step("SEQ_APPLY", answer))
        rt = f"({r})" if r < 0 else str(r)
        steps.append(step("CHECK", "term 4",
                          f"{a1}·{rt}^3 = {terms[3]}", terms[3]))
        steps.append(step("Z", answer))
        problem = (f"The sequence is defined by a_1 = {a1} and {rec_rule} "
                   f"for n > 1. Write an explicit formula for a_n.")
        return self._pack("recursive_to_explicit", problem, steps, answer)

    def _exp_to_rec_arith(self):
        d = random.choice([v for v in range(-9, 10) if v not in (-1, 0, 1)])
        const = random.randint(-9, 9)
        a1, a2, a3 = d + const, 2 * d + const, 3 * d + const
        formula = f"a_n = {lin_n(d, const)}"
        rec = (f"a_1 = {a1}; a_n = a_(n-1) + {d}" if d > 0
               else f"a_1 = {a1}; a_n = a_(n-1) - {-d}")
        steps = [step("SEQ_SETUP", formula, "recursive definition")]
        for n, val in ((1, a1), (2, a2)):
            steps.append(step("SUBST", "n", n,
                              f"{d}({n}) {'+' if const >= 0 else '-'} "
                              f"{abs(const)}"))
            steps.append(step("M", d, n, d * n))
            steps.append(step("A", d * n, const, val))
            steps.append(step("EVAL", f"a_{n}", val))
        steps.append(step("COMMON_DIFF",
                          f"{a2} - {f'({a1})' if a1 < 0 else a1}", d))
        steps.append(step("REWRITE", rec))
        steps.append(step("CHECK", "term 3",
                          f"explicit {d}·3 "
                          f"{'+' if const >= 0 else '-'} {abs(const)} = "
                          f"{a3}, recursion {a2} "
                          f"{'+' if d > 0 else '-'} {abs(d)} = {a3}", a3))
        steps.append(step("Z", rec))
        problem = (f"The sequence is defined by {formula}. "
                   f"Write a recursive definition.")
        return self._pack("explicit_to_recursive", problem, steps, rec)

    def _exp_to_rec_geo(self):
        a = random.choice([v for v in range(-6, 7) if v != 0])
        r = random.choice([2, 3, 4, -2])
        a1, a2, a3 = a, a * r, a * r * r
        formula = f"a_n = {geo_txt(a, r)}"
        rec = f"a_1 = {a1}; a_n = {r}·a_(n-1)"
        rt = f"({r})" if r < 0 else str(r)
        steps = [step("SEQ_SETUP", formula, "recursive definition")]
        for n, val in ((1, a1), (2, a2)):
            steps.append(step("SUBST", "n", n, f"{a}·{rt}^{n - 1}"))
            steps.append(step("E", rt, n - 1, r ** (n - 1)))
            steps.append(step("M", a, r ** (n - 1), val))
            steps.append(step("EVAL", f"a_{n}", val))
        steps.append(step("COMMON_RATIO",
                          f"{a2}/{f'({a1})' if a1 < 0 else a1}", r))
        steps.append(step("REWRITE", rec))
        steps.append(step("CHECK", "term 3",
                          f"explicit {a}·{rt}^2 = {a3}, "
                          f"recursion {r}·{a2} = {a3}", a3))
        steps.append(step("Z", rec))
        problem = (f"The sequence is defined by {formula}. "
                   f"Write a recursive definition.")
        return self._pack("explicit_to_recursive", problem, steps, rec)

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
