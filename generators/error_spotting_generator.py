import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


class ErrorSpottingGenerator(ProblemGenerator):
    """
    Critic-format problems: a worked scratchpad with exactly ONE seeded
    arithmetic mistake is given in the problem text (numbered lines, normal
    pipe dialect). Every given line after the mistake is consistent with it
    — the error propagates the way a real student's would. The task:
    verify line by line, flag the wrong one, redo the work from that point.

    Output vocabulary (see DESIGN.md "Derived Record Formats"):
    - VERIFY|k|ok — given line k re-checked and correct
    - FLAG|k|<true arithmetic, pipe-free> — given line k is the mistake
    - then ordinary op-codes redoing the work from line k
    - Z|step <k>; <correct answer> — composite answer (Principle 8)

    Error models (linear-chain skills, fully propagated):
    - two_step_equation: slip in the subtract/add step or the divide step
    - ratio_table: slip in the scale-factor multiply step
    """

    MODES = ["equation", "ratio"]

    def __init__(self, mode=None):
        if mode is not None and mode not in self.MODES:
            raise ValueError(f"mode must be one of {self.MODES} or None")
        self.mode = mode

    def generate(self) -> dict:
        mode = self.mode or random.choice(self.MODES)
        if mode == "equation":
            return self._equation_problem()
        return self._ratio_problem()

    @staticmethod
    def _render_given(problem_line, given):
        lines = [f"{i + 1}) {s}" for i, s in enumerate(given)]
        return (
            "The worked solution below contains exactly one arithmetic "
            "mistake. Check it line by line, identify the wrong line, and "
            "redo the work from that point.\n"
            f"Problem: {problem_line}\n" + "\n".join(lines))

    # ------------------------------------------------------------------

    def _equation_problem(self):
        a = random.randint(2, 9)
        x = random.choice([n for n in range(-9, 10) if n != 0])
        b = random.randint(2, 15)
        sign = random.choice(["+", "-"])
        c = a * x + b if sign == "+" else a * x - b
        rhs_ok = c - b if sign == "+" else c + b        # = a*x
        verb = "subtract" if sign == "+" else "add"
        equation = f"{a}x {sign} {b} = {c}"

        error_site = random.choice(["combine", "divide"])
        slip = random.choice([-2, -1, 1, 2])

        if error_site == "combine":
            # Student got c ∓ b wrong by a clean multiple of a (so their
            # own division still comes out whole).
            wrong_rhs = rhs_ok + slip * a
            wrong_x = x + slip
            given = [
                step("EQ_SETUP", equation),
                step("EQ_OP_BOTH", verb, b, f"{a}x", wrong_rhs),
                step("EQ_SIMPLIFY", f"{a}x = {wrong_rhs}"),
                step("EQ_OP_BOTH", "divide", a, "x", wrong_x),
                step("EQ_RESULT", "x", wrong_x),
                step("Z", wrong_x),
            ]
            k = 2
            truth = (f"{c} - {b} = {rhs_ok}, not {wrong_rhs}" if sign == "+"
                     else f"{c} + {b} = {rhs_ok}, not {wrong_rhs}")
            redo = [
                step("EQ_OP_BOTH", verb, b, f"{a}x", rhs_ok),
                step("EQ_SIMPLIFY", f"{a}x = {rhs_ok}"),
                step("EQ_OP_BOTH", "divide", a, "x", x),
                step("EQ_RESULT", "x", x),
            ]
        else:
            wrong_x = x + slip
            given = [
                step("EQ_SETUP", equation),
                step("EQ_OP_BOTH", verb, b, f"{a}x", rhs_ok),
                step("EQ_SIMPLIFY", f"{a}x = {rhs_ok}"),
                step("EQ_OP_BOTH", "divide", a, "x", wrong_x),
                step("EQ_RESULT", "x", wrong_x),
                step("Z", wrong_x),
            ]
            k = 4
            truth = f"{rhs_ok} ÷ {a} = {x}, not {wrong_x}"
            redo = [
                step("EQ_OP_BOTH", "divide", a, "x", x),
                step("EQ_RESULT", "x", x),
            ]

        answer = f"step {k}; {x}"
        steps = [step("VERIFY", i + 1, "ok") for i in range(k - 1)]
        steps.append(step("FLAG", k, truth))
        steps += redo
        xt = f"({x})" if x < 0 else str(x)
        check_val = a * x + b if sign == "+" else a * x - b
        steps.append(step("CHECK", "substitute",
                          f"{a}·{xt} {sign} {b} = {check_val}", str(c)))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="error_spotting_equation",
            problem=self._render_given(f"Solve for x: {equation}", given),
            steps=steps,
            final_answer=answer,
        )

    # ------------------------------------------------------------------

    def _ratio_problem(self):
        while True:
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            if a != b and gcd(a, b) == 1:
                break
        k_anchor, k_missing = random.sample(range(2, 13), 2)
        known = b * k_missing
        missing = a * k_missing
        pair1, pair2 = a * k_anchor, b * k_anchor
        row1 = f"Flour (cups): {pair1}, ?"
        row2 = f"Sugar (cups): {pair2}, {known}"

        error_site = random.choice(["scale", "multiply"])
        if error_site == "scale":
            # Slip in the division: wrong scale factor, multiply propagated.
            slip = random.choice([s for s in (-2, -1, 1, 2)
                                  if k_missing + s >= 1])
            k_wrong = k_missing + slip
            given = [
                step("RATIO_TABLE", row1, row2),
                step("RATIO_BASE", f"{pair1}:{pair2}", k_anchor, f"{a}:{b}"),
                step("D", known, b, k_wrong),
                step("M", a, k_wrong, a * k_wrong),
                step("Z", a * k_wrong),
            ]
            k = 3
            truth = f"{known} ÷ {b} = {k_missing}, not {k_wrong}"
            redo = [step("D", known, b, k_missing),
                    step("M", a, k_missing, missing)]
        else:
            slip = random.choice([s for s in (-2, -1, 1, 2) if a + s >= 1])
            wrong = (a + slip) * k_missing  # slip in the multiply step
            given = [
                step("RATIO_TABLE", row1, row2),
                step("RATIO_BASE", f"{pair1}:{pair2}", k_anchor, f"{a}:{b}"),
                step("D", known, b, k_missing),
                step("M", a, k_missing, wrong),
                step("Z", wrong),
            ]
            k = 4
            truth = f"{a} × {k_missing} = {missing}, not {wrong}"
            redo = [step("M", a, k_missing, missing)]

        answer = f"step {k}; {missing}"
        steps = [step("VERIFY", i + 1, "ok") for i in range(k - 1)]
        steps.append(step("FLAG", k, truth))
        steps += redo
        steps.append(step("CHECK", "cross_products",
                          f"{pair1}×{known}={pair1 * known}",
                          f"{pair2}×{missing}={pair2 * missing}"))
        steps.append(step("Z", answer))

        problem_line = ("A recipe mixes flour and sugar in a fixed ratio. "
                        "Find the missing value.\n"
                        f"{row1}\n{row2}")
        return dict(
            problem_id=jid(),
            operation="error_spotting_ratio",
            problem=self._render_given(problem_line, given),
            steps=steps,
            final_answer=answer,
        )
