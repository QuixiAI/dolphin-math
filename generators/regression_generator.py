import random
from fractions import Fraction
from itertools import permutations
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

# x is fixed at 1..5, so x̄ = 3 and Sxx = Σ(x - 3)² = 10.
XS = [1, 2, 3, 4, 5]
XBAR = 3
SXX = 10
XDEV = [x - XBAR for x in XS]

# y-deviation shapes: permutations of (-2,-1,0,1,2), so Σd = 0 and
# Σd² = 10. Scaling by k gives Σd² = 10k², hence Sxx·Syy = 100k² is a
# perfect square and √(Sxx·Syy) = 10k. Exclude the collinear shapes
# (|s0| = 10, r = ±1) so residuals stay meaningful.
_BASE = [-2, -1, 0, 1, 2]
SHAPES = []
for _p in sorted(set(permutations(_BASE))):
    _s0 = sum(dx * d for dx, d in zip(XDEV, _p))
    if abs(_s0) < 10:
        SHAPES.append((_p, _s0))


def line_txt(a, b):
    """ŷ = a + bx with sign and unit-coefficient cleanup."""
    if b == 0:
        return f"ŷ = {dec(a)}"
    mag = "x" if abs(b) == 1 else f"{dec(abs(b))}x"
    if a == 0:
        return f"ŷ = {mag}" if b > 0 else f"ŷ = -{mag}"
    sign = "+" if b > 0 else "-"
    return f"ŷ = {dec(a)} {sign} {mag}"


