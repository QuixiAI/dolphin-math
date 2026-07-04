import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


PRIMES = [5, 7, 11, 13, 17, 19, 23, 29]
EXPONENTS = [3, 5, 7, 11, 13, 17, 19]


def extended_trace(a, b):
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    steps = [
        step("EXT_GCD_SETUP", a, b),
        step("BACK_SUB_ROW", f"r={old_r}", f"x={old_x}", f"y={old_y}"),
        step("BACK_SUB_ROW", f"r={r}", f"x={x}", f"y={y}"),
    ]
    while r != 0:
        q = old_r // r
        product = q * r
        new_r = old_r - product
        steps.append(step("EUCLID_DIV", old_r, r, q, new_r))
        steps.append(step("M", q, r, product))
        steps.append(step("S", old_r, product, new_r))

        qx = q * x
        new_x = old_x - qx
        steps.append(step("M", q, x, qx))
        steps.append(step("S", old_x, qx, new_x))

        qy = q * y
        new_y = old_y - qy
        steps.append(step("M", q, y, qy))
        steps.append(step("S", old_y, qy, new_y))
        steps.append(step("BACK_SUB_ROW", f"r={new_r}",
                          f"x={new_x}", f"y={new_y}"))
        old_r, r = r, new_r
        old_x, x = x, new_x
        old_y, y = y, new_y
    return steps, old_r, old_x, old_y


class RSAGenerator(ProblemGenerator):
    """
    RSA key generation, encryption, and decryption with small primes.

    Op-codes used:
    - RSA_SETUP / RSA_PUBLIC_KEY / RSA_PRIVATE_KEY: key context
    - EXT_GCD_SETUP / EUCLID_DIV / BACK_SUB_ROW: inverse trace for d
    - MOD_NORMALIZE / MOD_INVERSE / MOD_POWER: modular arithmetic
    - RSA_ENCRYPT / RSA_DECRYPT / CHECK: end-to-end message verification
    - M / S / GCD_RESULT (established/shared): arithmetic
    - Z: key values, ciphertext, and decrypted message
    """

    def generate(self) -> dict:
        p, q = sorted(random.sample(PRIMES, 2))
        n = p * q
        phi_p = p - 1
        phi_q = q - 1
        phi = phi_p * phi_q
        possible_e = [e for e in EXPONENTS if e < phi and gcd(e, phi) == 1]
        e = random.choice(possible_e)
        while True:
            message = random.randint(2, n - 2)
            if gcd(message, n) == 1:
                break

        steps = [
            step("RSA_SETUP", f"p={p}", f"q={q}", f"message={message}"),
            step("M", p, q, n),
            step("S", p, 1, phi_p),
            step("S", q, 1, phi_q),
            step("M", phi_p, phi_q, phi),
            step("GCD_RESULT", f"gcd({e},{phi})", 1),
        ]
        euclid_steps, g, x, _ = extended_trace(e, phi)
        steps.extend(euclid_steps)
        d = x % phi
        check_product = e * d
        check_residue = check_product % phi
        steps.extend([
            step("MOD_NORMALIZE", x, f"mod {phi}", d),
            step("MOD_INVERSE", f"{e} mod {phi}", d),
            step("M", e, d, check_product),
            step("MOD_REDUCE", check_product, f"mod {phi}", check_residue),
            step("CHECK", "e*d mod phi", check_residue),
            step("RSA_PUBLIC_KEY", f"n={n}", f"e={e}"),
            step("RSA_PRIVATE_KEY", f"d={d}"),
        ])

        ciphertext = pow(message, e, n)
        decrypted = pow(ciphertext, d, n)
        steps.extend([
            step("MOD_POWER", f"{message}^{e}", f"mod {n}", ciphertext),
            step("RSA_ENCRYPT", message, ciphertext),
            step("MOD_POWER", f"{ciphertext}^{d}", f"mod {n}", decrypted),
            step("RSA_DECRYPT", ciphertext, decrypted),
            step("CHECK", "decrypted message", decrypted),
        ])
        answer = (
            f"n = {n}; phi = {phi}; d = {d}; ciphertext = {ciphertext}; "
            f"decrypted = {decrypted}"
        )
        problem = (
            f"For RSA primes p={p} and q={q} with public exponent e={e} "
            f"and message m={message}, compute n, phi(n), d, encrypt, "
            f"and decrypt."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="rsa",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
