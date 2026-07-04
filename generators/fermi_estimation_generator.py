import random

from base_generator import ProblemGenerator
from helpers import step, jid


def sig2(n):
    """Round a positive integer to two significant figures as scientific text."""
    assert n > 0
    exponent = len(str(n)) - 1
    if exponent == 0:
        return str(n)
    place = 10 ** (exponent - 1)
    q, r = divmod(n, place)
    if r * 2 >= place:
        q += 1
    if q == 100:
        q = 10
        exponent += 1
    if q % 10 == 0:
        mantissa = str(q // 10)
    else:
        mantissa = f"{q // 10}.{q % 10}"
    return f"{mantissa} × 10^{exponent}"


class FermiEstimationGenerator(ProblemGenerator):
    """
    Fermi-style estimates where the assumptions are supplied in the prompt,
    multiplied explicitly, and rounded to two significant figures.

    Variants:
    - water_use: town population times gallons per person per day
    - stadium: sections times rows times seats
    - cafeteria: students times slices per week times weeks

    Op-codes used:
    - FERMI_SETUP: scenario and target unit
    - FERMI_FACTOR: one supplied estimate factor
    - M (established): running product
    - SIGFIG_ROUND: round exact product to two significant figures
    - ESTIMATE_CHECK (established): rounded estimate vs raw product
    - Z: rounded estimate with units
    """

    VARIANTS = ["water_use", "stadium", "cafeteria"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _finish(steps, product, units):
        rounded = sig2(product)
        answer = f"{rounded} {units}"
        steps.extend([
            step("SIGFIG_ROUND", product, "2 significant figures", rounded),
            step("ESTIMATE_CHECK", rounded, product, "rounded estimate"),
            step("Z", answer),
        ])
        return answer

    def _water_use(self):
        people = random.choice([12000, 18000, 24000, 36000, 52000, 75000])
        gallons = random.choice([60, 75, 80, 90, 110, 125])
        product = people * gallons
        steps = [
            step("FERMI_SETUP", "town daily water use", "gallons/day"),
            step("FERMI_FACTOR", "people", people),
            step("FERMI_FACTOR", "gallons per person per day", gallons),
            step("M", people, gallons, product),
        ]
        answer = self._finish(steps, product, "gallons/day")
        problem = (
            f"Estimate daily water use for a town with {people} people using "
            f"about {gallons} gallons per person per day. Round to 2 "
            "significant figures."
        )
        return "water_use", problem, steps, answer

    def _stadium(self):
        sections = random.choice([18, 24, 32, 40, 48])
        rows = random.choice([18, 24, 28, 32, 36])
        seats = random.choice([14, 16, 18, 20, 22])
        partial = sections * rows
        product = partial * seats
        steps = [
            step("FERMI_SETUP", "stadium seats", "seats"),
            step("FERMI_FACTOR", "sections", sections),
            step("FERMI_FACTOR", "rows per section", rows),
            step("FERMI_FACTOR", "seats per row", seats),
            step("M", sections, rows, partial),
            step("M", partial, seats, product),
        ]
        answer = self._finish(steps, product, "seats")
        problem = (
            f"Estimate seats in a stadium with {sections} sections, {rows} "
            f"rows per section, and {seats} seats per row. Round to 2 "
            "significant figures."
        )
        return "stadium", problem, steps, answer

    def _cafeteria(self):
        students = random.choice([450, 600, 750, 900, 1200, 1500])
        slices = random.choice([1, 2, 3, 4])
        weeks = random.choice([30, 32, 36, 40])
        partial = students * slices
        product = partial * weeks
        steps = [
            step("FERMI_SETUP", "school pizza slices", "slices/year"),
            step("FERMI_FACTOR", "students", students),
            step("FERMI_FACTOR", "slices per week", slices),
            step("FERMI_FACTOR", "weeks", weeks),
            step("M", students, slices, partial),
            step("M", partial, weeks, product),
        ]
        answer = self._finish(steps, product, "slices/year")
        problem = (
            f"Estimate yearly pizza slices for a school with {students} "
            f"students eating {slices} slices per week for {weeks} weeks. "
            "Round to 2 significant figures."
        )
        return "cafeteria", problem, steps, answer

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "water_use":
            op_suffix, problem, steps, answer = self._water_use()
        elif variant == "stadium":
            op_suffix, problem, steps, answer = self._stadium()
        else:
            op_suffix, problem, steps, answer = self._cafeteria()

        return dict(
            problem_id=jid(),
            operation=f"fermi_estimation_{op_suffix}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
