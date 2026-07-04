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


class MLEGenerator(ProblemGenerator):
    """
    Maximum-likelihood estimates from log-likelihood score equations.

    Variants:
    - bernoulli: estimate p from 0/1 data
    - exponential: estimate lambda from positive observations
    - normal_mu: estimate mu with known sigma^2

    Op-codes used:
    - MLE_SETUP: model, parameter, and data
    - COUNT / SUM: sufficient statistics
    - LOG_LIKELIHOOD: log-likelihood up to standard constants
    - DERIVATIVE: score function
    - SCORE_EQ: score equation set to zero
    - REWRITE: simplified estimating equation
    - A / S / D (established/shared): exact arithmetic
    - CHECK: parameter-domain check
    - Z: log-likelihood, score, and MLE
    """

    VARIANTS = ["bernoulli", "exponential", "normal_mu"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "bernoulli":
            problem, steps, answer = self._generate_bernoulli()
        elif variant == "exponential":
            problem, steps, answer = self._generate_exponential()
        else:
            problem, steps, answer = self._generate_normal_mu()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"mle_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_bernoulli(self):
        n = random.randint(5, 18)
        successes = random.randint(1, n - 1)
        values = [1] * successes + [0] * (n - successes)
        random.shuffle(values)
        failures = n - successes
        p_hat = Fraction(successes, n)
        loglik = f"ell(p)={successes}*log(p)+{failures}*log(1-p)"
        score = f"score={successes}/p-{failures}/(1-p)"
        steps = [
            step("MLE_SETUP", "bernoulli", "parameter=p",
                 f"data={data_text(values)}"),
            step("COUNT", "n", n),
            step("COUNT", "sum x_i", successes),
            step("S", n, successes, failures),
            step("LOG_LIKELIHOOD", loglik),
            step("DERIVATIVE", score),
            step("SCORE_EQ", f"{successes}/p={failures}/(1-p)"),
            step("REWRITE", f"{successes}={n}*p"),
            step("D", successes, n, fraction_text(p_hat)),
            step("CHECK", f"0<={fraction_text(p_hat)}<=1",
                 "valid Bernoulli parameter"),
        ]
        answer = f"{loglik}; {score}; p_hat={fraction_text(p_hat)}"
        problem = (
            f"For Bernoulli data {data_text(values)}, write the "
            "log-likelihood for p, differentiate, and solve for the MLE "
            "p_hat."
        )
        return problem, steps, answer

    def _generate_exponential(self):
        n = random.randint(3, 9)
        values = [random.randint(1, 12) for _ in range(n)]
        total = sum(values)
        lambda_hat = Fraction(n, total)
        loglik = f"ell(lambda)={n}*log(lambda)-{total}*lambda"
        score = f"score={n}/lambda-{total}"
        steps = [
            step("MLE_SETUP", "exponential", "parameter=lambda",
                 f"data={data_text(values)}"),
            step("COUNT", "n", n),
            step("SUM", "sum x_i", sum_expr(values), total),
            step("LOG_LIKELIHOOD", loglik),
            step("DERIVATIVE", score),
            step("SCORE_EQ", f"{n}/lambda={total}"),
            step("D", n, total, fraction_text(lambda_hat)),
            step("CHECK", f"lambda_hat={fraction_text(lambda_hat)}>0",
                 "valid rate parameter"),
        ]
        answer = (
            f"{loglik}; {score}; lambda_hat={fraction_text(lambda_hat)}"
        )
        problem = (
            f"For exponential data {data_text(values)}, write the "
            "log-likelihood for lambda, differentiate, and solve for the "
            "MLE lambda_hat."
        )
        return problem, steps, answer

    def _generate_normal_mu(self):
        n = random.randint(3, 9)
        values = [random.randint(-8, 12) for _ in range(n)]
        sigma_sq = random.choice([1, 2, 3, 4, 5, 6, 8, 9])
        total = sum(values)
        mu_hat = Fraction(total, n)
        loglik = f"ell(mu)=-(1/(2*{sigma_sq}))*sum((x_i-mu)^2)+C"
        score = f"score=({total}-{n}*mu)/{sigma_sq}"
        steps = [
            step("MLE_SETUP", "normal_mu", "parameter=mu",
                 f"sigma^2={sigma_sq}"),
            step("MLE_SETUP", "data", data_text(values)),
            step("COUNT", "n", n),
            step("SUM", "sum x_i", sum_expr(values), total),
            step("LOG_LIKELIHOOD", loglik),
            step("DERIVATIVE", score),
            step("SCORE_EQ", f"{total}-{n}*mu=0"),
            step("REWRITE", f"{total}={n}*mu"),
            step("D", total, n, fraction_text(mu_hat)),
            step("CHECK", "mu_hat can be any real number",
                 fraction_text(mu_hat)),
        ]
        answer = f"{loglik}; {score}; mu_hat={fraction_text(mu_hat)}"
        problem = (
            f"For normal data {data_text(values)} with known "
            f"sigma^2={sigma_sq}, write the log-likelihood for mu, "
            "differentiate, and solve for the MLE mu_hat."
        )
        return problem, steps, answer
