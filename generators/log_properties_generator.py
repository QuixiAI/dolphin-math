import random
from base_generator import ProblemGenerator
from helpers import step, jid


def pw(v, e):
    """x^3 or bare x for exponent 1."""
    return v if e == 1 else f"{v}^{e}"


def coef_log(c, b, v, e=1):
    """3log_2(x) or log_2(x) for coefficient 1 (argument v^e)."""
    head = "" if c == 1 else str(c)
    return f"{head}log_{b}({pw(v, e)})"


class LogPropertiesGenerator(ProblemGenerator):
    """
    Log properties: expand a single log into a sum, or condense a sum
    into a single log, using the product, quotient, and power rules -
    each rule application is its own step. Numeric factors b^k are
    evaluated with the power shown.

    Variants:
    - expand:   log_b(N x^m y^n) or log_b(N x^m / y^n), N = b^k
                (N sometimes absent)
    - condense: c1·log_b(x) + c2·log_b(y) [- c3·log_b(z)]

    Op-codes used:
    - LOG_SETUP: the expression and the goal (expression, goal)
    - LOG_PRODUCT / LOG_QUOTIENT / LOG_POWER: one rule application each
      (before, after)
    - E / EVAL: numeric log evaluated via the power (established)
    - REWRITE / Z: assembled result (established)
    """

    VARIANTS = ["expand", "condense"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        b = random.choice([2, 3, 5, 10])

        if variant == "expand":
            return self._expand(b)
        return self._condense(b)

    def _expand(self, b):
        k_cap = {2: 5, 3: 4, 5: 3, 10: 3}[b]
        has_n = random.random() < 0.7
        quotient = random.random() < 0.5
        k = random.randint(1, k_cap) if has_n else 0
        N = b ** k
        m = random.randint(1, 4)
        n = random.randint(1, 4)

        num = f"{N if has_n else ''}{pw('x', m)}"
        expr = f"log_{b}({num}/{pw('y', n)})" if quotient \
            else f"log_{b}({num}{pw('y', n)})"

        steps = [step("LOG_SETUP", expr, "expand")]
        inner = f"log_{b}({num})"
        tail = f"log_{b}({pw('y', n)})"
        if quotient:
            steps.append(step("LOG_QUOTIENT", expr, f"{inner} - {tail}"))
        else:
            steps.append(step("LOG_PRODUCT", expr, f"{inner} + {tail}"))
        if has_n:
            steps.append(step("LOG_PRODUCT", inner,
                              f"log_{b}({N}) + log_{b}({pw('x', m)})"))
        if m > 1:
            steps.append(step("LOG_POWER", f"log_{b}({pw('x', m)})",
                              coef_log(m, b, "x")))
        if n > 1:
            steps.append(step("LOG_POWER", tail, coef_log(n, b, "y")))
        if has_n:
            steps.append(step("E", b, k, N))
            steps.append(step("EVAL", f"log_{b}({N})", k))

        parts = []
        if has_n:
            parts.append(str(k))
        parts.append(coef_log(m, b, "x"))
        answer = " + ".join(parts)
        answer += f" {'-' if quotient else '+'} {coef_log(n, b, 'y')}"
        steps.append(step("REWRITE", answer))
        steps.append(step("Z", answer))
        problem = f"Expand: {expr}."
        return self._pack("log_expand", problem, steps, answer)

    def _condense(self, b):
        three = random.random() < 0.5
        c1 = random.randint(1, 4)
        c2 = random.randint(1, 4)
        c3 = random.randint(1, 4)
        minus_second = (not three) and random.random() < 0.5

        t1 = coef_log(c1, b, "x")
        t2 = coef_log(c2, b, "y")
        if three:
            expr = f"{t1} + {t2} - {coef_log(c3, b, 'z')}"
        elif minus_second:
            expr = f"{t1} - {t2}"
        else:
            expr = f"{t1} + {t2}"

        steps = [step("LOG_SETUP", expr, "condense")]
        if c1 > 1:
            steps.append(step("LOG_POWER", t1,
                              f"log_{b}({pw('x', c1)})"))
        if c2 > 1:
            steps.append(step("LOG_POWER", t2,
                              f"log_{b}({pw('y', c2)})"))
        if three and c3 > 1:
            steps.append(step("LOG_POWER", coef_log(c3, b, "z"),
                              f"log_{b}({pw('z', c3)})"))

        top1, top2 = pw("x", c1), pw("y", c2)
        if three:
            steps.append(step("LOG_PRODUCT",
                              f"log_{b}({top1}) + log_{b}({top2})",
                              f"log_{b}({top1}{top2})"))
            answer = f"log_{b}({top1}{top2}/{pw('z', c3)})"
            steps.append(step("LOG_QUOTIENT",
                              f"log_{b}({top1}{top2}) - "
                              f"log_{b}({pw('z', c3)})", answer))
        elif minus_second:
            answer = f"log_{b}({top1}/{top2})"
            steps.append(step("LOG_QUOTIENT",
                              f"log_{b}({top1}) - log_{b}({top2})",
                              answer))
        else:
            answer = f"log_{b}({top1}{top2})"
            steps.append(step("LOG_PRODUCT",
                              f"log_{b}({top1}) + log_{b}({top2})",
                              answer))
        steps.append(step("Z", answer))
        problem = f"Write as a single logarithm: {expr}."
        return self._pack("log_condense", problem, steps, answer)

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
