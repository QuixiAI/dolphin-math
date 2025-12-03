import random
from generators.mixed_number_operation_generator import MixedNumberOperationGenerator


class MixedNumberOperationsRandom:
    """
    Wrapper generator that randomly picks +, -, *, / mixed-number operation.
    Useful for sampling/dataset inclusion without listing each op separately.
    """

    def __init__(self):
        self.variants = [
            MixedNumberOperationGenerator('+'),
            MixedNumberOperationGenerator('-'),
            MixedNumberOperationGenerator('*'),
            MixedNumberOperationGenerator('/'),
        ]

    def generate(self):
        gen = random.choice(self.variants)
        return gen.generate()
