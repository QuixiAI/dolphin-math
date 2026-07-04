import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


class LogConversionGenerator(ProblemGenerator):
    """
    Exponential <-> logarithmic form, evaluating logs by asking 'the
    base to what power?', change of base, and the ln identities.

    Variants:
    - exp_to_log:     rewrite b^y = x as log_b(x) = y
    - log_to_exp:     rewrite log_b(x) = y as b^y = x
    - evaluate:       log_b(x) by trying powers of b (A2 sweep);
                      reciprocal arguments give negative answers
    - change_of_base: log_b(x) = log_c(x)/log_c(b) with a shared
                      small base c, answer an exact fraction
    - ln_identity:    ln(e^k), ln(1), ln(e), e^(ln k)

    Op-codes used:
    - LOG_FORM: the defining equivalence b^y = x ⟺ log_b(x) = y
    - REWRITE: the converted statement (established)
    - TRY / REJECT / ACCEPT: the power sweep (established)
    - E: powers (established)
    - CHANGE_BASE: the change-of-base rewrite (expression)
    - LOG_IDENT: a named identity applied (identity, value)
    - M / D: arithmetic (established)
    - Z: final answer
    """

    VARIANTS = ["exp_to_log", "log_to_exp", "evaluate",
                "change_of_base", "ln_identity"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        b = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
        y_cap = {2: 6, 3: 5, 4: 4, 5: 4, 6: 4, 7: 3, 8: 3, 9: 3, 10: 4}[b]
        y = random.randint(2, y_cap)
        x = b ** y

        if variant == "exp_to_log":
            steps = [
                step("LOG_FORM", "b^y = x ⟺ log_b(x) = y"),
                step("REWRITE", f"log_{b}({x}) = {y}"),
                step("Z", f"log_{b}({x}) = {y}"),
            ]
            problem = f"Write {b}^{y} = {x} in logarithmic form."
            answer = f"log_{b}({x}) = {y}"
        elif variant == "log_to_exp":
            steps = [
                step("LOG_FORM", "log_b(x) = y ⟺ b^y = x"),
                step("REWRITE", f"{b}^{y} = {x}"),
                step("Z", f"{b}^{y} = {x}"),
            ]
            problem = f"Write log_{b}({x}) = {y} in exponential form."
            answer = f"{b}^{y} = {x}"
        elif variant == "evaluate":
            recip = random.random() < 0.3
            arg = f"1/{x}" if recip else str(x)
            target = -y if recip else y
            steps = [step("LOG_FORM",
                          f"log_{b}({arg}) = y ⟺ {b}^y = {arg}")]
            for k in range(1, y + 1):
                steps.append(step("TRY", f"{b}^{k}", b ** k))
                if k < y:
                    steps.append(step("REJECT", f"{b}^{k}",
                                      f"{b ** k} ≠ {x}"))
            steps.append(step("ACCEPT", f"{b}^{y}", x))
            if recip:
                steps.append(step("REWRITE",
                                  f"1/{x} = {b}^(-{y}), so y = -{y}"))
            steps.append(step("Z", target))
            problem = f"Evaluate log_{b}({arg})."
            answer = str(target)
        elif variant == "change_of_base":
            c = random.choice([2, 2, 3, 3, 5])
            cap = {2: 6, 3: 4, 5: 3}[c]
            m, n = random.sample(range(2, cap + 1), 2)
            big, base2 = c ** m, c ** n
            val = Fraction(m, n)
            steps = [
                step("CHANGE_BASE",
                     f"log_{base2}({big}) = log_{c}({big})/log_{c}({base2})"),
                step("E", c, m, big),
                step("EVAL", f"log_{c}({big})", m),
                step("E", c, n, base2),
                step("EVAL", f"log_{c}({base2})", n),
                step("D", m, n, val),
                step("Z", val),
            ]
            problem = (f"Use the change of base formula to evaluate "
                       f"log_{base2}({big}).")
            answer = str(val)
        else:
            kind = random.choice(["ln_e_k", "ln_1", "ln_e", "e_ln_k"])
            if kind == "ln_e_k":
                k = random.randint(2, 20)
                expr, answer = f"ln(e^{k})", str(k)
                steps = [
                    step("REWRITE", f"ln(e^{k}) = {k} · ln(e)"),
                    step("LOG_IDENT", "ln(e) = 1", 1),
                    step("M", k, 1, k),
                ]
            elif kind == "ln_1":
                expr, answer = "ln(1)", "0"
                steps = [step("LOG_IDENT", "ln(1) = 0", 0)]
            elif kind == "ln_e":
                expr, answer = "ln(e)", "1"
                steps = [step("LOG_IDENT", "ln(e) = 1", 1)]
            else:
                k = random.randint(2, 20)
                expr, answer = f"e^(ln {k})", str(k)
                steps = [step("LOG_IDENT",
                              "e^(ln x) = x (inverse functions)", k)]
            steps.append(step("Z", answer))
            problem = f"Evaluate {expr}."

        return dict(
            problem_id=jid(),
            operation=f"log_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
