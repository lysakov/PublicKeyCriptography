import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from signature import Rsa
from keyencryptor import KeyEncryptor
from certificate import Certificate,CertificateFactory
from algorithms import Algorithms
from cipher import Rabin
from utils import *

from Cryptodome.Util import number

import mocks

class Test(unittest.TestCase):

    def setUp(self):
        KeyEncryptor.init(mocks.PasswordController())

        with open("test/resources/long_message.txt", "r") as inp:
            self.message = string_to_bytes("".join(inp.readlines()))

        cert_factory = CertificateFactory.get_instance()
        self.ca_cert = cert_factory.generate_new_ca_certificate(512)
        self.cert = cert_factory.generate_new_certificate(self.ca_cert, 512)

    def test_rsa(self):
        rsa = Rsa()
        signature = rsa.sign(self.message, self.ca_cert, self.ca_cert)
        rsa.verify(self.ca_cert, self.message, signature)

    def test_rabin(self):
        rabin = Rabin()
        enc_data = rabin.encrypt(self.message, self.cert)
        dec_data = rabin.decrypt(enc_data, self.cert)
        self.assertEqual(self.message, dec_data)

    def test_residue(self):
        p = number.getPrime(64)
        a = generate_quadratic_residue(p)
        self.assertEqual(a, sqrt_mod(a, p)**2 % p)

    def test_certificate_coder(self):
        cert = self.cert
        blob = cert.to_bytes()
        cert_factory = CertificateFactory.get_instance()
        cert_2 = cert_factory.generate_certificate(blob)

        self.assertEqual(cert.get_alg_id(), cert_2.get_alg_id())
        self.assertEqual(cert.get_serial_number(), cert.get_serial_number())
        self.assertEqual(cert.get_public_key(), cert_2.get_public_key())
        self.assertEqual(cert.get_private_key(), cert_2.get_private_key())

        cert_2.validate(self.ca_cert)

if __name__ == "__main__":
    unittest.main()