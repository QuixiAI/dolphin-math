import random
from base_generator import ProblemGenerator
from helpers import step, jid


def sub(n):
    """A substituted input is always parenthesized: 2(3) + 5, (-2)^2."""
    return f"({n})"


def linear_txt(coef, const, var, power=""):
    """Renders coef·var^power + const, dropping a zero constant."""
    head = f"{coef}{var}{power}"
    if const == 0:
        return head
    return f"{head} + {const}" if const > 0 else f"{head} - {-const}"


class FunctionCompositionGenerator(ProblemGenerator):
    """
    Function composition, numeric and symbolic: f(g(2)) and f(g(x)).

    Numeric records evaluate inside-out - the inner function first, its
    value recorded with EVAL, then fed into the outer function. Symbolic
    records substitute the inner rule, distribute, and combine constants.
    Both f(g(k)) and (f o g)(k) notations appear; the ring notation gets
    an explicit FUNC_OP unfold to nested form.

    Op-codes used:
    - FUNC_SETUP: both definitions and the target (established)
    - FUNC_OP: unfold (f ∘ g)(k) to f(g(k)) (established)
    - SUBST / E / M / A: the arithmetic (established meanings)
    - EVAL: record a finished evaluation (established)
    - DIST: distribute over the substituted rule (established)
    - REWRITE: the simplified composed rule (established)
    - Z: final answer
    """

    VARIANTS = ["numeric", "symbolic"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _linear(lo=2, hi=4):
        a = random.choice([v for v in range(-hi, hi + 1)
                           if abs(v) >= lo])
        b = random.choice([v for v in range(-9, 10) if v != 0])
        return a, b

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        n_out, n_in = random.choice([("f", "g"), ("g", "h"), ("p", "q"),
                                     ("g", "f"), ("h", "g"), ("q", "p")])
        var = random.choice(["x", "x", "t"])
        ring = random.random() < 0.5

        if variant == "numeric":
            return self._numeric(n_out, n_in, var, ring)
        return self._symbolic(n_out, n_in, var, ring)

    def _numeric(self, n_out, n_in, var, ring):
        out_quad = random.random() < 0.3
        in_quad = (not out_quad) and random.random() < 0.3
        oa, ob = self._linear()
        ia, ib = self._linear()
        oc = random.choice([v for v in range(-9, 10) if v != 0])
        ic = random.choice([v for v in range(-9, 10) if v != 0])
        out_rule = linear_txt(1, oc, var, "^2").replace(f"1{var}", var) \
            if out_quad else linear_txt(oa, ob, var)
        in_rule = linear_txt(1, ic, var, "^2").replace(f"1{var}", var) \
            if in_quad else linear_txt(ia, ib, var)
        k = random.choice([v for v in range(-4, 5) if v != 0])

        iv = (k * k + ic) if in_quad else (ia * k + ib)
        ov = (iv * iv + oc) if out_quad else (oa * iv + ob)

        nested = f"{n_out}({n_in}({k}))"
        target = f"({n_out} ∘ {n_in})({k})" if ring else nested
        steps = [step("FUNC_SETUP",
                      f"{n_out}({var}) = {out_rule}; "
                      f"{n_in}({var}) = {in_rule}", target)]
        if ring:
            steps.append(step("FUNC_OP", target, nested))

        if in_quad:
            steps.append(step("SUBST", var, k,
                              linear_txt(1, ic, sub(k), "^2")
                              .replace(f"1{sub(k)}", sub(k))))
            steps.append(step("E", sub(k), 2, k * k))
            steps.append(step("A", k * k, ic, iv))
        else:
            steps.append(step("SUBST", var, k,
                              f"{ia}{sub(k)} "
                              f"{'+' if ib > 0 else '-'} {abs(ib)}"))
            steps.append(step("M", ia, k, ia * k))
            steps.append(step("A", ia * k, ib, iv))
        steps.append(step("EVAL", f"{n_in}({k})", iv))

        if out_quad:
            steps.append(step("SUBST", var, iv,
                              linear_txt(1, oc, sub(iv), "^2")
                              .replace(f"1{sub(iv)}", sub(iv))))
            steps.append(step("E", sub(iv), 2, iv * iv))
            steps.append(step("A", iv * iv, oc, ov))
        else:
            steps.append(step("SUBST", var, iv,
                              f"{oa}{sub(iv)} "
                              f"{'+' if ob > 0 else '-'} {abs(ob)}"))
            steps.append(step("M", oa, iv, oa * iv))
            steps.append(step("A", oa * iv, ob, ov))
        steps.append(step("EVAL", nested, ov))
        steps.append(step("Z", ov))

        problem = (f"Given {n_out}({var}) = {out_rule} and "
                   f"{n_in}({var}) = {in_rule}, find {target}.")
        return self._pack("function_composition_numeric", problem, steps,
                          str(ov))

    def _symbolic(self, n_out, n_in, var, ring):
        oa, ob = self._linear(2, 5)
        in_square = random.random() < 0.35
        if in_square:
            ic = random.choice([v for v in range(-9, 10) if v != 0])
            in_rule = linear_txt(1, ic, var, "^2").replace(f"1{var}", var)
            power, inner_coef, inner_const = "^2", 1, ic
        else:
            ia, ib = self._linear(2, 5)
            in_rule = linear_txt(ia, ib, var)
            power, inner_coef, inner_const = "", ia, ib

        out_rule = linear_txt(oa, ob, var)
        res_coef = oa * inner_coef
        res_const = oa * inner_const + ob
        answer = linear_txt(res_coef, res_const, var, power)

        nested = f"{n_out}({n_in}({var}))"
        target = f"({n_out} ∘ {n_in})({var})" if ring else nested
        substituted = (f"{oa}({in_rule}) "
                       f"{'+' if ob > 0 else '-'} {abs(ob)}")
        distributed = linear_txt(res_coef, oa * inner_const, var, power)

        steps = [step("FUNC_SETUP",
                      f"{n_out}({var}) = {out_rule}; "
                      f"{n_in}({var}) = {in_rule}", target)]
        if ring:
            steps.append(step("FUNC_OP", target, nested))
        steps.append(step("SUBST", var, in_rule, substituted))
        steps.append(step("DIST", oa, in_rule, distributed))
        steps.append(step("A", oa * inner_const, ob, res_const))
        steps.append(step("REWRITE", answer))
        steps.append(step("Z", answer))

        problem = (f"Given {n_out}({var}) = {out_rule} and "
                   f"{n_in}({var}) = {in_rule}, find {target} as a "
                   f"simplified expression.")
        return self._pack("function_composition_symbolic", problem, steps,
                          answer)

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
