import random

from base_generator import ProblemGenerator
from helpers import step, jid


VARIANTS = ["three_point_epoch", "four_point_epoch"]


def tuple_text(values):
    return "(" + ",".join(str(value) for value in values) + ")"


def samples_text(samples):
    return "[" + ", ".join(tuple_text(sample) for sample in samples) + "]"


def label_from_score(score):
    return 1 if score > 0 else -1


def make_samples(count):
    for _ in range(100):
        true_weights = [
            random.randint(-2, 2),
            random.choice([-3, -2, -1, 1, 2, 3]),
            random.choice([-3, -2, -1, 1, 2, 3]),
        ]
        points = random.sample(
            [(x1, x2) for x1 in range(-3, 4) for x2 in range(-3, 4)
             if (x1, x2) != (0, 0)],
            count,
        )
        samples = []
        for x1, x2 in points:
            score = true_weights[0] + true_weights[1] * x1 + true_weights[2] * x2
            if score == 0:
                break
            samples.append((x1, x2, label_from_score(score)))
        if len(samples) == count:
            return samples
    return [(1, 1, 1), (-1, 2, -1), (2, -1, 1)][:count]


def epoch_update(samples, weights, eta):
    weights = list(weights)
    mistakes = 0
    trace = []
    for index, (x1, x2, label) in enumerate(samples, start=1):
        old_weights = list(weights)
        term1 = weights[1] * x1
        partial = weights[0] + term1
        term2 = weights[2] * x2
        score = partial + term2
        margin = label * score
        update = margin <= 0
        detail = {
            "index": index,
            "x1": x1,
            "x2": x2,
            "label": label,
            "old_weights": old_weights,
            "term1": term1,
            "partial": partial,
            "term2": term2,
            "score": score,
            "margin": margin,
            "update": update,
        }
        if update:
            mistakes += 1
            eta_y = eta * label
            delta0 = eta_y
            delta1 = eta_y * x1
            delta2 = eta_y * x2
            weights = [
                weights[0] + delta0,
                weights[1] + delta1,
                weights[2] + delta2,
            ]
            detail.update({
                "eta_y": eta_y,
                "delta0": delta0,
                "delta1": delta1,
                "delta2": delta2,
                "new_weights": list(weights),
            })
        else:
            detail["new_weights"] = list(weights)
        trace.append(detail)
    return weights, mistakes, trace


class PerceptronGenerator(ProblemGenerator):
    """
    Perceptron updates over one ordered epoch of a small labeled dataset.

    Variants:
    - three_point_epoch: run one epoch over three labeled 2D examples.
    - four_point_epoch: run one epoch over four labeled 2D examples.

    Op-codes used:
    - PERCEPTRON_SETUP / PERCEPTRON_RULE / PERCEPTRON_SAMPLE
    - PERCEPTRON_SCORE / PERCEPTRON_UPDATE / CHECK
    - A / M (established/shared): exact score and update arithmetic
    - Z: final weights and number of updates
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        count = 3 if variant == "three_point_epoch" else 4
        eta = random.choice([1, 2])

        for _ in range(100):
            samples = make_samples(count)
            weights = [random.randint(-2, 2) for _ in range(3)]
            final_weights, mistakes, trace = epoch_update(samples, weights, eta)
            if mistakes:
                break
        else:
            samples = make_samples(count)
            weights = [0, 0, 0]
            final_weights, mistakes, trace = epoch_update(samples, weights, eta)

        steps = [
            step("PERCEPTRON_SETUP", f"eta={eta}",
                 f"w={tuple_text(weights)}",
                 f"samples={samples_text(samples)}"),
            step("PERCEPTRON_RULE", "score=w0+w1*x1+w2*x2",
                 "if y*score <= 0 update"),
        ]
        for item in trace:
            steps.extend([
                step("PERCEPTRON_SAMPLE", f"i={item['index']}",
                     f"x=({item['x1']},{item['x2']})",
                     f"y={item['label']}"),
                step("M", item["old_weights"][1], item["x1"], item["term1"]),
                step("A", item["old_weights"][0], item["term1"],
                     item["partial"]),
                step("M", item["old_weights"][2], item["x2"], item["term2"]),
                step("A", item["partial"], item["term2"], item["score"]),
                step("PERCEPTRON_SCORE", f"i={item['index']}",
                     f"score={item['score']}"),
                step("M", item["label"], item["score"], item["margin"]),
                step("CHECK", f"i={item['index']}",
                     f"y*score={item['margin']}",
                     "update" if item["update"] else "keep"),
            ])
            if item["update"]:
                steps.extend([
                    step("M", eta, item["label"], item["eta_y"]),
                    step("M", item["eta_y"], 1, item["delta0"]),
                    step("A", item["old_weights"][0], item["delta0"],
                         item["new_weights"][0]),
                    step("M", item["eta_y"], item["x1"], item["delta1"]),
                    step("A", item["old_weights"][1], item["delta1"],
                         item["new_weights"][1]),
                    step("M", item["eta_y"], item["x2"], item["delta2"]),
                    step("A", item["old_weights"][2], item["delta2"],
                         item["new_weights"][2]),
                    step("PERCEPTRON_UPDATE", f"i={item['index']}",
                         f"w={tuple_text(item['new_weights'])}"),
                ])
            else:
                steps.append(step("PERCEPTRON_UPDATE", f"i={item['index']}",
                                  "no change",
                                  f"w={tuple_text(item['new_weights'])}"))

        answer = (
            f"w_final={tuple_text(final_weights)}; updates={mistakes}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Run one perceptron epoch with eta={eta}, starting weights "
            f"w={tuple_text(weights)} for samples {samples_text(samples)}. "
            "Use bias feature x0=1, score=w0+w1*x1+w2*x2, and update when "
            "y*score <= 0."
        )
        return dict(
            problem_id=jid(),
            operation=f"perceptron_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
