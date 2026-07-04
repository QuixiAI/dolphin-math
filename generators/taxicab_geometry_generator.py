import random
from base_generator import ProblemGenerator
from helpers import step, jid


def wrap(n):
    return f"({n})" if n < 0 else str(n)


class TaxicabGeometryGenerator(ProblemGenerator):
    """
    Taxicab and Chebyshev metrics with middle-school arithmetic:
    distances, the lattice-point counts of taxicab 'circles' (diamonds)
    and Chebyshev 'circles' (squares), and a head-to-head comparison of
    the two metrics on one pair of points.

    Op-codes used:
    - METRIC: the metric definition being used (name, definition)
    - S / A / M: coordinate arithmetic (established)
    - ABS_VAL: absolute value of a difference (input, value)
    - MAX: maximum of two values (values, max)
    - REWRITE: the circle-shape reasoning (established)
    - Z: final answer
    """

    VARIANTS = ["taxi_distance", "cheb_distance", "taxi_circle",
                "cheb_circle", "compare"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _points():
        while True:
            x1, y1 = random.randint(-9, 9), random.randint(-9, 9)
            x2, y2 = random.randint(-9, 9), random.randint(-9, 9)
            if x1 != x2 and y1 != y2:
                return x1, y1, x2, y2

    @staticmethod
    def _dist_steps(steps, x1, y1, x2, y2):
        dx, dy = x2 - x1, y2 - y1
        steps.append(step("S", x2, x1, dx))
        steps.append(step("ABS_VAL", wrap(dx), abs(dx)))
        steps.append(step("S", y2, y1, dy))
        steps.append(step("ABS_VAL", wrap(dy), abs(dy)))
        return abs(dx), abs(dy)

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "taxi_distance":
            x1, y1, x2, y2 = self._points()
            steps = [step("METRIC", "taxicab",
                          "d = abs(x2 - x1) + abs(y2 - y1)")]
            ax, ay = self._dist_steps(steps, x1, y1, x2, y2)
            steps.append(step("A", ax, ay, ax + ay))
            answer = str(ax + ay)
            problem = (f"Using the taxicab metric, find the distance "
                       f"between ({x1}, {y1}) and ({x2}, {y2}).")
        elif variant == "cheb_distance":
            x1, y1, x2, y2 = self._points()
            steps = [step("METRIC", "Chebyshev",
                          "d = max(abs(x2 - x1), abs(y2 - y1))")]
            ax, ay = self._dist_steps(steps, x1, y1, x2, y2)
            steps.append(step("MAX", f"{ax}, {ay}", max(ax, ay)))
            answer = str(max(ax, ay))
            problem = (f"Using the Chebyshev metric, find the distance "
                       f"between ({x1}, {y1}) and ({x2}, {y2}).")
        elif variant == "taxi_circle":
            r = random.randint(2, 12)
            steps = [
                step("METRIC", "taxicab circle",
                     f"all points with abs(x) + abs(y) = {r}"),
                step("REWRITE",
                     "the 'circle' is a diamond with 4 sides; each side "
                     f"contains {r} lattice points counting one corner"),
                step("M", 4, r, 4 * r),
            ]
            answer = str(4 * r)
            problem = (f"In taxicab geometry, how many lattice points "
                       f"lie at distance exactly {r} from the origin?")
        elif variant == "cheb_circle":
            r = random.randint(2, 12)
            steps = [
                step("METRIC", "Chebyshev circle",
                     f"all points with max(abs(x), abs(y)) = {r}"),
                step("REWRITE",
                     f"the 'circle' is a square with side {2 * r}; its "
                     f"border contains 8·{r} lattice points"),
                step("M", 8, r, 8 * r),
            ]
            answer = str(8 * r)
            problem = (f"In Chebyshev geometry, how many lattice points "
                       f"lie at distance exactly {r} from the origin?")
        else:
            x1, y1, x2, y2 = self._points()
            steps = [step("METRIC", "taxicab vs Chebyshev",
                          "sum of absolute differences vs their max")]
            ax, ay = self._dist_steps(steps, x1, y1, x2, y2)
            steps.append(step("A", ax, ay, ax + ay))
            steps.append(step("MAX", f"{ax}, {ay}", max(ax, ay)))
            answer = f"taxicab {ax + ay}; Chebyshev {max(ax, ay)}"
            problem = (f"For the points ({x1}, {y1}) and ({x2}, {y2}), "
                       f"find both the taxicab distance and the "
                       f"Chebyshev distance.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"taxicab_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
