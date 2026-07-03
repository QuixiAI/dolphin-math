import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


def sgn_num(n):
    """Renders a signed number for work strings: '6' or '(-1)'."""
    return f"({n})" if n < 0 else str(n)


def binomial(var, r):
    """Renders (x + r) sign-aware: '(x + 2)', '(x - 4)'."""
    return f"({var} + {r})" if r > 0 else f"({var} - {-r})"


def binomial2(var, p, r):
    """Renders (px + r) sign-aware, hiding a unit coefficient."""
    head = var if p == 1 else f"{p}{var}"
    return f"({head} + {r})" if r > 0 else f"({head} - {-r})"


def xterm(coef, var):
    """Signed x-term for polynomial strings: '+ 9x', '- x'."""
    mag = "" if abs(coef) == 1 else str(abs(coef))
    return f"+ {mag}{var}" if coef > 0 else f"- {mag}{var}"


def lead_xterm(coef, var):
    """Leading x-term (no spaced sign): '9x', '-2x', 'x'."""
    mag = "" if abs(coef) == 1 else str(abs(coef))
    return f"{mag}{var}" if coef > 0 else f"-{mag}{var}"


class FactorTrinomialGenerator(ProblemGenerator):
    """
    Factors trinomials with visible trial-and-error (A2).

    form="monic":   x² + bx + c by the find-two-numbers method.
    form="general": ax² + bx + c (a ≠ 1) by the ac-method — find m, n with
        m·n = ac and m + n = b (same TRY/REJECT/ACCEPT search), split the
        middle term, factor by grouping, pull out the common binomial.
        Built from primitive binomials, so there is never a hidden overall
        GCF (Gauss's lemma). Emits difficulty 5 per-instance (A3).

    Op-codes used:
    - POLY_SETUP, FACTOR_PAIR_GOAL, TRY, REJECT, ACCEPT, REWRITE, CHECK, Z
    - AC_PRODUCT: compute a·c for the ac-method (work, value)
    - SPLIT_MIDDLE: split bx into mx + nx (split work, resulting polynomial)
    - GROUP: the two grouped halves (group1, group2)
    - FACTOR_GROUP: factor one group (group, gcf, common binomial)
    """

    FORMS = ["monic", "general"]

    def __init__(self, form="monic"):
        if form not in self.FORMS:
            raise ValueError(f"form must be one of {self.FORMS}")
        self.form = form
        self.op_symbol = form

    # ------------------------------------------------------------------

    def _pair_search(self, steps, product, target_sum):
        """Emits FACTOR_PAIR_GOAL and the TRY/REJECT/ACCEPT sweep for two
        numbers with the given product and sum. Returns the winning pair."""
        steps.append(step("FACTOR_PAIR_GOAL", f"m·n = {product}",
                          f"m + n = {target_sum}"))
        for d in range(1, abs(product) + 1):
            if d * d > abs(product):
                break
            if abs(product) % d != 0:
                continue
            big = abs(product) // d
            if product > 0:
                m, n = (d, big) if target_sum > 0 else (-d, -big)
            else:
                m, n = (-d, big) if target_sum > 0 else (d, -big)
            s = m + n
            work = (f"{sgn_num(m)}·{sgn_num(n)}={product}, "
                    f"{sgn_num(m)}+{sgn_num(n)}={s}")
            steps.append(step("TRY", f"({m}, {n})", work))
            if s == target_sum:
                steps.append(step("ACCEPT", f"({m}, {n})",
                                  f"product {product} ✓, sum {target_sum} ✓"))
                return m, n
            steps.append(step("REJECT", f"({m}, {n})",
                              f"sum is {s}, need {target_sum}"))
        raise ValueError(f"no pair for product={product}, sum={target_sum}")

    @staticmethod
    def _pairs_before(product, d_win):
        """How many divisor pairs precede the winner (keeps chains short)."""
        count = 0
        for d in range(1, d_win):
            if d * d > abs(product):
                break
            if abs(product) % d == 0:
                count += 1
        return count

    # ------------------------------------------------------------------

    def generate(self) -> dict:
        if self.form == "general":
            return self._generate_general()
        return self._generate_monic()

    def _generate_monic(self) -> dict:
        var = random.choice(["x", "x", "x", "y", "n"])
        while True:
            p = random.choice([n for n in range(-9, 10) if n != 0])
            q = random.choice([n for n in range(-9, 10) if n != 0])
            if p != q and p + q != 0:
                break
        p, q = sorted((p, q))
        b, c = p + q, p * q

        c_txt = f"+ {c}" if c > 0 else f"- {-c}"
        original = f"{var}^2 {xterm(b, var)} {c_txt}"

        steps = [step("POLY_SETUP", original)]
        self._pair_search(steps, c, b)

        factored = f"{binomial(var, p)}{binomial(var, q)}"
        steps.append(step("REWRITE", factored))
        foil = f"{var}^2 {xterm(q, var)} {xterm(p, var)} {c_txt}"
        steps.append(step("CHECK", "foil", foil, original))
        steps.append(step("Z", factored))

        return dict(
            problem_id=jid(),
            operation="factor_trinomial",
            problem=f"Factor: {original}",
            steps=steps,
            final_answer=factored,
        )

    def _generate_general(self) -> dict:
        var = random.choice(["x", "x", "x", "y", "n"])
        while True:
            p, q = random.randint(1, 4), random.randint(1, 4)
            if p * q < 2:
                continue
            r = random.choice([v for v in range(-6, 7) if v != 0])
            s = random.choice([v for v in range(-6, 7) if v != 0])
            if gcd(p, abs(r)) != 1 or gcd(q, abs(s)) != 1:
                continue
            if p == q and r == s:            # perfect square — special forms
                continue
            a, b, c = p * q, p * s + q * r, r * s
            if b == 0:
                continue
            m, n = p * s, q * r              # the ac-method split, in
            if m == n:                       # grouping-compatible order
                continue
            # Keep the trial chain humane: at most 5 rejected pairs.
            if self._pairs_before(a * c, min(abs(m), abs(n))) > 5:
                continue
            break

        c_txt = f"+ {c}" if c > 0 else f"- {-c}"
        a_txt = str(a) if a > 1 else ""
        original = f"{a_txt}{var}^2 {xterm(b, var)} {c_txt}"

        steps = [step("POLY_SETUP", original)]
        steps.append(step("AC_PRODUCT", f"{a} × {sgn_num(c)}", a * c))
        self._pair_search(steps, a * c, b)

        four_term = (f"{a_txt}{var}^2 {xterm(m, var)} {xterm(n, var)} {c_txt}")
        steps.append(step("SPLIT_MIDDLE",
                          f"{lead_xterm(b, var)} = "
                          f"{lead_xterm(m, var)} {xterm(n, var)}",
                          four_term))

        g1 = f"{a_txt}{var}^2 {xterm(m, var)}"
        g2 = f"{lead_xterm(n, var)} {c_txt}"
        steps.append(step("GROUP", f"({g1})", f"({g2})"))

        common = binomial2(var, q, s)
        gcf1 = f"{p}{var}" if p > 1 else var
        steps.append(step("FACTOR_GROUP", g1, gcf1, common))
        steps.append(step("FACTOR_GROUP", g2, str(r), common))

        factors = sorted([(q, s), (p, r)], key=lambda t: (t[1], t[0]))
        factored = "".join(binomial2(var, pf, rf) for pf, rf in factors)
        steps.append(step("REWRITE", factored))
        steps.append(step("CHECK", "foil", four_term, original))
        steps.append(step("Z", factored))

        return dict(
            problem_id=jid(),
            operation="factor_trinomial_general",
            problem=f"Factor: {original}",
            steps=steps,
            final_answer=factored,
            difficulty=5,
        )
