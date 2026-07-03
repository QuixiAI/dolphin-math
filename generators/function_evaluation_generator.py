import random
from base_generator import ProblemGenerator
from helpers import step, jid


def signed(n):
    return f"({n})" if n < 0 else str(n)


class FunctionEvaluationGenerator(ProblemGenerator):
    """
    Evaluates functions from rules and from tables: f(3) = ?

    Variants:
    - linear:    f(x) = ax + b — substitute, multiply, add
    - quadratic: f(x) = ax² + bx + c — substitute, square, chain the
      arithmetic explicitly
    - table:     a value table defines f; read the entry

    Op-codes used:
    - FUNC_SETUP: the rule or table, and the evaluation target (definition,
      target)
    - SUBST: substitute the input (variable, value, resulting expression)
    - E / M / A / S: the arithmetic (established meanings)
    - TABLE_LOOKUP: read a provided table (entry, value)
    - Z: final answer
    """

    VARIANTS = ["linear", "quadratic", "table"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        fname = random.choice(["f", "g", "h"])
        var = random.choice(["x", "x", "t"])

        if variant == "table":
            xs = sorted(random.sample(range(-4, 10), 5))
            ys = random.sample(range(-15, 30), 5)
            k = random.choice(xs)
            value = ys[xs.index(k)]
            table = (f"{var}: {', '.join(str(v) for v in xs)}; "
                     f"{fname}({var}): {', '.join(str(v) for v in ys)}")
            problem = (f"The table defines {fname}. {table}. "
                       f"Find {fname}({k}).")
            steps = [
                step("FUNC_SETUP", table, f"{fname}({k})"),
                step("TABLE_LOOKUP", f"{fname}({k})", value),
                step("Z", value),
            ]
            return self._pack("function_evaluation_table", problem, steps,
                              str(value))

        k = random.choice([v for v in range(-9, 10) if v != 0])
        b = random.choice([v for v in range(-9, 10) if v != 0])
        a = random.choice([v for v in range(-5, 6) if v not in (0, 1)])
        b_txt = f"+ {b}" if b > 0 else f"- {-b}"

        if variant == "linear":
            rule = f"{fname}({var}) = {a}{var} {b_txt}"
            value = a * k + b
            steps = [
                step("FUNC_SETUP", rule, f"{fname}({k})"),
                step("SUBST", var, k, f"{a}{signed(k)} {b_txt}"),
                step("M", a, k, a * k),
                step("A", a * k, b, value),
                step("Z", value),
            ]
            return self._pack("function_evaluation_rule",
                              f"Given {rule}, find {fname}({k}).", steps,
                              str(value))

        c = random.randint(-9, 9)
        b2 = random.choice([v for v in range(-6, 7) if v != 0])
        b2_txt = f"+ {b2}{var}" if b2 > 0 else f"- {-b2}{var}"
        c_txt = f"+ {c}" if c >= 0 else f"- {-c}"
        rule = f"{fname}({var}) = {a}{var}^2 {b2_txt} {c_txt}"
        sq = k * k
        t1 = a * sq
        t2 = b2 * k
        value = t1 + t2 + c
        steps = [
            step("FUNC_SETUP", rule, f"{fname}({k})"),
            step("SUBST", var, k,
                 f"{a}{signed(k)}^2 {'+' if b2 > 0 else '-'} "
                 f"{abs(b2)}{signed(k)} {c_txt}"),
            step("E", signed(k), 2, sq),
            step("M", a, sq, t1),
            step("M", b2, k, t2),
            step("A", t1, t2, t1 + t2),
            step("A", t1 + t2, c, value),
            step("Z", value),
        ]
        return self._pack("function_evaluation_rule",
                          f"Given {rule}, find {fname}({k}).", steps,
                          str(value))

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
