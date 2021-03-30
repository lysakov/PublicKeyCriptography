from Cryptodome.Util import number
from math import sqrt, log2, ceil
from decimal import Decimal

from utils import *
from keyencryptor import KeyEncryptor
from algorithms import Algorithms

class Rabin(object):

    _PADDING = bytes.fromhex("FF"*4)
    _LAST_BYTE = bytes.fromhex("FF")
    _SPLITTER = bytes.fromhex("FF"*4)

    def __init__(self):
        self._key_encryptor = KeyEncryptor.get_instance()
        self._key_coder = RabinKeyCoder()

    def encrypt(self, data, certificate):
        if certificate.get_alg_id() != Algorithms.RABIN:
            raise ValueError("Wrong cerificate algorithm id")

        n = self._key_coder.decode_public_key(certificate.get_public_key())
        block_size = byte_length(int(Decimal(n).sqrt()))
        ciphertexts = []

        for i in range(len(data)//block_size + 1):
            left_bound = i*block_size
            right_bound = (i + 1)*block_size if (i + 1)*block_size < len(data) else len(data)
            if left_bound == right_bound:
                continue

            enc_block = self.__encrypt_block(data[left_bound:right_bound], block_size, n)
            ciphertexts.append(int_to_bytes(enc_block))

        return Rabin._SPLITTER.join(ciphertexts)

    def __encrypt_block(self, data, block_size, n):
        padding_nulls = bytes.fromhex("00"*(byte_length(block_size)-byte_length(len(data))))
        data_len = int_to_bytes(len(data)) + padding_nulls

        m =  bytes_to_int(Rabin._PADDING + data_len +
            bytes.fromhex("00"*(block_size - len(data))) + data + Rabin._LAST_BYTE)

        return pow(m, 2, n)

    def decrypt(self, blob, certificate):
        if certificate.get_alg_id() != Algorithms.RABIN:
            raise ValueError("Wrong cerificate algorithm id")

        private_key = self._key_encryptor.decrypt(certificate.get_private_key())
        p, q = self._key_coder.decode_private_key(private_key)
        n = self._key_coder.decode_public_key(certificate.get_public_key())
        block_size = byte_length(int(Decimal(n).sqrt()))
        enc_data = blob.split(Rabin._SPLITTER)
        data = [self.__decrypt_block(blob, p, q, block_size, n) for blob in enc_data]

        return b''.join(data)

    def __decrypt_block(self, blob, p, q, block_size, n):
        c = bytes_to_int(blob)
        m_p = sqrt_mod(c, p)
        m_q = sqrt_mod(c, q)
        q_inv = number.inverse(q, p)
        p_inv = number.inverse(p, q)
        m = [(m_p*q*q_inv + m_q*p*p_inv)%n, (m_p*q*q_inv - m_q*p*p_inv)%n]
        m += [n - m[0], n - m[1]]

        for block in m:
            bytes_arr = int_to_bytes(block)
            if bytes_to_int(bytes_arr[:len(Rabin._PADDING)]) == bytes_to_int(Rabin._PADDING):
                data_len = bytes_arr[len(Rabin._PADDING):len(Rabin._PADDING) + byte_length(block_size)]
                data_len = bytes_to_int(data_len)

                return bytes_arr[-1 - data_len:-1]

        raise ValueError("Incorrect ciphertext format")

    @staticmethod
    def keygen(security_param = 2048):
        p = number.getPrime(security_param // 2)
        q = number.getPrime(security_param // 2)

        key_encryptor = KeyEncryptor.get_instance()
        key_coder = RabinKeyCoder()
        public_key = key_coder.encode_public_key(p*q)
        private_key = key_encryptor.encrypt(key_coder.encode_private_key(p, q))

        return public_key, private_key

class RabinKeyCoder(object):

    def encode_public_key(self, n):
        return int_to_bytes(Algorithms.RABIN.value) + int_to_bytes(n)

    def decode_public_key(self, blob):
        alg = blob[0]
        if Algorithms(alg) != Algorithms.RABIN:
            raise ValueError("Wrong key algorithm")

        return bytes_to_int(blob[1:])

    def encode_private_key(self, p, q):
        return int_to_bytes(Algorithms.RABIN.value) + int_to_bytes(p) + int_to_bytes(q)

    def decode_private_key(self, blob):
        alg = blob[0]
        if Algorithms(alg) != Algorithms.RABIN:
            raise ValueError("Wrong key algorithm")

        p = bytes_to_int(blob[1:][:len(blob[1:])//2])
        q = bytes_to_int(blob[1:][len(blob[1:])//2:])

        return p, q