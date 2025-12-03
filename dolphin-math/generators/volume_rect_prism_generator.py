import random
from base_generator import ProblemGenerator
from helpers import step, jid


class VolumeRectPrismGenerator(ProblemGenerator):
    """Computes volume of a rectangular prism with explicit multiplication steps."""

    def generate(self) -> dict:
        length = random.randint(2, 15)
        width = random.randint(2, 15)
        height = random.randint(2, 15)

        # Volume = length * width * height
        steps = []
        lw = length * width
        steps.append(step("M", length, width, lw))
        vol = lw * height
        steps.append(step("M", lw, height, vol))
        steps.append(step("VOLUME", vol))
        steps.append(step("Z", str(vol)))

        return dict(
            problem_id=jid(),
            operation="volume_rect_prism",
            problem=f"Find volume of rectangular prism: L={length}, W={width}, H={height}",
            steps=steps,
            final_answer=str(vol),
        )
