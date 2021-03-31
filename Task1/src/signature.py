from Cryptodome.Util import number

from random import randint
from algorithms import Algorithms
from keyencryptor import KeyEncryptor
from utils import *

class Rsa(object):

    def __init__(self):
        self._key_encryptor = KeyEncryptor.get_instance()
        self._key_coder = RsaKeyCoder()

    def sign(self, data, certificate, ca_cert=None):
        if certificate.get_alg_id() != Algorithms.RSA:
            raise ValueError("Impossible to sign with this public key")

        if ca_cert is not None:
            certificate.validate(ca_cert)

        d, n = self._key_coder.decode_private_key(self._key_encryptor.decrypt(certificate.get_private_key()))
        m = bytes_to_int(compute_hash(data))%n
        signature = int_to_bytes(pow(m, d, n))

        return signature


    def verify(self, certificate, data, signature):
        e, n = self._key_coder.decode_public_key(certificate.get_public_key())
        m = bytes_to_int(compute_hash(data))%n
        if m != pow(bytes_to_int(signature), e, n):
            raise ValueError("Failed to verify signature")

    @staticmethod
    def keygen(security_param = 2048):
        p = number.getPrime(security_param // 2)
        q = number.getPrime(security_param // 2)
        n = p*q

        phi = (p - 1)*(q - 1)
        e = randint(0, phi)
        while number.GCD(e, phi) != 1:
            e = randint(0, phi)

        key_coder = RsaKeyCoder()
        public_key = key_coder.encode_public_key(e, n)

        key_encryptor = KeyEncryptor.get_instance()
        d = number.inverse(e, phi)
        private_key = key_encryptor.encrypt(key_coder.encode_private_key(d, n))

        return public_key, private_key

class RsaKeyCoder(object):

    def encode_public_key(self, e, n):
        e_len = int_to_bytes(byte_length(e)) + (b'\x00' if byte_length(byte_length(e)) < 2 else b'')
        n_len = int_to_bytes(byte_length(n)) + (b'\x00' if byte_length(byte_length(n)) < 2 else b'')

        return int_to_bytes(Algorithms.RSA.value) + e_len + n_len + int_to_bytes(e) + int_to_bytes(n)

    def decode_public_key(self, blob):
        alg = blob[0]
        if Algorithms(alg) != Algorithms.RSA:
            raise ValueError("Wrong key algorithm")

        e_len = bytes_to_int(blob[1:3] if blob[2] != 0 else blob[1:2])
        n_len = bytes_to_int(blob[3:5] if blob[4] != 0 else blob[3:4])

        return bytes_to_int(blob[5:5+e_len]), bytes_to_int(blob[-n_len:])

    def encode_private_key(self, d, n):
        d_len = int_to_bytes(byte_length(d)) + (b'\x00' if byte_length(byte_length(d)) < 2 else b'')
        n_len = int_to_bytes(byte_length(n)) + (b'\x00' if byte_length(byte_length(n)) < 2 else b'')

        return int_to_bytes(Algorithms.RSA.value) + d_len + n_len + int_to_bytes(d) + int_to_bytes(n)

    def decode_private_key(self, blob):
        alg = blob[0]
        if Algorithms(alg) != Algorithms.RSA:
            raise ValueError("Wrong key algorithm")

        d_len = bytes_to_int(blob[1:3] if blob[2] != 0 else blob[1:2])
        n_len = bytes_to_int(blob[3:5] if blob[4] != 0 else blob[3:4])

        return bytes_to_int(blob[5:5+d_len]), bytes_to_int(blob[-n_len:])