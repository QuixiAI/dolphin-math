import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class OpticsGenerator(ProblemGenerator):
    """
    Exact geometric-optics arithmetic: Snell's law, thin lenses, and mirrors.

    Variants:
    - snell: solve sin(theta2)=n1*sin(theta1)/n2.
    - thin_lens: solve 1/di=1/f-1/do.
    - mirror_magnification: compute di, magnification, and image height.

    Op-codes used:
    - OPTICS_SETUP / OPTICS_FORMULA
    - A / S / M / D (established/shared): exact optical arithmetic
    - Z: refracted sine, image distance, or magnification and height
    """

    VARIANTS = ["snell", "thin_lens", "mirror_magnification"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "snell":
            problem, steps, answer = self._generate_snell()
        elif variant == "thin_lens":
            problem, steps, answer = self._generate_thin_lens()
        else:
            problem, steps, answer = self._generate_mirror_magnification()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"optics_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_snell(self):
        n1 = random.randint(1, 6)
        n2 = random.randint(n1, 10)
        sin1 = Fraction(random.randint(1, n2), n2)
        product = n1 * sin1
        sin2 = product / n2
        steps = [
            step("OPTICS_SETUP", "snell", f"n1={n1}, n2={n2}",
                 f"sin(theta1)={fraction_text(sin1)}"),
            step("OPTICS_FORMULA", "n1*sin(theta1)=n2*sin(theta2)"),
            step("M", n1, fraction_text(sin1), fraction_text(product)),
            step("D", fraction_text(product), n2, fraction_text(sin2)),
        ]
        answer = f"sin(theta2)={fraction_text(sin2)}"
        problem = (
            f"A ray goes from medium n1={n1} to n2={n2}. Given "
            f"sin(theta1)={fraction_text(sin1)}, use Snell's law to find "
            "sin(theta2)."
        )
        return problem, steps, answer

    def _generate_thin_lens(self):
        focal = random.randint(2, 30)
        object_distance = random.randint(focal + 1, focal + 80)
        inv_f = Fraction(1, focal)
        inv_do = Fraction(1, object_distance)
        inv_di = inv_f - inv_do
        image_distance = Fraction(1, inv_di)
        steps = [
            step("OPTICS_SETUP", "thin_lens",
                 f"f={focal}", f"d_o={object_distance}"),
            step("OPTICS_FORMULA", "1/f=1/d_o+1/d_i"),
            step("D", 1, focal, fraction_text(inv_f)),
            step("D", 1, object_distance, fraction_text(inv_do)),
            step("S", fraction_text(inv_f), fraction_text(inv_do),
                 fraction_text(inv_di)),
            step("D", 1, fraction_text(inv_di),
                 fraction_text(image_distance)),
        ]
        answer = f"d_i={fraction_text(image_distance)} cm"
        problem = (
            f"A thin lens has focal length f={focal} cm and object distance "
            f"d_o={object_distance} cm. Find image distance d_i."
        )
        return problem, steps, answer

    def _generate_mirror_magnification(self):
        focal = random.randint(2, 30)
        object_distance = random.randint(focal + 1, focal + 80)
        object_height = random.randint(1, 20)
        inv_f = Fraction(1, focal)
        inv_do = Fraction(1, object_distance)
        inv_di = inv_f - inv_do
        image_distance = Fraction(1, inv_di)
        magnification = -image_distance / object_distance
        image_height = magnification * object_height
        steps = [
            step("OPTICS_SETUP", "mirror_magnification",
                 f"f={focal}, d_o={object_distance}", f"h_o={object_height}"),
            step("OPTICS_FORMULA", "1/f=1/d_o+1/d_i"),
            step("D", 1, focal, fraction_text(inv_f)),
            step("D", 1, object_distance, fraction_text(inv_do)),
            step("S", fraction_text(inv_f), fraction_text(inv_do),
                 fraction_text(inv_di)),
            step("D", 1, fraction_text(inv_di),
                 fraction_text(image_distance)),
            step("OPTICS_FORMULA", "m=-d_i/d_o, h_i=m*h_o"),
            step("D", fraction_text(-image_distance), object_distance,
                 fraction_text(magnification)),
            step("M", fraction_text(magnification), object_height,
                 fraction_text(image_height)),
        ]
        answer = (
            f"d_i={fraction_text(image_distance)} cm; "
            f"m={fraction_text(magnification)}; "
            f"h_i={fraction_text(image_height)} cm"
        )
        problem = (
            f"A concave mirror has focal length f={focal} cm, object distance "
            f"d_o={object_distance} cm, and object height h_o={object_height} "
            "cm. Find d_i, magnification m, and image height h_i."
        )
        return problem, steps, answer
