import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def sqrt_text(value):
    value = Fraction(value)
    if value == 1:
        return "1"
    return f"sqrt({fraction_text(value)})"


class WavefunctionGenerator(ProblemGenerator):
    """
    Normalize simple wavefunctions and compute expectation values by integration.

    Variant:
    - power_interval: psi(x)=N*(x/L)^k on 0<=x<=L

    Op-codes used:
    - WAVE_SETUP: wavefunction and interval
    - WAVE_FORMULA: normalization or expectation relation
    - POWER_INTEGRAL: simplified interval integral for a power moment
    - A / M / D (established/shared): exact coefficient arithmetic
    - Z: normalization constant and expectations
    """

    VARIANTS = ["power_interval"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or "power_interval"
        power = random.randint(0, 10)
        length = random.randint(1, 50)
        two_k = 2 * power
        norm_num = two_k + 1
        norm_sq = Fraction(norm_num, length)
        norm = sqrt_text(norm_sq)
        x_den = two_k + 2
        x_num = norm_num * length
        x_expect = Fraction(x_num, x_den)
        x2_den = two_k + 3
        length_sq = length ** 2
        x2_num = norm_num * length_sq
        x2_expect = Fraction(x2_num, x2_den)
        steps = [
            step("WAVE_SETUP", variant, f"psi=N*(x/L)^{power}",
                 f"0<=x<={length}"),
            step("WAVE_FORMULA",
                 "1=N^2*integral_0^L (x/L)^(2k) dx"),
            step("M", 2, power, two_k),
            step("A", two_k, 1, norm_num),
            step("POWER_INTEGRAL", f"n={two_k}", f"L/{norm_num}"),
            step("D", norm_num, length, fraction_text(norm_sq)),
            step("WAVE_FORMULA", f"N^2={fraction_text(norm_sq)}"),
            step("WAVE_FORMULA",
                 "<x>=N^2*integral_0^L x*(x/L)^(2k) dx"),
            step("A", two_k, 2, x_den),
            step("POWER_INTEGRAL", f"n={two_k + 1}", f"L^2/{x_den}"),
            step("M", norm_num, length, x_num),
            step("D", x_num, x_den, fraction_text(x_expect)),
            step("WAVE_FORMULA",
                 "<x^2>=N^2*integral_0^L x^2*(x/L)^(2k) dx"),
            step("A", two_k, 3, x2_den),
            step("POWER_INTEGRAL", f"n={two_k + 2}", f"L^3/{x2_den}"),
            step("E", length, 2, length_sq),
            step("M", norm_num, length_sq, x2_num),
            step("D", x2_num, x2_den, fraction_text(x2_expect)),
        ]
        answer = (
            f"N={norm}; <x>={fraction_text(x_expect)}; "
            f"<x^2>={fraction_text(x2_expect)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"On 0<=x<={length}, let psi(x)=N*(x/L)^{power}. Normalize it "
            "and compute <x> and <x^2>."
        )
        return dict(
            problem_id=jid(),
            operation=f"wavefunction_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
