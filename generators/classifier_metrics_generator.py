import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class ClassifierMetricsGenerator(ProblemGenerator):
    """
    Precision, recall, and F1 from a binary confusion matrix.

    Counts are positive where needed so every denominator is nonzero. The
    metrics are emitted as exact reduced fractions for the positive class.

    Op-codes used:
    - METRICS_SETUP / METRIC_FORMULA
    - A / M / D (established/shared): exact denominators and F1 arithmetic
    - Z: precision, recall, and F1
    """

    def generate(self) -> dict:
        tp = random.randint(1, 40)
        fp = random.randint(1, 30)
        fn = random.randint(1, 30)
        tn = random.randint(1, 50)

        predicted_positive = tp + fp
        actual_positive = tp + fn
        precision = Fraction(tp, predicted_positive)
        recall = Fraction(tp, actual_positive)
        product = precision * recall
        f1_numerator = 2 * product
        f1_denominator = precision + recall
        f1 = f1_numerator / f1_denominator

        steps = [
            step("METRICS_SETUP", f"TP={tp}, FP={fp}, FN={fn}, TN={tn}"),
            step("METRIC_FORMULA", "precision=TP/(TP+FP)"),
            step("A", tp, fp, predicted_positive),
            step("D", tp, predicted_positive, fraction_text(precision)),
            step("METRIC_FORMULA", "recall=TP/(TP+FN)"),
            step("A", tp, fn, actual_positive),
            step("D", tp, actual_positive, fraction_text(recall)),
            step("METRIC_FORMULA", "F1=2PR/(P+R)"),
            step("M", fraction_text(precision), fraction_text(recall),
                 fraction_text(product)),
            step("M", 2, fraction_text(product), fraction_text(f1_numerator)),
            step("A", fraction_text(precision), fraction_text(recall),
                 fraction_text(f1_denominator)),
            step("D", fraction_text(f1_numerator),
                 fraction_text(f1_denominator), fraction_text(f1)),
        ]
        answer = (
            f"precision={fraction_text(precision)}; "
            f"recall={fraction_text(recall)}; F1={fraction_text(f1)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Given confusion matrix counts TP={tp}, FP={fp}, FN={fn}, "
            f"TN={tn}, compute precision, recall, and F1 for the positive "
            "class."
        )
        return dict(
            problem_id=jid(),
            operation="classifier_precision_recall_f1",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
