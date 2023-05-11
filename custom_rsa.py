import random
from math import gcd


def generate_key_pair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e such that 1 < e < phi and gcd(e, phi) = 1
    e = random.randint(1, phi)
    while gcd(e, phi) != 1:
        e = random.randint(1, phi)

    # Calculate d such that (d * e) % phi = 1
    d = pow(e, -1, phi)

    return (e, n), (d, n)


def encrypt(message, public_key):
    e, n = public_key
    return pow(len(message), e, n)


def decrypt(ciphertext, private_key):
    d, n = private_key
    return pow(len(ciphertext), d, n)
