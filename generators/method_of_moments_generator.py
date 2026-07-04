import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def data_text(values):
    return "[" + ",".join(str(v) for v in values) + "]"


def sum_expr(values):
    return " + ".join(str(v) for v in values)


class MethodOfMomentsGenerator(ProblemGenerator):
    """
    First-moment method-of-moments estimators.

    Variants:
    - poisson: E[X]=lambda
    - exponential: E[X]=1/lambda
    - uniform_zero_theta: E[X]=theta/2

    Op-codes used:
    - MOM_SETUP: model, parameter, and data
    - COUNT / SUM: sample size and total
    - SAMPLE_MOMENT: sample mean
    - MOM_EQUATION: population moment matched to sample moment
    - REWRITE: solved estimating equation
    - D / M (established/shared): exact estimator arithmetic
    - CHECK: domain check
    - Z: sample moment and estimator
    """

    VARIANTS = ["poisson", "exponential", "uniform_zero_theta"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "poisson":
            problem, steps, answer = self._generate_poisson()
        elif variant == "exponential":
            problem, steps, answer = self._generate_exponential()
        else:
            problem, steps, answer = self._generate_uniform()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"method_of_moments_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _summary_steps(self, model, parameter, values):
        n = len(values)
        total = sum(values)
        mean = Fraction(total, n)
        steps = [
            step("MOM_SETUP", model, f"parameter={parameter}",
                 f"data={data_text(values)}"),
            step("COUNT", "n", n),
            step("SUM", "sum x_i", sum_expr(values), total),
            step("D", total, n, fraction_text(mean)),
            step("SAMPLE_MOMENT", "xbar", fraction_text(mean)),
        ]
        return n, total, mean, steps

    def _generate_poisson(self):
        n = random.randint(3, 10)
        values = [random.randint(0, 9) for _ in range(n)]
        if sum(values) == 0:
            values[random.randrange(n)] = random.randint(1, 9)
        _, _, mean, steps = self._summary_steps("poisson", "lambda", values)
        lambda_hat = mean
        steps += [
            step("MOM_EQUATION", "E[X]=lambda", "xbar=lambda"),
            step("REWRITE", f"lambda_hat={fraction_text(lambda_hat)}"),
            step("CHECK", f"lambda_hat={fraction_text(lambda_hat)}>=0",
                 "valid Poisson parameter"),
        ]
        answer = (
            f"xbar={fraction_text(mean)}; "
            f"lambda_hat={fraction_text(lambda_hat)}"
        )
        problem = (
            f"For data {data_text(values)} from a Poisson(lambda) model, "
            "use the first moment equation to find the method-of-moments "
            "estimator lambda_hat."
        )
        return problem, steps, answer

    def _generate_exponential(self):
        n = random.randint(3, 10)
        values = [random.randint(1, 12) for _ in range(n)]
        _, total, mean, steps = self._summary_steps(
            "exponential", "lambda", values
        )
        lambda_hat = Fraction(n, total)
        steps += [
            step("MOM_EQUATION", "E[X]=1/lambda", "xbar=1/lambda"),
            step("REWRITE", "lambda_hat=1/xbar"),
            step("D", n, total, fraction_text(lambda_hat)),
            step("CHECK", f"lambda_hat={fraction_text(lambda_hat)}>0",
                 "valid rate parameter"),
        ]
        answer = (
            f"xbar={fraction_text(mean)}; "
            f"lambda_hat={fraction_text(lambda_hat)}"
        )
        problem = (
            f"For data {data_text(values)} from an Exponential(lambda) "
            "model, use E[X]=1/lambda to find the method-of-moments "
            "estimator lambda_hat."
        )
        return problem, steps, answer

    def _generate_uniform(self):
        n = random.randint(3, 10)
        values = [random.randint(1, 20) for _ in range(n)]
        _, _, mean, steps = self._summary_steps(
            "uniform_zero_theta", "theta", values
        )
        theta_hat = 2 * mean
        steps += [
            step("MOM_EQUATION", "E[X]=theta/2", "xbar=theta/2"),
            step("REWRITE", "theta_hat=2*xbar"),
            step("M", 2, fraction_text(mean), fraction_text(theta_hat)),
            step("CHECK", f"theta_hat={fraction_text(theta_hat)}>0",
                 "valid upper endpoint"),
        ]
        answer = (
            f"xbar={fraction_text(mean)}; "
            f"theta_hat={fraction_text(theta_hat)}"
        )
        problem = (
            f"For data {data_text(values)} from a Uniform(0,theta) model, "
            "use E[X]=theta/2 to find the method-of-moments estimator "
            "theta_hat."
        )
        return problem, steps, answer
