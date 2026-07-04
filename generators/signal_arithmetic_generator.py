import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class SignalArithmeticGenerator(ProblemGenerator):
    """
    Sampling/Nyquist and dB arithmetic.

    Variants:
    - nyquist: Nyquist rate and sampling margin
    - db_power: power ratio to decibels with supplied log10

    Op-codes used:
    - SIGNAL_SETUP: signal arithmetic inputs
    - NYQUIST: Nyquist criterion statement
    - DB_FORMULA: dB formula
    - LOG_SUPPLIED: supplied logarithm value
    - M / S (established/shared): exact arithmetic
    - CHECK: pass/fail interpretation
    - Z: requested signal metric
    """

    VARIANTS = ["nyquist", "db_power"]
    DB_LOGS = {
        Fraction(1, 100): -2,
        Fraction(1, 10): -1,
        Fraction(1, 1): 0,
        Fraction(10, 1): 1,
        Fraction(100, 1): 2,
        Fraction(1000, 1): 3,
    }

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "nyquist":
            problem, steps, answer = self._generate_nyquist()
        else:
            problem, steps, answer = self._generate_db_power()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"signal_arithmetic_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_nyquist(self):
        f_max = random.randint(20, 2000)
        nyquist = 2 * f_max
        sample_rate = random.randint(f_max + 1, 5 * f_max)
        margin = sample_rate - nyquist
        status = "above Nyquist" if margin >= 0 else "below Nyquist"
        steps = [
            step("SIGNAL_SETUP", "sampling", f"f_max={f_max} Hz",
                 f"f_s={sample_rate} Hz"),
            step("NYQUIST", "required rate = 2*f_max"),
            step("M", 2, f_max, nyquist),
            step("S", sample_rate, nyquist, margin),
            step("CHECK", f"margin={margin} Hz", status),
        ]
        answer = f"Nyquist rate={nyquist} Hz; margin={margin} Hz; {status}"
        problem = (
            f"For a signal with maximum frequency {f_max} Hz sampled at "
            f"{sample_rate} Hz, compute the Nyquist rate and sampling margin."
        )
        return problem, steps, answer

    def _generate_db_power(self):
        ratio = random.choice(list(self.DB_LOGS))
        log_value = self.DB_LOGS[ratio]
        db_value = 10 * log_value
        steps = [
            step("SIGNAL_SETUP", "dB power ratio",
                 f"P2/P1={fraction_text(ratio)}"),
            step("DB_FORMULA", "G_dB=10*log10(P2/P1)"),
            step("LOG_SUPPLIED", f"log10({fraction_text(ratio)})",
                 log_value),
            step("M", 10, log_value, db_value),
            step("CHECK", "positive is gain, negative is loss",
                 f"{db_value} dB"),
        ]
        answer = f"G={db_value} dB"
        problem = (
            f"For a power ratio P2/P1={fraction_text(ratio)}, use supplied "
            f"log10(P2/P1)={log_value} to compute gain in dB."
        )
        return problem, steps, answer