class RegressionGenerator(ProblemGenerator):
    """
    Least-squares linear regression by the deviation formulas:
    b = Sxy/Sxx, a = ȳ - b·x̄, r = Sxy/√(Sxx·Syy), r² and residuals.
    Data are built so x̄, ȳ, Sxx and √(Sxx·Syy) are integers, making
    every reported value an exact terminating decimal.

    Variants:
    - line:        the regression line ŷ = a + bx
    - correlation: r = Sxy/√(Sxx·Syy)
    - r_squared:   r² = Sxy²/(Sxx·Syy)
    - residual:    observed − predicted at one point (line given)
    - predict:     ŷ at a given x (line given)

    Op-codes used:
    - REG_SETUP / RESID_SETUP: the data (or line) and the goal
    - SUM / MEAN_DIV (established): totals and means
    - REG_ROW: one deviation row (x-x̄, y-ȳ, product)
    - SLOPE_FORMULA / INTERCEPT_FORMULA / CORR_FORMULA / RSQ_FORMULA:
      the formula being applied
    - M / D / S / A / E / ROOT / REWRITE (established)
    - Z: the line, r, r², residual, or prediction
    """

    VARIANTS = ["line", "correlation", "r_squared", "residual",
                "predict"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _data(self, allow_flat=True):
        """Return (ys, k, s0, ybar, Sxy, Syy, b, a)."""
        while True:
            shape, s0 = random.choice(SHAPES)
            if s0 != 0 or allow_flat:
                break
        k = random.choice([1, 2, 3])
        ybar = random.randint(30, 80)
        ys = [ybar + k * d for d in shape]
        Sxy = k * s0
        Syy = 10 * k * k
        b = Fraction(Sxy, SXX)
        a = ybar - b * XBAR
        return ys, k, s0, ybar, Sxy, Syy, b, a

    def _points_txt(self, ys):
        return ", ".join(f"({x}, {y})" for x, y in zip(XS, ys))

    def _dev_rows(self, ys, ybar):
        rows = []
        for x, y in zip(XS, ys):
            dx, dy = x - XBAR, y - ybar
            rows.append(step("REG_ROW", f"x-x̄={dx}", f"y-ȳ={dy}",
                             f"product={dx * dy}"))
        return rows

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        ys, k, s0, ybar, Sxy, Syy, b, a = self._data(
            allow_flat=(variant not in ("residual", "predict")))
        pts = self._points_txt(ys)
        sum_expr = " + ".join(str(y) for y in ys)
        total = sum(ys)

        if variant == "line":
            steps = [
                step("REG_SETUP", f"points: {pts}",
                     "least-squares line"),
                step("MEAN_DIV", "15", 5, XBAR),
                step("SUM", sum_expr, total),
                step("MEAN_DIV", total, 5, ybar),
            ]
            steps += self._dev_rows(ys, ybar)
            steps += [
                step("SUM", f"Sxy = sum of products", Sxy),
                step("SUM", "Sxx = 4 + 1 + 0 + 1 + 4", SXX),
                step("SLOPE_FORMULA", "b = Sxy/Sxx"),
                step("D", Sxy, SXX, dec(b)),
                step("INTERCEPT_FORMULA", "a = ȳ - b·x̄"),
                step("M", dec(b), XBAR, dec(b * XBAR)),
                step("S", ybar, dec(b * XBAR), dec(a)),
                step("REWRITE", line_txt(a, b)),
            ]
            answer = line_txt(a, b)
            problem = (f"Find the least-squares regression line for "
                       f"the points {pts}.")
        elif variant == "correlation":
            root = 10 * k
            r = Fraction(s0, 10)
            steps = [
                step("REG_SETUP", f"points: {pts}",
                     "correlation coefficient r"),
                step("SUM", sum_expr, total),
                step("MEAN_DIV", total, 5, ybar),
            ]
            steps += self._dev_rows(ys, ybar)
            steps += [
                step("SUM", "Sxy = sum of products", Sxy),
                step("SUM", "Sxx = 4 + 1 + 0 + 1 + 4", SXX),
                step("SUM", "Syy = sum of (y-ȳ)^2", Syy),
                step("CORR_FORMULA", "r = Sxy/√(Sxx·Syy)"),
                step("M", SXX, Syy, SXX * Syy),
                step("ROOT", f"√{SXX * Syy}", root),
                step("D", Sxy, root, dec(r)),
            ]
            answer = dec(r)
            problem = (f"Find the correlation coefficient r for the "
                       f"points {pts}. Give an exact value.")
        elif variant == "r_squared":
            r2 = Fraction(Sxy * Sxy, SXX * Syy)
            steps = [
                step("REG_SETUP", f"points: {pts}",
                     "coefficient of determination r^2"),
                step("SUM", sum_expr, total),
                step("MEAN_DIV", total, 5, ybar),
            ]
            steps += self._dev_rows(ys, ybar)
            steps += [
                step("SUM", "Sxy = sum of products", Sxy),
                step("SUM", "Sxx = 4 + 1 + 0 + 1 + 4", SXX),
                step("SUM", "Syy = sum of (y-ȳ)^2", Syy),
                step("RSQ_FORMULA", "r^2 = Sxy^2/(Sxx·Syy)"),
                step("E", Sxy, 2, Sxy * Sxy),
                step("M", SXX, Syy, SXX * Syy),
                step("D", Sxy * Sxy, SXX * Syy, dec(r2)),
            ]
            answer = dec(r2)
            problem = (f"Find r^2 for the points {pts}. Give an exact "
                       f"value.")
        elif variant == "residual":
            j = random.choice(XS)
            yj = ys[XS.index(j)]
            pred = a + b * j
            resid = yj - pred
            steps = [
                step("RESID_SETUP",
                     f"point ({j}, {yj}), line {line_txt(a, b)}",
                     "residual = observed − predicted"),
                step("M", dec(b), j, dec(b * j)),
                step("A", dec(a), dec(b * j), dec(pred)),
                step("S", yj, dec(pred), dec(resid)),
            ]
            answer = dec(resid)
            problem = (f"The least-squares line for a data set is "
                       f"{line_txt(a, b)}. Find the residual at the "
                       f"point ({j}, {yj}).")
        else:
            j = random.choice([6, 7, 8, 10])
            pred = a + b * j
            steps = [
                step("REG_SETUP", f"line {line_txt(a, b)}",
                     f"predict ŷ at x = {j}"),
                step("M", dec(b), j, dec(b * j)),
                step("A", dec(a), dec(b * j), dec(pred)),
            ]
            answer = dec(pred)
            problem = (f"The least-squares line for a data set is "
                       f"{line_txt(a, b)}. Predict ŷ when x = {j}.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"regression_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
