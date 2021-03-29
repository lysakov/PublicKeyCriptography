import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from signature import Rsa
from keyencryptor import KeyEncryptor
from certificate import Certificate
from algorithms import Algorithms
from cipher import Rabin
from utils import *

from Cryptodome.Util import number

import mocks

class Test(unittest.TestCase):

    def setUp(self):
        KeyEncryptor.init(mocks.PasswordController())
        with open("test/resources/long_message.txt", "r") as inp:
            self._message = string_to_bytes("".join(inp.readlines()))

    def test_rsa(self):
        rsa = Rsa()
        public_key, private_key = Rsa.keygen(512)
        cert = Certificate(Algorithms.RSA, public_key, private_key, 0, 0, 0, 0, 0)
        signature = rsa.sign(self._message, cert)
        rsa.verify(signature)

    def test_rabin(self):
        rabin = Rabin()
        public_key, private_key = Rabin.keygen(512)
        cert = Certificate(Algorithms.RABIN, public_key, private_key, 0, 0, 0, 0, 0)

        enc_data = rabin.encrypt(self._message, cert)
        dec_data = rabin.decrypt(enc_data, cert)
        self.assertEqual(self._message, dec_data)

    def test_residue(self):
        p = number.getPrime(64)
        a = generate_quadratic_residue(p)
        self.assertEqual(a, sqrt_mod(a, p)**2 % p)


if __name__ == "__main__":
    unittest.main()