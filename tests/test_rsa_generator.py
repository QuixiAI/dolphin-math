import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.rsa_generator import RSAGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For RSA primes p=(\d+) and q=(\d+) with public exponent e=(\d+) "
    r"and message m=(\d+), compute n, phi\(n\), d, encrypt, and decrypt\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    p, q, e, message = map(int, match.groups())
    return p, q, e, message


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def extended_trace(a, b):
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    steps = [
        make_step("EXT_GCD_SETUP", a, b),
        make_step("BACK_SUB_ROW", f"r={old_r}", f"x={old_x}", f"y={old_y}"),
        make_step("BACK_SUB_ROW", f"r={r}", f"x={x}", f"y={y}"),
    ]
    while r != 0:
        q = old_r // r
        product = q * r
        new_r = old_r - product
        steps.append(make_step("EUCLID_DIV", old_r, r, q, new_r))
        steps.append(make_step("M", q, r, product))
        steps.append(make_step("S", old_r, product, new_r))

        qx = q * x
        new_x = old_x - qx
        steps.append(make_step("M", q, x, qx))
        steps.append(make_step("S", old_x, qx, new_x))

        qy = q * y
        new_y = old_y - qy
        steps.append(make_step("M", q, y, qy))
        steps.append(make_step("S", old_y, qy, new_y))
        steps.append(make_step("BACK_SUB_ROW", f"r={new_r}",
                               f"x={new_x}", f"y={new_y}"))
        old_r, r = r, new_r
        old_x, x = x, new_x
        old_y, y = y, new_y
    return steps, old_r, old_x, old_y


def expected_flow(p, q, e, message):
    n = p * q
    phi_p = p - 1
    phi_q = q - 1
    phi = phi_p * phi_q
    steps = [
        make_step("RSA_SETUP", f"p={p}", f"q={q}", f"message={message}"),
        make_step("M", p, q, n),
        make_step("S", p, 1, phi_p),
        make_step("S", q, 1, phi_q),
        make_step("M", phi_p, phi_q, phi),
        make_step("GCD_RESULT", f"gcd({e},{phi})", 1),
    ]
    euclid_steps, g, x, _ = extended_trace(e, phi)
    assert g == 1
    steps.extend(euclid_steps)
    d = x % phi
    check_product = e * d
    check_residue = check_product % phi
    steps.extend([
        make_step("MOD_NORMALIZE", x, f"mod {phi}", d),
        make_step("MOD_INVERSE", f"{e} mod {phi}", d),
        make_step("M", e, d, check_product),
        make_step("MOD_REDUCE", check_product, f"mod {phi}", check_residue),
        make_step("CHECK", "e*d mod phi", check_residue),
        make_step("RSA_PUBLIC_KEY", f"n={n}", f"e={e}"),
        make_step("RSA_PRIVATE_KEY", f"d={d}"),
    ])
    ciphertext = pow(message, e, n)
    decrypted = pow(ciphertext, d, n)
    steps.extend([
        make_step("MOD_POWER", f"{message}^{e}", f"mod {n}", ciphertext),
        make_step("RSA_ENCRYPT", message, ciphertext),
        make_step("MOD_POWER", f"{ciphertext}^{d}", f"mod {n}", decrypted),
        make_step("RSA_DECRYPT", ciphertext, decrypted),
        make_step("CHECK", "decrypted message", decrypted),
    ])
    answer = (
        f"n = {n}; phi = {phi}; d = {d}; ciphertext = {ciphertext}; "
        f"decrypted = {decrypted}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestRSAGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RSAGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "rsa")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            p, q, e, message = parse_problem(result["problem"])
            expected_steps, answer = expected_flow(p, q, e, message)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_key_conditions_and_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            p, q, e, message = parse_problem(result["problem"])
            n = p * q
            phi = (p - 1) * (q - 1)
            self.assertTrue(is_prime(p))
            self.assertTrue(is_prime(q))
            self.assertEqual(gcd(e, phi), 1)
            self.assertEqual(gcd(message, n), 1)
            answer_match = re.fullmatch(
                r"n = (\d+); phi = (\d+); d = (\d+); ciphertext = (\d+); "
                r"decrypted = (\d+)",
                result["final_answer"],
            )
            self.assertIsNotNone(answer_match)
            n_out, phi_out, d, ciphertext, decrypted = map(
                int, answer_match.groups()
            )
            self.assertEqual((n_out, phi_out), (n, phi))
            self.assertEqual((e * d) % phi, 1)
            self.assertEqual(pow(message, e, n), ciphertext)
            self.assertEqual(pow(ciphertext, d, n), decrypted)
            self.assertEqual(decrypted, message)

            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "EUCLID_DIV":
                    dividend, divisor, quotient, remainder = map(
                        int, fields[1:]
                    )
                    self.assertEqual(dividend, quotient * divisor + remainder)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "MOD_REDUCE":
                    mod = int(fields[2].split()[1])
                    self.assertEqual(int(fields[1]) % mod, int(fields[3]),
                                     raw_step)
                elif fields[0] == "MOD_POWER":
                    base, exponent = map(int, fields[1].split("^"))
                    mod = int(fields[2].split()[1])
                    self.assertEqual(pow(base, exponent, mod),
                                     int(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
