import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


def mono(coef, var, power):
    """Renders one monomial: '12x^3', '18x', '-6', 'x^2', '-x'."""
    if power == 0:
        return str(coef)
    v = var if power == 1 else f"{var}^{power}"
    if coef == 1:
        return v
    if coef == -1:
        return f"-{v}"
    return f"{coef}{v}"


def poly(terms, var):
    """Renders [(coef, power), ...] sign-aware: '12x^3 + 18x^2 - 6x'."""
    out = mono(terms[0][0], var, terms[0][1])
    for coef, power in terms[1:]:
        sign = " + " if coef > 0 else " - "
        out += sign + mono(abs(coef), var, power)
    return out


class FactorGCFGenerator(ProblemGenerator):
    """
    Factors the greatest common factor out of a 2- or 3-term polynomial.

    Procedure: find the GCF of the coefficients, find the lowest variable
    power, divide every term by the combined GCF, and verify by
    redistributing (A1 CHECK).

    Op-codes used:
    - POLY_SETUP: the polynomial (string)
    - GCF_COEFF: GCF of the coefficients (coefficient list, gcf)
    - GCF_VAR: lowest variable power (variable parts, lowest)
    - GCF_RESULT: the combined GCF monomial (gcf)
    - DIV_TERM: divide one term by the GCF (term, gcf, quotient term)
    - REWRITE: the factored form (string)
    - CHECK: redistribute and compare with the original (method, lhs, rhs)
    - Z: final answer
    """

    def generate(self) -> dict:
        var = random.choice(["x", "y", "n", "t"])
        n_terms = random.choice([2, 3])
        g_coef = random.randint(2, 6)
        g_pow = random.choice([0, 1, 1, 2])

        # Quotient: coefficients with overall gcd 1, first positive, and a
        # constant term (lowest power 0) so the variable GCF is exactly g_pow.
        while True:
            q_coefs = [random.randint(1, 9)]
            q_coefs += [random.choice([-1, 1]) * random.randint(1, 9)
                        for _ in range(n_terms - 1)]
            overall = 0
            for c in q_coefs:
                overall = gcd(overall, abs(c))
            if overall == 1 and len({abs(c) for c in q_coefs}) >= 1:
                break
        if n_terms == 2:
            q_pows = [random.randint(1, 3), 0]
        else:
            hi = random.randint(2, 4)
            q_pows = [hi, random.randint(1, hi - 1), 0]

        q_terms = list(zip(q_coefs, q_pows))
        o_terms = [(g_coef * c, g_pow + p) for c, p in q_terms]

        original = poly(o_terms, var)
        gcf_txt = mono(g_coef, var, g_pow)
        factored = f"{gcf_txt}({poly(q_terms, var)})"

        steps = [step("POLY_SETUP", original)]
        steps.append(step("GCF_COEFF",
                          ", ".join(str(abs(c)) for c, _ in o_terms), g_coef))
        if g_pow > 0:
            var_parts = ", ".join(
                mono(1, var, p) if p > 0 else "1" for _, p in o_terms)
            steps.append(step("GCF_VAR", var_parts, mono(1, var, g_pow)))
        steps.append(step("GCF_RESULT", gcf_txt))
        for (oc, op_), (qc, qp) in zip(o_terms, q_terms):
            steps.append(step("DIV_TERM", mono(oc, var, op_), gcf_txt,
                              mono(qc, var, qp)))
        steps.append(step("REWRITE", factored))

        redistributed = " + ".join(
            f"{gcf_txt}·({mono(c, var, p)})" for c, p in q_terms)
        steps.append(step("CHECK", "distribute", redistributed, original))
        steps.append(step("Z", factored))

        return dict(
            problem_id=jid(),
            operation="factor_gcf",
            problem=f"Factor out the greatest common factor: {original}",
            steps=steps,
            final_answer=factored,
        )
