import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def vector_text(values):
    return "(" + ",".join(str(value) for value in values) + ")"


def fraction_vector_text(values):
    return "(" + ",".join(fraction_text(value) for value in values) + ")"


def round_half_up(value):
    return math.floor(value + Fraction(1, 2))


class QuantizationGenerator(ProblemGenerator):
    """
    Int8 affine quantize, dequantize, and round-trip error.

    Uses q = round(x/scale) + zero_point, with exact Fraction arithmetic and
    generated values that avoid half-way rounding ties.

    Op-codes used:
    - QUANT_SETUP / ROUND / QUANT_VALUE / DEQUANT_VALUE / ABS_ERROR /
      ROUNDTRIP_ERROR
    - D / A / S / M (established/shared): scale, zero-point, dequant, errors
    - Z: quantized tensor, dequantized tensor, sum absolute error
    """

    def generate(self) -> dict:
        scale = random.choice([Fraction(1, 10), Fraction(1, 20),
                               Fraction(1, 25)])
        zero_point = random.randint(-10, 10)
        raw_values = []
        while len(raw_values) < 3:
            numerator = random.randint(-200, 200)
            if numerator % 10 == 5:
                continue
            value = Fraction(numerator, 100)
            shifted = value / scale + zero_point
            q_value = round_half_up(shifted)
            if -128 <= q_value <= 127:
                raw_values.append(value)

        q_values = []
        dequantized = []
        abs_errors = []
        steps = [
            step("QUANT_SETUP", f"x={fraction_vector_text(raw_values)}",
                 f"scale={fraction_text(scale)}", f"zero_point={zero_point}"),
        ]
        for index, value in enumerate(raw_values, start=1):
            scaled = value / scale
            shifted = scaled + zero_point
            q_value = round_half_up(shifted)
            q_minus_zp = q_value - zero_point
            deq = q_minus_zp * scale
            error = value - deq
            abs_error = abs(error)
            steps.extend([
                step("D", fraction_text(value), fraction_text(scale),
                     fraction_text(scaled)),
                step("A", fraction_text(scaled), zero_point,
                     fraction_text(shifted)),
                step("ROUND", fraction_text(shifted), q_value),
                step("QUANT_VALUE", index, q_value),
                step("S", q_value, zero_point, q_minus_zp),
                step("M", q_minus_zp, fraction_text(scale),
                     fraction_text(deq)),
                step("DEQUANT_VALUE", index, fraction_text(deq)),
                step("S", fraction_text(value), fraction_text(deq),
                     fraction_text(error)),
                step("ABS_ERROR", index, fraction_text(abs_error)),
            ])
            q_values.append(q_value)
            dequantized.append(deq)
            abs_errors.append(abs_error)

        running = Fraction(0)
        for abs_error in abs_errors:
            new_running = running + abs_error
            steps.append(step("A", fraction_text(running),
                              fraction_text(abs_error),
                              fraction_text(new_running)))
            running = new_running
        steps.append(step("ROUNDTRIP_ERROR", "sum_abs", fraction_text(running)))
        answer = (
            f"q={vector_text(q_values)}; dequant={fraction_vector_text(dequantized)}; "
            f"sum_abs_error={fraction_text(running)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Quantize tensor x={fraction_vector_text(raw_values)} with int8 "
            f"scale={fraction_text(scale)} and zero_point={zero_point} using "
            "q=round(x/scale)+zero_point, then dequantize and compute sum "
            "absolute round-trip error."
        )
        return dict(
            problem_id=jid(),
            operation="quantization_int8_affine",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
