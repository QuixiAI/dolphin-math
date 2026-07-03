import random
from base_generator import ProblemGenerator
from helpers import step, jid


def is_square(n):
    if n < 0:
        return False
    r = int(n ** 0.5)
    return r * r == n or (r + 1) * (r + 1) == n


def isqrt_exact(n):
    r = int(n ** 0.5)
    while r * r < n:
        r += 1
    return r if r * r == n else None


class DiscriminantGenerator(ProblemGenerator):
    """
    Discriminant analysis: compute Δ = b² − 4ac and classify the number and
    type of solutions. The outcome class is sampled first so all four appear
    evenly, and the answer is composite (Principle 8): 'Δ = 49; two rational
    solutions' — naming the class without computing Δ earns nothing.

    Classes: two rational / two irrational / one repeated rational /
    no real solutions.

    Op-codes used:
    - EQ_SETUP: the quadratic (string)
    - DISC: discriminant parts (b², 4ac, Δ) — shared with QuadraticGenerator
    - DISC_CLASSIFY: sign comparison and conclusion (comparison, conclusion)
    - SQUARE_TEST: perfect-square test when Δ > 0 (value, work, verdict)
    - Z: 'Δ = <value>; <classification>'
    """

    CLASSES = ["rational", "irrational", "repeated", "none"]
    LABELS = {
        "rational": "two rational solutions",
        "irrational": "two irrational solutions",
        "repeated": "one repeated rational solution",
        "none": "no real solutions",
    }

    def __init__(self, outcome=None):
        if outcome is not None and outcome not in self.CLASSES:
            raise ValueError(f"outcome must be one of {self.CLASSES} or None")
        self.outcome = outcome

    def _sample_coeffs(self, outcome):
        if outcome == "repeated":
            a = random.randint(1, 5)
            t = random.choice([v for v in range(-4, 5) if v != 0])
            return a, 2 * a * t, a * t * t
        while True:
            a = random.randint(1, 5)
            b = random.choice([v for v in range(-9, 10) if v != 0])
            c = random.choice([v for v in range(-9, 10) if v != 0])
            d = b * b - 4 * a * c
            if outcome == "none" and d < 0:
                return a, b, c
            if d > 0:
                square = isqrt_exact(d) is not None
                if outcome == "rational" and square:
                    return a, b, c
                if outcome == "irrational" and not square:
                    return a, b, c

    def generate(self) -> dict:
        outcome = self.outcome or random.choice(self.CLASSES)
        a, b, c = self._sample_coeffs(outcome)
        d = b * b - 4 * a * c
        var = random.choice(["x", "x", "x", "y", "n"])

        a_txt = "" if a == 1 else str(a)
        b_mag = "" if abs(b) == 1 else str(abs(b))
        b_txt = f"+ {b_mag}{var}" if b > 0 else f"- {b_mag}{var}"
        c_txt = f"+ {c}" if c > 0 else f"- {-c}"
        original = f"{a_txt}{var}^2 {b_txt} {c_txt} = 0"

        steps = [step("EQ_SETUP", original)]
        steps.append(step("DISC", b * b, 4 * a * c, d))

        if d > 0:
            steps.append(step("DISC_CLASSIFY", f"{d} > 0",
                              "two real solutions"))
            r = isqrt_exact(d)
            if r is not None:
                steps.append(step("SQUARE_TEST", d, f"{r}^2 = {d}",
                                  "perfect square"))
                label = self.LABELS["rational"]
            else:
                lo = int(d ** 0.5)
                steps.append(step("SQUARE_TEST", d,
                                  f"{lo}^2 = {lo * lo}, "
                                  f"{lo + 1}^2 = {(lo + 1) ** 2}",
                                  "not a perfect square"))
                label = self.LABELS["irrational"]
        elif d == 0:
            steps.append(step("DISC_CLASSIFY", "0 = 0",
                              self.LABELS["repeated"]))
            label = self.LABELS["repeated"]
        else:
            steps.append(step("DISC_CLASSIFY", f"{d} < 0",
                              self.LABELS["none"]))
            label = self.LABELS["none"]

        answer = f"Δ = {d}; {label}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="discriminant_analysis",
            problem=(f"Without solving, use the discriminant to determine "
                     f"the number and type of solutions: {original}"),
            steps=steps,
            final_answer=answer,
        )
