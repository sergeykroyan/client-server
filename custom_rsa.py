import random


class RSAEncryptor:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (self.p - 1) * (self.q - 1)

    def gcd(self, a, b):
        if b == 0:
            return a
        return self.gcd(b, a % b)

    def is_prime(self, n):
        if self.n < 2:
            return False
        for i in range(2, int(self.n ** 0.5) + 1):
            if self.n % i == 0:
                return False
        return True

    def generate_key_pair(self):
        e = random.randint(1, self.phi - 1)
        while self.gcd(e, self.phi) != 1:
            e = random.randint(1, self.phi - 1)
        d = pow(e, -1, self.phi)
        return (self.n, e), (self.n, d)

    @staticmethod
    def encrypt(message, public_key):
        n, e = public_key
        ciphertext = [chr(pow(ord(char), e, n)) for char in message]
        return ''.join(ciphertext)

    @staticmethod
    def decrypt(ciphertext, private_key):
        n, d = private_key
        plaintext = [chr(pow(ord(char), d, n)) for char in ciphertext]
        return ''.join(plaintext)
