import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.factor_trinomial_generator import (
    binomial,
    pair_search,
    xterm,
)


class QuadraticFactoringGenerator(ProblemGenerator):
    """
    Solves quadratics by factoring and the zero-product property.

    Variants:
    - standard:  x² + bx + c = 0 (integer roots; the trinomial search with
      its TRY/REJECT/ACCEPT trial-and-error is reused verbatim)
    - rearrange: the same, but presented as x² + bx = -c — the scratchpad
      moves everything to one side first (MOVE_TERM)
    - gcf:       ax² + bx = 0 — factor out the GCF monomial, one root is 0

    Op-codes used:
    - EQ_SETUP, MOVE_TERM, FACTOR_PAIR_GOAL, TRY, REJECT, ACCEPT
    - GCF_COEFF / GCF_VAR / GCF_RESULT (gcf variant)
    - REWRITE: factored equation (string)
    - ZERO_PRODUCT: apply the zero-product property (factored eq, split)
    - EQ_OP_BOTH / EQ_RESULT: solve each linear factor
    - CHECK: substitute each root back (method, work, expected)
    - Z: 'x = r1 or x = r2' with roots ascending (A0)
    """

    VARIANTS = ["standard", "rearrange", "gcf"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _gcf_subst_work(a, b_coef, root):
        """'6·(-3)^2 - 18·(-3) = 0' — substitute a root into ax² + bx."""
        rt = f"({root})" if root < 0 else str(root)
        val = a * root * root + b_coef * root
        sign = "+" if b_coef >= 0 else "-"
        return f"{a}·{rt}^2 {sign} {abs(b_coef)}·{rt} = {val}"

    @staticmethod
    def _subst_work(b, c, root):
        """'9^2 - 9 - 72 = 0' — substitute a root into x² + bx + c."""
        rt = f"({root})" if root < 0 else str(root)
        val = root * root + b * root + c
        sign_b = "+" if b >= 0 else "-"
        sign_c = "+" if c >= 0 else "-"
        return f"{rt}^2 {sign_b} {abs(b)}·{rt} {sign_c} {abs(c)} = {val}"

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        var = random.choice(["x", "x", "x", "y", "n"])

        if variant == "gcf":
            a = random.randint(2, 6)
            r = random.choice([v for v in range(-9, 10) if v != 0])
            # a·x² - a·r·x = 0 has roots 0 and r
            b_coef = -a * r
            lhs = f"{a}{var}^2 {xterm(b_coef, var)}"
            original = f"{lhs} = 0"
            gcf_txt = f"{a}{var}"
            inner = binomial(var, -r)
            factored = f"{gcf_txt}{inner} = 0"
            roots = sorted((0, r))
            steps = [
                step("EQ_SETUP", original),
                step("GCF_COEFF", f"{a}, {abs(b_coef)}", a),
                step("GCF_VAR", f"{var}^2, {var}", var),
                step("GCF_RESULT", gcf_txt),
                step("REWRITE", factored),
                step("ZERO_PRODUCT", factored,
                     f"{gcf_txt} = 0 or {inner.strip('()')} = 0"),
                step("EQ_OP_BOTH", "divide", a, var, 0),
                step("EQ_RESULT", var, 0),
                step("EQ_RESULT", var, r),
                step("CHECK", "substitute",
                     self._gcf_subst_work(a, b_coef, 0), "0"),
                step("CHECK", "substitute",
                     self._gcf_subst_work(a, b_coef, r), "0"),
            ]
            op = "quadratic_by_factoring_gcf"

        else:
            while True:
                p = random.choice([v for v in range(-9, 10) if v != 0])
                q = random.choice([v for v in range(-9, 10) if v != 0])
                if p != q and p + q != 0:
                    break
            b, c = -(p + q), p * q          # roots p, q of x² + bx + c
            roots = sorted((p, q))
            c_txt = f"+ {c}" if c > 0 else f"- {-c}"
            standard_form = f"{var}^2 {xterm(b, var)} {c_txt} = 0"

            steps = []
            if variant == "rearrange":
                original = f"{var}^2 {xterm(b, var)} = {-c}"
                steps.append(step("EQ_SETUP", original))
                verb_val = -c
                steps.append(step("MOVE_TERM", str(verb_val), "left",
                                  standard_form))
            else:
                original = standard_form
                steps.append(step("EQ_SETUP", original))

            pair_search(steps, c, b)
            f1, f2 = binomial(var, -roots[0]), binomial(var, -roots[1])
            factored = f"{f1}{f2} = 0"
            steps.append(step("REWRITE", factored))
            steps.append(step("ZERO_PRODUCT", factored,
                              f"{f1.strip('()')} = 0 or {f2.strip('()')} = 0"))
            steps.append(step("EQ_RESULT", var, roots[0]))
            steps.append(step("EQ_RESULT", var, roots[1]))
            for root in roots:
                steps.append(step("CHECK", "substitute",
                                  self._subst_work(b, c, root), "0"))
            op = "quadratic_by_factoring"

        answer = f"{var} = {roots[0]} or {var} = {roots[1]}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=op,
            problem=f"Solve: {original}",
            steps=steps,
            final_answer=answer,
        )
