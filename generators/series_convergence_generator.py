import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


def pow_txt(p):
    """1/n^p with the standard renders for p = 1, 1/2, 3/2, ..."""
    if p == 1:
        return "1/n"
    if p == Fraction(1, 2):
        return "1/√n"
    if p.denominator == 1:
        return f"1/n^{p}"
    return f"1/n^({p})"


class SeriesConvergenceGenerator(ProblemGenerator):
    """
    Convergence tests where the scratchpad's first move is CHOOSING
    the right test: nth-term, geometric, p-series, ratio, alternating
    (absolute vs conditional), and direct/limit comparison. Geometric
    sums are exact fractions.

    Variants:
    - nth_term: rational terms with nonzero limit -> diverges
    - geometric: sum a·r^n from n = 0; exact sum when abs(r) < 1
    - p_series: 1/n^p for p in {1/2, 1, 3/2, 2, 3}
    - ratio: c^n/n! (converges) or n!/c^n (diverges)
    - alternating: (-1)^(n+1)·1/n^p, absolute vs conditional
    - comparison: 1/(n^2 + k) (direct) or n/(n^2 + k) (limit)

    Op-codes used:
    - SERIES_SETUP: the series and the question
    - TEST_CHOOSE: which test and the tell that picks it
    - CONVERGE_CHECK / DEGREE_COMPARE / LIMIT_SETUP / CHECK /
      REWRITE / CANCEL / THEOREM / S / D (established)
    - Z: diverges / converges / converges to S / converges
      absolutely / converges conditionally
    """

    VARIANTS = ["nth_term", "geometric", "p_series", "ratio",
                "alternating", "comparison"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "nth_term":
            a, c = random.randint(1, 5), random.randint(1, 5)
            b, d = random.randint(0, 6), random.randint(1, 6)
            lim = Fraction(a, c)
            an = "n" if a == 1 else f"{a}n"
            cn = "n" if c == 1 else f"{c}n"
            num = f"{an} + {b}" if b else an
            den = f"{cn} + {d}"
            body = f"({num})/({den})"
            steps = [
                step("SERIES_SETUP", f"Σ {body}, n ≥ 1",
                     "converge or diverge?"),
                step("TEST_CHOOSE", "nth-term test",
                     "always check lim a_n first"),
                step("LIMIT_SETUP", f"lim n→∞ {body}"),
                step("DEGREE_COMPARE", "deg num = deg den = 1",
                     f"limit = {lim}"),
                step("CHECK", "nth-term", f"{lim} ≠ 0",
                     "terms do not approach 0"),
            ]
            answer = "diverges"
            problem = (f"Determine whether Σ {body} for n ≥ 1 "
                       f"converges or diverges.")
        elif variant == "geometric":
            a = random.choice([v for v in range(-9, 10) if v != 0])
            r = random.choice([Fraction(1, 2), Fraction(-1, 2),
                               Fraction(1, 3), Fraction(-1, 3),
                               Fraction(2, 3), Fraction(-2, 3),
                               Fraction(3, 4), Fraction(1, 4),
                               Fraction(3, 2), Fraction(-3, 2),
                               Fraction(2), Fraction(-2)])
            r_txt = f"({r})" if r.denominator > 1 or r < 0 else str(r)
            body = f"{a}·{r_txt}^n"
            steps = [
                step("SERIES_SETUP", f"Σ {body}, n ≥ 0",
                     "converge or diverge? find the sum if it "
                     "converges"),
                step("TEST_CHOOSE", "geometric series",
                     f"common ratio r = {r}"),
            ]
            if abs(r) < 1:
                one_minus = 1 - r
                total = Fraction(a) / one_minus
                steps += [
                    step("CONVERGE_CHECK", f"abs({r}) < 1", "converges"),
                    step("THEOREM", "geometric series sum",
                         "S = a/(1 - r), first term a"),
                    step("S", 1, str(r), str(one_minus)),
                    step("D", a, str(one_minus), str(total)),
                ]
                answer = f"converges to {total}"
            else:
                steps.append(step("CONVERGE_CHECK",
                                  f"abs({r}) ≥ 1", "diverges"))
                answer = "diverges"
            problem = (f"Determine whether Σ {body} for n ≥ 0 "
                       f"converges or diverges; if it converges, "
                       f"find the sum.")
        elif variant == "p_series":
            p = random.choice([Fraction(1, 2), Fraction(1),
                               Fraction(3, 2), Fraction(2),
                               Fraction(3), Fraction(4)])
            body = pow_txt(p)
            conv = p > 1
            steps = [
                step("SERIES_SETUP", f"Σ {body}, n ≥ 1",
                     "converge or diverge?"),
                step("TEST_CHOOSE", "p-series",
                     f"Σ 1/n^p with p = {p}"),
                step("CHECK", "p-series",
                     f"p = {p} {'>' if conv else '≤'} 1",
                     "converges" if conv else "diverges"),
            ]
            answer = "converges" if conv else "diverges"
            problem = (f"Determine whether Σ {body} for n ≥ 1 "
                       f"converges or diverges.")
        elif variant == "ratio":
            c = random.randint(2, 9)
            over = random.random() < 0.5
            body = f"{c}^n/n!" if over else f"n!/{c}^n"
            ratio = f"{c}/(n + 1)" if over else f"(n + 1)/{c}"
            lim_txt = "0" if over else "∞"
            steps = [
                step("SERIES_SETUP", f"Σ {body}, n ≥ 1",
                     "converge or diverge?"),
                step("TEST_CHOOSE", "ratio test", "factorial present"),
                step("REWRITE",
                     f"a_(n+1)/a_n = "
                     f"({c}^(n+1)/(n+1)!)·(n!/{c}^n)" if over else
                     f"a_(n+1)/a_n = "
                     f"((n+1)!/{c}^(n+1))·({c}^n/n!)"),
                step("CANCEL", f"{c}^(n+1)/{c}^n = {c}",
                     "(n+1)!/n! = n + 1"),
                step("REWRITE", f"a_(n+1)/a_n = {ratio}"),
                step("LIMIT_SETUP", f"lim n→∞ {ratio} = {lim_txt}"),
                step("CHECK", "ratio test",
                     "0 < 1" if over else "∞ > 1",
                     "converges" if over else "diverges"),
            ]
            answer = "converges" if over else "diverges"
            problem = (f"Determine whether Σ {body} for n ≥ 1 "
                       f"converges or diverges.")
        elif variant == "alternating":
            p = random.choice([Fraction(1, 2), Fraction(1),
                               Fraction(3, 2), Fraction(2),
                               Fraction(3)])
            body = f"(-1)^(n+1)·{pow_txt(p)}"
            abs_conv = p > 1
            steps = [
                step("SERIES_SETUP", f"Σ {body}, n ≥ 1",
                     "absolutely convergent, conditionally "
                     "convergent, or divergent?"),
                step("TEST_CHOOSE", "alternating series test",
                     "signs alternate"),
                step("CHECK", "AST", f"{pow_txt(p)} decreases to 0",
                     "converges"),
                step("REWRITE",
                     f"Σ abs(a_n) = Σ {pow_txt(p)}"),
                step("CHECK", "p-series",
                     f"p = {p} {'>' if abs_conv else '≤'} 1",
                     f"Σ {pow_txt(p)} "
                     f"{'converges' if abs_conv else 'diverges'}"),
            ]
            answer = ("converges absolutely" if abs_conv
                      else "converges conditionally")
            problem = (f"Determine whether Σ {body} for n ≥ 1 "
                       f"converges absolutely, converges "
                       f"conditionally, or diverges.")
        else:
            k = random.randint(1, 9)
            direct = random.random() < 0.5
            if direct:
                body = f"1/(n^2 + {k})"
                steps = [
                    step("SERIES_SETUP", f"Σ {body}, n ≥ 1",
                         "converge or diverge?"),
                    step("TEST_CHOOSE", "direct comparison",
                         "compare with Σ 1/n^2"),
                    step("CHECK", "comparison",
                         f"0 < 1/(n^2 + {k}) < 1/n^2",
                         "for all n ≥ 1"),
                    step("CHECK", "p-series", "p = 2 > 1",
                         "Σ 1/n^2 converges"),
                ]
                answer = "converges"
            else:
                body = f"n/(n^2 + {k})"
                steps = [
                    step("SERIES_SETUP", f"Σ {body}, n ≥ 1",
                         "converge or diverge?"),
                    step("TEST_CHOOSE", "limit comparison",
                         "behaves like Σ 1/n"),
                    step("LIMIT_SETUP",
                         f"lim n→∞ (n/(n^2 + {k}))/(1/n) = "
                         f"lim n→∞ n^2/(n^2 + {k})"),
                    step("DEGREE_COMPARE", "deg num = deg den = 2",
                         "limit = 1"),
                    step("CHECK", "limit comparison", "0 < 1 < ∞",
                         "same behavior as Σ 1/n"),
                    step("CHECK", "p-series", "p = 1 ≤ 1",
                         "Σ 1/n diverges"),
                ]
                answer = "diverges"
            problem = (f"Determine whether Σ {body} for n ≥ 1 "
                       f"converges or diverges.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"series_convergence_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
