import random
from base_generator import ProblemGenerator
from helpers import step, jid

SQUARE_FREE = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22, 23, 26]


def signed(n):
    return f"({n})" if n < 0 else str(n)


class CompletingSquareGenerator(ProblemGenerator):
    """
    Completing the square, both uses:
    - solve:  x² + bx + c = 0 (b even) — move c, add (b/2)² to both sides,
      recognize the PST, then the square-root machinery finishes it; the
      right side may be a perfect square (integer roots) or square-free
      (exact h ± √k answers)
    - vertex: y = x² + bx + c — add and subtract (b/2)² to reach
      y = (x + h)² + v

    Op-codes used (all established except COMPLETE_SQUARE):
    - EQ_SETUP / MOVE_TERM / EQ_OP_BOTH / EQ_RESULT / REWRITE
    - COMPLETE_SQUARE: the halve-and-square move (halving work, squaring work)
    - FORM_IDENTIFY: the PST recognition (name, formula)
    - ROOT / SQRT_BOTH_SIDES / PLUS_MINUS: the square-root finish
    - CHECK: substitute back (method, work, expected)
    - Z: final answer
    """

    MODES = ["solve", "vertex"]

    def __init__(self, mode=None):
        if mode is not None and mode not in self.MODES:
            raise ValueError(f"mode must be one of {self.MODES} or None")
        self.mode = mode

    @staticmethod
    def _pst(var, h):
        """'(x + 3)^2' / '(x - 3)^2'."""
        return (f"({var} + {h})^2" if h > 0 else f"({var} - {-h})^2")

    @staticmethod
    def _lin(var, h):
        """'x + 3' / 'x - 3'."""
        return f"{var} + {h}" if h > 0 else f"{var} - {-h}"

    def generate(self) -> dict:
        mode = self.mode or random.choice(self.MODES)
        var = random.choice(["x", "x", "x", "y", "n"])
        h = random.choice([v for v in range(-8, 9) if v != 0])
        b = 2 * h
        b_txt = f"+ {b}{var}" if b > 0 else f"- {-b}{var}"
        hh = h * h

        cs_step = step("COMPLETE_SQUARE", f"half of {b} = {h}",
                       f"{signed(h)}^2 = {hh}")
        pst_step = step("FORM_IDENTIFY", "perfect_square_trinomial",
                        f"a^2 + 2ab + b^2 = (a + b)^2" if h > 0
                        else "a^2 - 2ab + b^2 = (a - b)^2")

        if mode == "vertex":
            c = random.randint(-9, 9)
            v = c - hh
            c_txt = f"+ {c}" if c >= 0 else f"- {-c}"
            original = f"y = {var}^2 {b_txt} {c_txt}"
            v_txt = f"+ {v}" if v > 0 else f"- {-v}" if v < 0 else ""
            vertex_form = f"y = {self._pst(var, h)} {v_txt}".rstrip()
            steps = [
                step("EQ_SETUP", original),
                cs_step,
                step("REWRITE",
                     f"y = ({var}^2 {b_txt} + {hh}) - {hh} {c_txt}"),
                pst_step,
                step("REWRITE", vertex_form),
                step("Z", vertex_form),
            ]
            return dict(
                problem_id=jid(),
                operation="vertex_form_by_completing_square",
                problem=f"Write in vertex form: {original}",
                steps=steps,
                final_answer=vertex_form,
            )

        # solve mode
        if random.random() < 0.6:
            r = random.randint(1, 9)
            k = r * r
            irrational = False
        else:
            k = random.choice(SQUARE_FREE)
            irrational = True
        c = hh - k
        c_txt = f"+ {c}" if c >= 0 else f"- {-c}"
        original = f"{var}^2 {b_txt} {c_txt} = 0"
        moved = f"{var}^2 {b_txt} = {-c}"
        pst_eq = f"{self._pst(var, h)} = {k}"

        steps = [step("EQ_SETUP", original)]
        if c != 0:
            steps.append(step("MOVE_TERM", str(c), "right", moved))
        steps.append(cs_step)
        steps.append(step("EQ_OP_BOTH", "add", hh, f"{var}^2 {b_txt}",
                          -c + hh))
        steps.append(step("REWRITE", f"{var}^2 {b_txt} + {hh} = {k}"))
        steps.append(pst_step)
        steps.append(step("REWRITE", pst_eq))

        lin = self._lin(var, h)
        verb = "subtract" if h > 0 else "add"
        if irrational:
            steps.append(step("SQRT_BOTH_SIDES", pst_eq,
                              f"{lin} = ±√{k}"))
            steps.append(step("PLUS_MINUS", f"{lin} = ±√{k}",
                              f"{lin} = √{k} or {lin} = -√{k}"))
            lo = f"{-h} - √{k}"
            hi = f"{-h} + √{k}"
            steps.append(step("CHECK", "substitute",
                              f"(√{k})^2 = {k}", str(k)))
            answer = f"{var} = {lo} or {var} = {hi}"
        else:
            r = int(k ** 0.5)
            roots = sorted((-h - r, -h + r))
            steps.append(step("ROOT", k, r))
            steps.append(step("SQRT_BOTH_SIDES", pst_eq, f"{lin} = ±{r}"))
            steps.append(step("PLUS_MINUS", f"{lin} = ±{r}",
                              f"{lin} = {r} or {lin} = -{r}"))
            steps.append(step("EQ_OP_BOTH", verb, abs(h), var, -h + r))
            steps.append(step("EQ_RESULT", var, -h + r))
            steps.append(step("EQ_OP_BOTH", verb, abs(h), var, -h - r))
            steps.append(step("EQ_RESULT", var, -h - r))
            for root in roots:
                val = root * root + b * root + c
                sign_b = "+" if b >= 0 else "-"
                sign_c = "+" if c >= 0 else "-"
                steps.append(step(
                    "CHECK", "substitute",
                    f"{signed(root)}^2 {sign_b} {abs(b)}·{signed(root)} "
                    f"{sign_c} {abs(c)} = {val}", "0"))
            answer = f"{var} = {roots[0]} or {var} = {roots[1]}"

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="completing_the_square",
            problem=f"Solve by completing the square: {original}",
            steps=steps,
            final_answer=answer,
        )
