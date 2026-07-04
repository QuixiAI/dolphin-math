import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.integration_by_parts_generator import cm


def fac(r):
    """Factor text for the root r: (x - r), (x + r), or x."""
    if r == 0:
        return "x"
    return f"(x - {r})" if r > 0 else f"(x + {-r})"


def ln_term(r):
    """ln(abs(x - r)) with the sign folded in."""
    if r == 0:
        inner = "x"
    else:
        inner = f"x - {r}" if r > 0 else f"x + {-r}"
    return f"ln(abs({inner}))"


def lin_txt(p, q):
    """px + q with unit and zero coefficients cleaned up."""
    if p == 0:
        return str(q)
    xt = "x" if p == 1 else ("-x" if p == -1 else f"{p}x")
    if q == 0:
        return xt
    return f"{xt} + {q}" if q > 0 else f"{xt} - {-q}"


def num_txt(p, q):
    """The numerator as it appears over a fraction bar."""
    t = lin_txt(p, q)
    return f"({t})" if " " in t else t


def sub_txt(p, q, x):
    """px + q with x substituted and parenthesized: 2(3) + 7."""
    if p == 0:
        return str(q)
    if p == 1:
        core = f"({x})"
    elif p == -1:
        core = f"-({x})"
    else:
        core = f"{p}({x})"
    if q == 0:
        return core
    return f"{core} + {q}" if q > 0 else f"{core} - {-q}"


def signed_join(terms):
    """Join (coefficient, unsigned magnitude text) terms with signs."""
    out = ("-" if terms[0][0] < 0 else "") + terms[0][1]
    for c, mag in terms[1:]:
        out += f" + {mag}" if c > 0 else f" - {mag}"
    return out


class PartialFractionsGenerator(ProblemGenerator):
    """
    Partial fraction decomposition of proper rationals with linear
    factors, solved by clearing denominators and substituting the
    roots (the cover-up idea made explicit), then integrated term by
    term when the item asks for the integral. All constants are
    integers by construction.

    Variants:
    - decompose: (px+q)/((x-a)(x-b)) -> A/(x-a) + B/(x-b), no integral
    - integrate: the same decomposition followed by term-by-term
      antiderivatives A ln(abs(x-a)) + B ln(abs(x-b)) + C
    - repeated:  (px+q)/(x-a)^2 -> A/(x-a) + B/(x-a)^2, integrated to
      A ln(abs(x-a)) - B/(x-a) + C

    Op-codes used:
    - INTEG_SETUP / INTEG_RULE / ANTIDERIV / REWRITE (established)
    - PARTFRAC_SETUP: the decomposition ansatz with unknowns A, B
    - SUBST / EVAL / EQ_OP_BOTH (established) to pin down A and B
    - Z: the decomposition or the antiderivative
    """

    VARIANTS = ["decompose", "integrate", "repeated"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _solve_distinct(p, q, a, b, A, B):
        """Steps that pin down A and B by substituting the roots."""
        steps = [step("REWRITE",
                      f"{lin_txt(p, q)} = A{fac(b)} + B{fac(a)}")]
        for name, val, root, other in (("A", A, a, b), ("B", B, b, a)):
            coef = root - other
            inner = (f"({root}) - {other}" if other > 0 else
                     f"({root}) + {-other}" if other < 0 else f"{root}")
            steps.append(step("SUBST", "x", root,
                              f"{sub_txt(p, q, root)} = {name}({inner})"))
            coef_txt = "" if coef == 1 else ("-" if coef == -1 else str(coef))
            steps.append(step("EVAL", f"{val * coef} = {coef_txt}{name}"))
            if coef != 1:
                steps.append(step("EQ_OP_BOTH", "divide", coef, name, val))
        return steps

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        nz = [v for v in range(-4, 5) if v != 0]

        if variant in ("decompose", "integrate"):
            A, B = random.choice(nz), random.choice(nz)
            a, b = random.sample(range(-4, 5), 2)
            p, q = A + B, -(A * b + B * a)
            expr = f"{num_txt(p, q)}/({fac(a)}{fac(b)})"
            mag_a, mag_b = f"{abs(A)}/{fac(a)}", f"{abs(B)}/{fac(b)}"
            decomp = signed_join([(A, mag_a), (B, mag_b)])
            setup = step("PARTFRAC_SETUP",
                         f"{expr} = A/{fac(a)} + B/{fac(b)}")
            solve = self._solve_distinct(p, q, a, b, A, B)
            found = step("REWRITE", f"{expr} = {decomp}")
            if variant == "decompose":
                answer = decomp
                steps = [setup] + solve + [found]
                problem = f"Decompose {expr} into partial fractions."
            else:
                ln_a = cm(abs(A), ln_term(a))
                ln_b = cm(abs(B), ln_term(b))
                answer = signed_join([(A, ln_a), (B, ln_b)]) + " + C"
                steps = ([step("INTEG_SETUP", f"∫ {expr} dx",
                               "partial fractions"), setup] + solve +
                         [found,
                          step("INTEG_RULE", "term by term",
                               signed_join([(A, f"∫ {mag_a} dx"),
                                            (B, f"∫ {mag_b} dx")])),
                          step("ANTIDERIV",
                               signed_join([(A, f"{mag_a} dx")]),
                               signed_join([(A, ln_a)])),
                          step("ANTIDERIV",
                               signed_join([(B, f"{mag_b} dx")]),
                               signed_join([(B, ln_b)]) + " + C"),
                          step("REWRITE", answer)])
                problem = f"Find ∫ {expr} dx."
        else:
            p = random.choice(nz)
            Bv = random.choice([v for v in range(-5, 6) if v != 0])
            a = random.choice(range(-4, 5))
            q = Bv - p * a
            expr = f"{num_txt(p, q)}/{fac(a)}^2"
            mag_1 = f"{abs(p)}/{fac(a)}"
            mag_2 = f"{abs(Bv)}/{fac(a)}^2"
            decomp = signed_join([(p, mag_1), (Bv, mag_2)])
            ln_a = cm(abs(p), ln_term(a))
            answer = signed_join([(p, ln_a),
                                  (-Bv, f"{abs(Bv)}/{fac(a)}")]) + " + C"
            b_txt = f" + {Bv}" if Bv > 0 else f" - {-Bv}"
            steps = [
                step("INTEG_SETUP", f"∫ {expr} dx", "partial fractions"),
                step("PARTFRAC_SETUP",
                     f"{expr} = A/{fac(a)} + B/{fac(a)}^2"),
                step("REWRITE", f"{lin_txt(p, q)} = A{fac(a)} + B"),
                step("SUBST", "x", a, f"{sub_txt(p, q, a)} = B"),
                step("EVAL", f"B = {Bv}"),
                step("SUBST", "x", a + 1,
                     f"{sub_txt(p, q, a + 1)} = A(1){b_txt}"),
                step("EVAL", f"{p + Bv} = A{b_txt}"),
                step("EQ_OP_BOTH",
                     "subtract" if Bv > 0 else "add", abs(Bv), "A", p),
                step("REWRITE", f"{expr} = {decomp}"),
                step("ANTIDERIV", signed_join([(p, f"{mag_1} dx")]),
                     signed_join([(p, ln_a)])),
                step("ANTIDERIV", signed_join([(Bv, f"{mag_2} dx")]),
                     signed_join([(-Bv, f"{abs(Bv)}/{fac(a)}")]) + " + C"),
                step("REWRITE", answer),
            ]
            problem = f"Find ∫ {expr} dx."
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"partial_fractions_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
