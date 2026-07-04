import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.polynomial_long_division_generator import poly_txt


class MeanValueTheoremGenerator(ProblemGenerator):
    """
    MVT and IVT applications.

    Variants:
    - mvt: for a quadratic on [a, b], compute the average slope from
      both endpoint values, set f'(c) equal to it, and solve - the c
      lands at the interval midpoint, checked to lie inside
    - ivt: evaluate the endpoints and either certify a root by sign
      change or report the test inconclusive when signs agree

    Op-codes used:
    - MVT_SETUP / IVT_SETUP: the function, interval, and question
    - SUBST / E / M / A / S / D / EVAL (established)
    - THEOREM / POWER_RULE / EQ_OP_BOTH / CHECK (established)
    - Z: 'c = 3', or the IVT verdict
    """

    VARIANTS = ["mvt", "ivt"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _eval_quad(steps, b, c, x):
        wa = f"({x})" if x < 0 else str(x)
        fx = x * x + b * x + c
        steps.append(step("SUBST", "x", x,
                          f"{wa}^2 {'+' if b > 0 else '-'} "
                          f"{'' if abs(b) == 1 else abs(b)}{wa}" +
                          (f" {'+' if c > 0 else '-'} {abs(c)}"
                           if c else "")))
        steps.append(step("E", wa, 2, x * x))
        steps.append(step("M", b, x, b * x))
        steps.append(step("A", x * x + b * x, c, fx))
        steps.append(step("EVAL", f"f({x})", fx))
        return fx

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "mvt":
            b = random.choice([v for v in range(-6, 7) if v != 0])
            c = random.randint(-8, 8)
            a1 = random.randint(-4, 2)
            a2 = a1 + 2 * random.randint(1, 4)
            mid = (a1 + a2) // 2
            f_txt = poly_txt([1, b, c], "x")
            steps = [step("MVT_SETUP",
                          f"f(x) = {f_txt} on [{a1}, {a2}]",
                          "find the c guaranteed by the MVT")]
            f1 = self._eval_quad(steps, b, c, a1)
            f2 = self._eval_quad(steps, b, c, a2)
            slope = (f2 - f1) // (a2 - a1)
            steps.append(step("S", f2, f1, f2 - f1))
            steps.append(step("S", a2, a1, a2 - a1))
            steps.append(step("D", f2 - f1, a2 - a1, slope))
            steps.append(step("THEOREM", "Mean Value Theorem",
                              f"some c in ({a1}, {a2}) has "
                              f"f'(c) = {slope}"))
            steps.append(step("POWER_RULE", f_txt,
                              poly_txt([2, b], "x")))
            steps.append(step("EQ_OP_BOTH",
                              "subtract" if b > 0 else "add", abs(b),
                              "2c", slope - b))
            steps.append(step("D", slope - b, 2, mid))
            steps.append(step("CHECK", "c inside the interval",
                              f"{a1} < {mid} < {a2}", "valid"))
            answer = f"c = {mid}"
            problem = (f"Find the value c guaranteed by the Mean Value "
                       f"Theorem for f(x) = {f_txt} on [{a1}, {a2}].")
        else:
            while True:
                b = random.choice([v for v in range(-4, 5) if v != 0])
                c = random.randint(-9, 9)
                a1 = random.randint(-4, 2)
                a2 = a1 + random.randint(1, 4)
                f1 = a1 ** 3 + b * a1 + c
                f2 = a2 ** 3 + b * a2 + c
                if f1 != 0 and f2 != 0:
                    break
            f_txt = poly_txt([1, 0, b, c], "x")
            steps = [step("IVT_SETUP",
                          f"f(x) = {f_txt} on [{a1}, {a2}]",
                          "does the IVT guarantee a root?")]
            for x, fx in ((a1, f1), (a2, f2)):
                wa = f"({x})" if x < 0 else str(x)
                steps.append(step("SUBST", "x", x,
                                  f"{wa}^3 {'+' if b > 0 else '-'} "
                                  f"{'' if abs(b) == 1 else abs(b)}"
                                  f"{wa}" +
                                  (f" {'+' if c > 0 else '-'} {abs(c)}"
                                   if c else "")))
                steps.append(step("E", wa, 3, x ** 3))
                steps.append(step("M", b, x, b * x))
                steps.append(step("A", x ** 3 + b * x, c, fx))
                steps.append(step("EVAL", f"f({x})", fx))
            if f1 * f2 < 0:
                lo, hi = (f1, f2) if f1 < 0 else (f2, f1)
                steps.append(step("CHECK", "sign change",
                                  f"one endpoint is negative and the "
                                  f"other positive", "opposite signs"))
                steps.append(step("THEOREM",
                                  "Intermediate Value Theorem",
                                  "a continuous function takes every "
                                  "value between its endpoint values"))
                answer = f"Yes — a root exists in ({a1}, {a2})"
            else:
                steps.append(step("CHECK", "sign change",
                                  f"f({a1}) and f({a2}) have the same "
                                  f"sign", "no sign change"))
                answer = ("Inconclusive — the IVT does not guarantee "
                          "a root here")
            steps.append(step("Z", answer))
            problem = (f"Does the Intermediate Value Theorem guarantee "
                       f"that f(x) = {f_txt} has a root in "
                       f"[{a1}, {a2}]?")
            return self._pack("ivt_application", problem, steps, answer)
        steps.append(step("Z", answer))
        return self._pack("mvt_application", problem, steps, answer)

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
