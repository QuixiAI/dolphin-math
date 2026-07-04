import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def over_pi_text(value):
    value = Fraction(value)
    if value == 0:
        return "0"
    if value.denominator == 1:
        return f"{value.numerator}/pi"
    return f"({value.numerator}/{value.denominator})/pi"


class FourierSeriesGenerator(ProblemGenerator):
    """
    Fourier sine coefficients for square and sawtooth waves.

    Variants:
    - square: odd square wave with amplitude A
    - sawtooth: f(x)=A*x on (-pi,pi)

    Op-codes used:
    - FOURIER_SETUP: waveform and requested coefficient
    - SYMMETRY: odd/even coefficient simplification
    - INTEGRAL / ANTIDERIVATIVE / INTEGRATION_BY_PARTS: calculus setup
    - PARITY: (-1)^n value
    - S / M / D (established/shared): exact coefficient arithmetic
    - FOURIER_COEF: final coefficient form
    - Z: requested Fourier coefficient
    """

    VARIANTS = ["square", "sawtooth"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "square":
            problem, steps, answer = self._generate_square()
        else:
            problem, steps, answer = self._generate_sawtooth()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"fourier_series_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_square(self):
        amplitude = random.randint(1, 12)
        n = random.randint(1, 12)
        parity = -1 if n % 2 else 1
        factor = 1 - parity
        two_a = 2 * amplitude
        numerator = two_a * factor
        rational_part = Fraction(numerator, n)
        coefficient = over_pi_text(rational_part)
        steps = [
            step("FOURIER_SETUP", "square",
                 f"A={amplitude}", f"n={n}"),
            step("SYMMETRY", "odd function", "a0=0, a_n=0"),
            step("INTEGRAL", "b_n=(2/pi)*int_0^pi A sin(nx) dx"),
            step("ANTIDERIVATIVE", "-A*cos(nx)/n"),
            step("PARITY", f"(-1)^n={parity}"),
            step("S", 1, parity, factor),
            step("M", 2, amplitude, two_a),
            step("M", two_a, factor, numerator),
            step("D", numerator, n, fraction_text(rational_part)),
            step("FOURIER_COEF", f"b_{n}={coefficient}"),
        ]
        answer = f"a0=0, a_n=0, b_{n}={coefficient}"
        problem = (
            f"For the 2pi-periodic square wave f(x)={amplitude} on (0,pi) "
            f"and -{amplitude} on (-pi,0), compute b_{n} by integration."
        )
        return problem, steps, answer

    def _generate_sawtooth(self):
        amplitude = random.randint(1, 12)
        n = random.randint(1, 12)
        parity = 1 if n % 2 else -1
        two_a = 2 * amplitude
        signed_num = two_a * parity
        coefficient = Fraction(signed_num, n)
        steps = [
            step("FOURIER_SETUP", "sawtooth",
                 f"A={amplitude}", f"n={n}"),
            step("SYMMETRY", "odd function", "a0=0, a_n=0"),
            step("INTEGRAL", "b_n=(1/pi)*int_-pi^pi A*x*sin(nx) dx"),
            step("INTEGRATION_BY_PARTS", "u=x", "dv=sin(nx)dx"),
            step("PARITY", f"(-1)^(n+1)={parity}"),
            step("M", 2, amplitude, two_a),
            step("M", two_a, parity, signed_num),
            step("D", signed_num, n, fraction_text(coefficient)),
            step("FOURIER_COEF", f"b_{n}={fraction_text(coefficient)}"),
        ]
        answer = f"a0=0, a_n=0, b_{n}={fraction_text(coefficient)}"
        problem = (
            f"For the 2pi-periodic sawtooth f(x)={amplitude}*x on "
            f"(-pi,pi), compute b_{n} by integration."
        )
        return problem, steps, answer
