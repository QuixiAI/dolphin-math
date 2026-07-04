import random

from base_generator import ProblemGenerator
from helpers import step, jid


def seq_text(values):
    return "[" + ",".join(str(value) for value in values) + "]"


def complex_text(real, imag=0):
    if imag == 0:
        return str(real)
    if real == 0:
        if imag == 1:
            return "i"
        if imag == -1:
            return "-i"
        return f"{imag}i"
    if imag > 0:
        imag_text = "i" if imag == 1 else f"{imag}i"
        return f"{real}+{imag_text}"
    imag_text = "i" if imag == -1 else f"{-imag}i"
    return f"{real}-{imag_text}"


def dft_values(values):
    if len(values) == 2:
        x0, x1 = values
        return [complex_text(x0 + x1), complex_text(x0 - x1)]
    x0, x1, x2, x3 = values
    return [
        complex_text(x0 + x1 + x2 + x3),
        complex_text(x0 - x2, x3 - x1),
        complex_text(x0 - x1 + x2 - x3),
        complex_text(x0 - x2, x1 - x3),
    ]


class DFTGenerator(ProblemGenerator):
    """
    Length-2 and length-4 discrete Fourier transforms with exact twiddles.

    Op-codes used:
    - DFT_SETUP: length and input signal
    - TWIDDLE: exact root-of-unity values
    - DFT_BIN: output bin formula/result
    - A / S (established/shared): exact real/imag arithmetic
    - Z: DFT vector
    """

    LENGTHS = [2, 4]

    def __init__(self, length=None):
        if length is not None and length not in self.LENGTHS:
            raise ValueError(f"length must be one of {self.LENGTHS} or None")
        self.length = length

    def generate(self) -> dict:
        length = self.length or random.choice(self.LENGTHS)
        values = [random.randint(-6, 9) for _ in range(length)]
        if length == 2:
            steps, answer = self._steps_len2(values)
        else:
            steps, answer = self._steps_len4(values)
        steps.append(step("Z", answer))
        problem = f"Compute the length-{length} DFT of x={seq_text(values)}."
        return dict(
            problem_id=jid(),
            operation=f"dft_length_{length}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _steps_len2(self, values):
        x0, x1 = values
        x0_plus_x1 = x0 + x1
        x0_minus_x1 = x0 - x1
        outputs = [complex_text(x0_plus_x1), complex_text(x0_minus_x1)]
        steps = [
            step("DFT_SETUP", "N=2", f"x={seq_text(values)}"),
            step("TWIDDLE", "W2=-1"),
            step("DFT_BIN", "X0=x0+x1"),
            step("A", x0, x1, x0_plus_x1),
            step("DFT_BIN", "X1=x0-x1"),
            step("S", x0, x1, x0_minus_x1),
        ]
        return steps, f"X={seq_text(outputs)}"

    def _steps_len4(self, values):
        x0, x1, x2, x3 = values
        x0_x1 = x0 + x1
        x0_x1_x2 = x0_x1 + x2
        X0 = x0_x1_x2 + x3
        real13 = x0 - x2
        imag1 = x3 - x1
        x0_minus_x1 = x0 - x1
        x0_minus_x1_plus_x2 = x0_minus_x1 + x2
        X2 = x0_minus_x1_plus_x2 - x3
        imag3 = x1 - x3
        outputs = [
            complex_text(X0),
            complex_text(real13, imag1),
            complex_text(X2),
            complex_text(real13, imag3),
        ]
        steps = [
            step("DFT_SETUP", "N=4", f"x={seq_text(values)}"),
            step("TWIDDLE", "W4=-i", "W4^2=-1", "W4^3=i"),
            step("DFT_BIN", "X0=x0+x1+x2+x3"),
            step("A", x0, x1, x0_x1),
            step("A", x0_x1, x2, x0_x1_x2),
            step("A", x0_x1_x2, x3, X0),
            step("DFT_BIN", "X1=(x0-x2)+(x3-x1)i"),
            step("S", x0, x2, real13),
            step("S", x3, x1, imag1),
            step("DFT_BIN", f"X1={complex_text(real13, imag1)}"),
            step("DFT_BIN", "X2=x0-x1+x2-x3"),
            step("S", x0, x1, x0_minus_x1),
            step("A", x0_minus_x1, x2, x0_minus_x1_plus_x2),
            step("S", x0_minus_x1_plus_x2, x3, X2),
            step("DFT_BIN", "X3=(x0-x2)+(x1-x3)i"),
            step("S", x0, x2, real13),
            step("S", x1, x3, imag3),
            step("DFT_BIN", f"X3={complex_text(real13, imag3)}"),
        ]
        return steps, f"X={seq_text(outputs)}"
