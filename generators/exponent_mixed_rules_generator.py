import random
from base_generator import ProblemGenerator
from helpers import step, jid


def exp_txt(e):
    """Renders an exponent: '4' or '(-2)' — parenthesized when negative."""
    return f"({e})" if e < 0 else str(e)


class ExponentMixedRulesGenerator(ProblemGenerator):
    """
    Simplifies expressions that need TWO exponent rules in sequence
    (product/quotient/power), where inputs may carry negative exponents and
    the result may come out positive, negative (rewrite as 1/x^n), or zero
    (rewrite as 1). The outcome class is sampled first so all three appear
    evenly — the finishing rule must be earned, never assumed.

    Op-codes used (shared with ExponentRulesGenerator):
    - EXP_RULE_SETUP: the expression (string)
    - EXP_RULE_IDENTIFY: rule used (rule_name, rule_formula)
    - EXP_RULE_APPLY: apply it (verb, exp1, exp2, result_exp)
    - REWRITE: current expression after a rule (string)
    - EXP_RULE_SIMPLIFY: final simplified form (string)
    - Z: final answer
    """

    BASES = ["x", "y", "a", "m", "n"]
    FORMS = ["product_quotient", "power_quotient", "power_product",
             "triple_product"]

    def __init__(self, form=None):
        if form is not None and form not in self.FORMS:
            raise ValueError(f"form must be one of {self.FORMS} or None")
        self.form = form

    def _pick_exp(self):
        """Nonzero exponent, magnitude 2..7, negative one time in three."""
        mag = random.randint(2, 7)
        return -mag if random.random() < 1 / 3 else mag

    def _final_answer(self, base, e):
        if e == 0:
            return "1"
        if e == 1:
            return base
        if e > 0:
            return f"{base}^{e}"
        return f"1/{base}" if e == -1 else f"1/{base}^{-e}"

    def generate(self) -> dict:
        form = self.form or random.choice(self.FORMS)
        base = random.choice(self.BASES)
        target = random.choice(["positive", "negative", "zero"])
        e_final = {"positive": random.randint(1, 8),
                   "negative": -random.randint(1, 8),
                   "zero": 0}[target]

        steps = []

        if form == "product_quotient":
            a, b = self._pick_exp(), self._pick_exp()
            c = a + b - e_final
            expr = f"{base}^{exp_txt(a)} · {base}^{exp_txt(b)} / {base}^{exp_txt(c)}"
            steps.append(step("EXP_RULE_SETUP", expr))
            steps.append(step("EXP_RULE_IDENTIFY", "product_rule",
                              "x^a · x^b = x^(a+b)"))
            steps.append(step("EXP_RULE_APPLY", "add", a, b, a + b))
            steps.append(step("REWRITE",
                              f"{base}^{exp_txt(a + b)} / {base}^{exp_txt(c)}"))
            steps.append(step("EXP_RULE_IDENTIFY", "quotient_rule",
                              "x^a / x^b = x^(a-b)"))
            steps.append(step("EXP_RULE_APPLY", "subtract", a + b, c, e_final))

        elif form == "power_quotient":
            a = random.choice([e for e in range(-4, 5) if e not in (0, 1)])
            b = random.choice([e for e in range(-3, 4) if e not in (0, 1)])
            c = a * b - e_final
            expr = f"({base}^{exp_txt(a)})^{exp_txt(b)} / {base}^{exp_txt(c)}"
            steps.append(step("EXP_RULE_SETUP", expr))
            steps.append(step("EXP_RULE_IDENTIFY", "power_rule",
                              "(x^a)^b = x^(ab)"))
            steps.append(step("EXP_RULE_APPLY", "multiply", a, b, a * b))
            steps.append(step("REWRITE",
                              f"{base}^{exp_txt(a * b)} / {base}^{exp_txt(c)}"))
            steps.append(step("EXP_RULE_IDENTIFY", "quotient_rule",
                              "x^a / x^b = x^(a-b)"))
            steps.append(step("EXP_RULE_APPLY", "subtract", a * b, c, e_final))

        elif form == "power_product":
            a = random.choice([e for e in range(-4, 5) if e not in (0, 1)])
            b = random.choice([e for e in range(-3, 4) if e not in (0, 1)])
            c = e_final - a * b
            expr = f"({base}^{exp_txt(a)})^{exp_txt(b)} · {base}^{exp_txt(c)}"
            steps.append(step("EXP_RULE_SETUP", expr))
            steps.append(step("EXP_RULE_IDENTIFY", "power_rule",
                              "(x^a)^b = x^(ab)"))
            steps.append(step("EXP_RULE_APPLY", "multiply", a, b, a * b))
            steps.append(step("REWRITE",
                              f"{base}^{exp_txt(a * b)} · {base}^{exp_txt(c)}"))
            steps.append(step("EXP_RULE_IDENTIFY", "product_rule",
                              "x^a · x^b = x^(a+b)"))
            steps.append(step("EXP_RULE_APPLY", "add", a * b, c, e_final))

        else:  # triple_product
            a, b = self._pick_exp(), self._pick_exp()
            c = e_final - a - b
            expr = (f"{base}^{exp_txt(a)} · {base}^{exp_txt(b)} · "
                    f"{base}^{exp_txt(c)}")
            steps.append(step("EXP_RULE_SETUP", expr))
            steps.append(step("EXP_RULE_IDENTIFY", "product_rule",
                              "x^a · x^b = x^(a+b)"))
            steps.append(step("EXP_RULE_APPLY", "add", a, b, a + b))
            steps.append(step("REWRITE",
                              f"{base}^{exp_txt(a + b)} · {base}^{exp_txt(c)}"))
            steps.append(step("EXP_RULE_IDENTIFY", "product_rule",
                              "x^a · x^b = x^(a+b)"))
            steps.append(step("EXP_RULE_APPLY", "add", a + b, c, e_final))

        steps.append(step("REWRITE", f"{base}^{exp_txt(e_final)}"))

        if e_final == 0:
            steps.append(step("EXP_RULE_IDENTIFY", "zero_exponent", "x^0 = 1"))
        elif e_final < 0:
            steps.append(step("EXP_RULE_IDENTIFY", "negative_exponent",
                              "x^(-n) = 1/x^n"))

        answer = self._final_answer(base, e_final)
        steps.append(step("EXP_RULE_SIMPLIFY", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="exponent_mixed_rules",
            problem=f"Simplify (answer with positive exponents): {expr}",
            steps=steps,
            final_answer=answer,
        )
