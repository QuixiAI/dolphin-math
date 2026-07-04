import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

# Sizes whose halves have odd length, so both quartiles are actual
# data points (median-exclusive halves).
SIZES = [7, 10, 11, 14, 15]


def summary(data):
    """(min, Q1, median, Q3, max, lower half, upper half) exactly."""
    s = sorted(data)
    n = len(s)
    if n % 2:
        med = Fraction(s[n // 2])
        lo_half, hi_half = s[:n // 2], s[n // 2 + 1:]
    else:
        med = Fraction(s[n // 2 - 1] + s[n // 2], 2)
        lo_half, hi_half = s[:n // 2], s[n // 2:]
    q1 = lo_half[len(lo_half) // 2]
    q3 = hi_half[len(hi_half) // 2]
    return s[0], q1, med, q3, s[-1], lo_half, hi_half


class FiveNumberSummaryGenerator(ProblemGenerator):
    """
    Five-number summary, IQR, and the 1.5×IQR outlier fence, worked
    on small integer data sets sized so both quartiles are actual
    data points (halves have odd length). Planted outliers sit far
    above the fence by construction.

    Variants:
    - summary: min, Q1, median, Q3, max
    - iqr: Q3 - Q1
    - outliers: fences Q1 - 1.5·IQR and Q3 + 1.5·IQR, then the list

    Op-codes used:
    - SORT / MEDIAN_PICK / MEDIAN_PAIR / MEAN_DIV (established,
      simple_stats)
    - QUARTILE: which quartile, the half it is the median of, value
    - EVAL / S / A / M / CHECK (established)
    - Z: the summary, the IQR, or the outlier list ("none" if none)
    """

    VARIANTS = ["summary", "iqr", "outliers"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        n = random.choice(SIZES)
        plant = variant == "outliers" and random.random() < 0.6
        base = [random.randint(5, 45) for _ in range(n - plant)]
        data = base + ([random.randint(150, 200)] if plant else [])
        random.shuffle(data)
        mn, q1, med, q3, mx, lo_half, hi_half = summary(data)
        s = sorted(data)
        iqr = q3 - q1

        raw = ", ".join(map(str, data))
        steps = [step("SORT", ",".join(map(str, data)),
                      ",".join(map(str, s)))]
        if len(s) % 2:
            steps.append(step("MEDIAN_PICK", s[len(s) // 2],
                              dec(med)))
        else:
            a, b = s[len(s) // 2 - 1], s[len(s) // 2]
            steps.append(step("MEDIAN_PAIR", a, b))
            steps.append(step("MEAN_DIV", a + b, 2, dec(med)))
        steps.append(step("QUARTILE", "Q1",
                          ",".join(map(str, lo_half)), q1))
        steps.append(step("QUARTILE", "Q3",
                          ",".join(map(str, hi_half)), q3))

        if variant == "summary":
            answer = (f"min = {mn}, Q1 = {q1}, median = {dec(med)}, "
                      f"Q3 = {q3}, max = {mx}")
            steps.insert(1, step("EVAL", "min", mn))
            steps.append(step("EVAL", "max", mx))
            problem = (f"Find the five-number summary of the data "
                       f"set: {raw}.")
        elif variant == "iqr":
            steps.append(step("S", q3, q1, iqr))
            answer = str(iqr)
            problem = (f"Find the interquartile range of the data "
                       f"set: {raw}.")
        else:
            f = Fraction(3, 2) * iqr
            lo_fence = q1 - f
            hi_fence = q3 + f
            outs = [v for v in s if v < lo_fence or v > hi_fence]
            steps += [
                step("S", q3, q1, iqr),
                step("M", "1.5", iqr, dec(f)),
                step("S", q1, dec(f), dec(lo_fence)),
                step("A", q3, dec(f), dec(hi_fence)),
                step("CHECK", "1.5×IQR rule",
                     f"outside [{dec(lo_fence)}, {dec(hi_fence)}]",
                     ", ".join(map(str, outs)) if outs else "none"),
            ]
            answer = ", ".join(map(str, outs)) if outs else "none"
            problem = (f"Using the 1.5×IQR rule, find the outliers "
                       f"in the data set: {raw}.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"five_number_summary_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
