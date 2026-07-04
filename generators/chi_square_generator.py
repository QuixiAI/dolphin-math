import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

# Upper-tail χ² critical values (α = 0.05) by degrees of freedom,
# supplied in the problem text (Principle 5).
CRIT_BY_DF = {
    1: "3.841", 2: "5.991", 3: "7.815", 4: "9.488",
    5: "11.070", 6: "12.592",
}
# Expected counts per category for the uniform goodness-of-fit case;
# each divides a power of 10 so every χ² term is an exact decimal.
GOF_EXPECTED = [5, 10, 20, 25]


def exact(fr):
    """Terminating decimal when possible, else the reduced fraction."""
    d = fr.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return dec(fr) if d == 1 else str(fr)


def sq_txt(d):
    """(d)^2 rendered with parentheses around a negative base."""
    return f"({d})^2 = {d * d}" if d < 0 else f"{d}^2 = {d * d}"


class ChiSquareGenerator(ProblemGenerator):
    """
    Chi-square tests worked cell by cell: a goodness-of-fit test
    against a uniform model, and a 2×2 test of independence with an
    expected-count table. Data are built so every expected count and
    every χ² contribution is exact; the critical value is supplied in
    the problem (Principle 5).

    Variants:
    - gof_stat:       the χ² statistic for goodness of fit
    - gof_decision:   χ², then reject / fail to reject
    - independence_stat:     the χ² statistic for a 2×2 table
    - independence_decision: χ², then reject / fail to reject

    Op-codes used:
    - CHI_SETUP: observed/expected (or the table) and the goal
    - CHI_FORMULA: the χ² definition
    - EXP_CELL: one expected count = (row·col)/N
    - CHI_TERM: one contribution (O-E, (O-E)², (O-E)²/E)
    - A (established): running sum of the contributions
    - CHECK (established): χ² vs the critical value
    - Z: the statistic, or "reject H0" / "fail to reject H0"
    """

    VARIANTS = ["gof_stat", "gof_decision", "independence_stat",
                "independence_decision"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _decision_step(chi, crit):
        reject = chi > crit
        verdict = "reject H0" if reject else "fail to reject H0"
        rel = ">" if reject else "≤"
        return step("CHECK", "χ² vs critical value",
                    f"{exact(chi)} {rel} {dec(crit)}", verdict), verdict

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant.startswith("gof"):
            k = random.randint(3, 6)
            E = random.choice(GOF_EXPECTED)
            df = k - 1
            crit = Fraction(CRIT_BY_DF[df])
            while True:
                devs = [random.randint(-4, 4) for _ in range(k - 1)]
                devs.append(-sum(devs))
                obs = [E + d for d in devs]
                if all(o >= 0 for o in obs) and abs(devs[-1]) <= E:
                    break
            chi = Fraction(sum(d * d for d in devs), E)
            steps = [
                step("CHI_SETUP",
                     f"observed: {', '.join(map(str, obs))}; "
                     f"expected: {E} each",
                     f"goodness of fit; df = {df}, "
                     f"critical value = {dec(crit)}"),
                step("CHI_FORMULA", "χ² = Σ (O - E)^2/E"),
            ]
            running = Fraction(0)
            terms = []
            for o, d in zip(obs, devs):
                term = Fraction(d * d, E)
                terms.append(term)
                steps.append(step("CHI_TERM", f"{o} - {E} = {d}",
                                  sq_txt(d),
                                  f"{d * d}/{E} = {exact(term)}"))
            running = terms[0]
            for t in terms[1:]:
                steps.append(step("A", exact(running), exact(t),
                                  exact(running + t)))
                running += t
            if variant == "gof_decision":
                dstep, verdict = self._decision_step(chi, crit)
                steps.append(dstep)
                answer = verdict
            else:
                answer = exact(chi)
            ask = ("what is the χ² test statistic?"
                   if variant == "gof_stat"
                   else "state the conclusion (reject H0 or fail to "
                   "reject H0).")
            problem = (f"A goodness-of-fit test checks whether {k} "
                       f"categories are equally likely. The observed "
                       f"counts are {', '.join(map(str, obs))} and "
                       f"each expected count is {E}. Using a critical "
                       f"value of {dec(crit)} (df = {df}), {ask}")
        else:
            df = 1
            crit = Fraction(CRIT_BY_DF[df])
            N = 100
            # Both a and 10-a stay in {2,5,8}, so every expected count
            # is a 2^x·5^y product and each χ² term is an exact decimal.
            a1 = random.choice([2, 5, 8])
            b1 = random.choice([2, 5, 8])
            R1, R2 = a1 * 10, (10 - a1) * 10
            C1, C2 = b1 * 10, (10 - b1) * 10
            E11 = Fraction(R1 * C1, N)
            E12 = Fraction(R1 * C2, N)
            E21 = Fraction(R2 * C1, N)
            E22 = Fraction(R2 * C2, N)
            minE = min(E11, E12, E21, E22)
            delta = random.randint(1, int(minE) - 1) if minE > 1 else 1
            O11, O12 = int(E11) + delta, int(E12) - delta
            O21, O22 = int(E21) - delta, int(E22) + delta
            cells = [(O11, E11, R1, C1), (O12, E12, R1, C2),
                     (O21, E21, R2, C1), (O22, E22, R2, C2)]
            chi = sum(Fraction((o - e) ** 2) / e for o, e, _, _ in cells)
            steps = [
                step("CHI_SETUP",
                     f"row 1: {O11}, {O12}; row 2: {O21}, {O22}; "
                     f"N = {N}",
                     f"independence; df = 1, "
                     f"critical value = {dec(crit)}"),
                step("CHI_FORMULA",
                     "E = (row·col)/N; χ² = Σ (O - E)^2/E"),
            ]
            for o, e, r, c in cells:
                steps.append(step("EXP_CELL", f"({r}·{c})/{N}",
                                  exact(e)))
            terms = []
            for o, e, r, c in cells:
                d = o - e
                term = Fraction(d * d) / e
                terms.append(term)
                dv = int(d)
                steps.append(step("CHI_TERM", f"{o} - {exact(e)} = {dv}",
                                  sq_txt(dv),
                                  f"{dv * dv}/{exact(e)} = {exact(term)}"))
            running = terms[0]
            for t in terms[1:]:
                steps.append(step("A", exact(running), exact(t),
                                  exact(running + t)))
                running += t
            if variant == "independence_decision":
                dstep, verdict = self._decision_step(chi, crit)
                steps.append(dstep)
                answer = verdict
            else:
                answer = exact(chi)
            ask = ("what is the χ² test statistic?"
                   if variant == "independence_stat"
                   else "state the conclusion (reject H0 or fail to "
                   "reject H0).")
            problem = (f"A 2×2 contingency table has counts {O11}, "
                       f"{O12} in row 1 and {O21}, {O22} in row 2 "
                       f"(N = {N}). Test the two variables for "
                       f"independence. Using a critical value of "
                       f"{dec(crit)} (df = 1), {ask}")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"chi_square_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
