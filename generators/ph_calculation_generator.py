import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


LOG_VALUES = [
    (2, Fraction(3, 10)),
    (3, Fraction(12, 25)),
    (4, Fraction(3, 5)),
    (5, Fraction(7, 10)),
    (6, Fraction(39, 50)),
    (7, Fraction(17, 20)),
    (8, Fraction(9, 10)),
    (9, Fraction(19, 20)),
]


def dec(value):
    value = Fraction(value)
    num, den = value.numerator, value.denominator
    p10 = 0
    while den % 2 == 0:
        den //= 2
        num *= 5
        p10 += 1
    while den % 5 == 0:
        den //= 5
        num *= 2
        p10 += 1
    assert den == 1, value
    if p10 == 0:
        return str(num)
    s = str(abs(num)).rjust(p10 + 1, "0")
    out = f"{s[:-p10]}.{s[-p10:]}".rstrip("0").rstrip(".")
    return ("-" if num < 0 else "") + out


class PHCalculationGenerator(ProblemGenerator):
    """
    Exact pH and pOH arithmetic with powers of ten or supplied log values.

    Variants:
    - hydronium_power: [H+]=10^-n gives pH=n.
    - hydroxide_power: [OH-]=10^-n gives pOH=n and pH=14-n.
    - hydronium_with_log: [H+]=a*10^-n with log10(a) supplied.
    - hydroxide_with_log: [OH-]=a*10^-n with log10(a) supplied.

    Op-codes used:
    - PH_SETUP / PH_FORMULA / LOG_POWER / LOG_PRODUCT
    - S (established/shared): exact subtraction for logs and pH+pOH=14
    - Z: pH or pOH/pH pair
    """

    VARIANTS = [
        "hydronium_power",
        "hydroxide_power",
        "hydronium_with_log",
        "hydroxide_with_log",
    ]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "hydronium_power":
            problem, steps, answer = self._generate_hydronium_power()
        elif variant == "hydroxide_power":
            problem, steps, answer = self._generate_hydroxide_power()
        elif variant == "hydronium_with_log":
            problem, steps, answer = self._generate_hydronium_with_log()
        else:
            problem, steps, answer = self._generate_hydroxide_with_log()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"ph_calculation_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_hydronium_power(self):
        exponent = random.randint(1, 12)
        log_h = -exponent
        ph = exponent
        steps = [
            step("PH_SETUP", "hydronium_power", f"[H+]=10^-{exponent}"),
            step("PH_FORMULA", "pH=-log10([H+])"),
            step("LOG_POWER", f"log10(10^-{exponent})", log_h),
            step("S", 0, log_h, ph),
        ]
        answer = f"pH={ph}"
        problem = f"A solution has [H+]=10^-{exponent} M. Find pH."
        return problem, steps, answer

    def _generate_hydroxide_power(self):
        exponent = random.randint(1, 12)
        log_oh = -exponent
        poh = exponent
        ph = 14 - poh
        steps = [
            step("PH_SETUP", "hydroxide_power", f"[OH-]=10^-{exponent}"),
            step("PH_FORMULA", "pOH=-log10([OH-]), pH=14-pOH"),
            step("LOG_POWER", f"log10(10^-{exponent})", log_oh),
            step("S", 0, log_oh, poh),
            step("S", 14, poh, ph),
        ]
        answer = f"pOH={poh}; pH={ph}"
        problem = (
            f"A solution has [OH-]=10^-{exponent} M. Find pOH and pH "
            "using pH+pOH=14."
        )
        return problem, steps, answer

    def _generate_hydronium_with_log(self):
        coefficient, log_value = random.choice(LOG_VALUES)
        exponent = random.randint(2, 12)
        log_h = log_value - exponent
        ph = 0 - log_h
        steps = [
            step("PH_SETUP", "hydronium_with_log",
                 f"[H+]={coefficient}*10^-{exponent}",
                 f"log10({coefficient})={dec(log_value)}"),
            step("PH_FORMULA", "pH=-log10([H+])"),
            step("LOG_PRODUCT",
                 f"log10({coefficient}*10^-{exponent})=log10({coefficient})-{exponent}"),
            step("S", dec(log_value), exponent, dec(log_h)),
            step("S", 0, dec(log_h), dec(ph)),
        ]
        answer = f"pH={dec(ph)}"
        problem = (
            f"A solution has [H+]={coefficient}*10^-{exponent} M. "
            f"Use provided log10({coefficient})={dec(log_value)} to find pH."
        )
        return problem, steps, answer

    def _generate_hydroxide_with_log(self):
        coefficient, log_value = random.choice(LOG_VALUES)
        exponent = random.randint(2, 12)
        log_oh = log_value - exponent
        poh = 0 - log_oh
        ph = 14 - poh
        steps = [
            step("PH_SETUP", "hydroxide_with_log",
                 f"[OH-]={coefficient}*10^-{exponent}",
                 f"log10({coefficient})={dec(log_value)}"),
            step("PH_FORMULA", "pOH=-log10([OH-]), pH=14-pOH"),
            step("LOG_PRODUCT",
                 f"log10({coefficient}*10^-{exponent})=log10({coefficient})-{exponent}"),
            step("S", dec(log_value), exponent, dec(log_oh)),
            step("S", 0, dec(log_oh), dec(poh)),
            step("S", 14, dec(poh), dec(ph)),
        ]
        answer = f"pOH={dec(poh)}; pH={dec(ph)}"
        problem = (
            f"A solution has [OH-]={coefficient}*10^-{exponent} M. "
            f"Use provided log10({coefficient})={dec(log_value)} to find "
            "pOH and pH with pH+pOH=14."
        )
        return problem, steps, answer
