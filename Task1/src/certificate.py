from utils import *
from signature import Rsa
from cipher import Rabin
from algorithms import Algorithms
from random import Random

class Certificate(object):

    def __init__(self, 
            alg_id,
            public_key, 
            private_key, 
            serial_number, 
            ca_signature):

        self._alg_id = alg_id
        self._public_key = public_key
        self._private_key = private_key
        self._serial_number = serial_number
        self._ca_signature = ca_signature
        self._validation_engine = Rsa()

    def get_alg_id(self):
        return self._alg_id

    def get_public_key(self):
        return self._public_key

    def get_private_key(self):
        return self._private_key

    def get_serial_number(self):
        return self._serial_number

    def validate(self, ca_cert):
        try:
            coder = CertificateCoder()
            blob = coder.encode_cert_without_signature(self)
            self._validation_engine.verify(ca_cert, blob, self._ca_signature)
        except ValueError:
            raise ValueError("Certificate is not valid")

    def to_bytes(self):
        coder = CertificateCoder()

        return coder.encode(self)

class CertificateCoder(object):

    def encode(self, cert : Certificate) -> bytes:
        return self.encode_without_signature(cert.get_alg_id(),
        cert.get_serial_number(), cert.get_public_key(), 
        cert.get_private_key()) + cert._ca_signature

    def encode_without_signature(self, 
                            alg : Algorithms,
                            serial_number : int,
                            public_key: bytes,
                            private_key: bytes) -> bytes:

        res = int_to_bytes(alg.value)
        res += int_to_bytes(serial_number)
        res += self.__encode_key(public_key)
        res += self.__encode_key(private_key)

        return res

    def encode_cert_without_signature(self, cert: Certificate) -> bytes:
        res = int_to_bytes(cert.get_alg_id().value)
        res += int_to_bytes(cert.get_serial_number())
        res += self.__encode_key(cert.get_public_key())
        res += self.__encode_key(cert.get_private_key())

        return res
    
    """4 bytes for key length"""
    def __encode_key(self, key):
        key_len_bytes = byte_length(len(key))

        return int_to_bytes(len(key)) + b'\x00'*(4 - key_len_bytes) + key

    def decode(self, blob: bytes) -> Certificate:
        offset = 0
        alg_id = Algorithms(blob[offset])
        offset += 1

        """4 bytes for serial number"""
        serial_number = bytes_to_int(blob[offset:offset+4])
        offset += 4

        pub_key_len = bytes_to_int(blob[offset:offset+4])
        offset += 4

        public_key = blob[offset:offset+pub_key_len]
        offset += pub_key_len

        private_key_len = bytes_to_int(blob[offset:offset+4])
        offset += 4

        private_key = blob[offset:offset+private_key_len]
        offset += private_key_len

        signature = blob[offset:]

        return Certificate(alg_id, public_key, private_key, serial_number, signature)


class CertificateFactory(object):

    _cert_factory = None

    @staticmethod
    def get_instance():
        if CertificateFactory._cert_factory is None:
            CertificateFactory._cert_factory = CertificateFactory()

        return CertificateFactory._cert_factory

    def generate_certificate(self, blob : bytes) -> Certificate:
        coder = CertificateCoder()

        return coder.decode(blob)

    def generate_new_certificate(self, ca_cert: Certificate, security_param = 2048) -> Certificate:
        alg_id = Algorithms.RABIN
        public_key, private_key = Rabin.keygen(security_param)
        serial_number = Random().getrandbits(32)
        ca_signature = Rsa().sign(CertificateCoder().encode_without_signature(alg_id,
                        serial_number, public_key, private_key), ca_cert)

        return Certificate(alg_id, public_key, private_key, serial_number, ca_signature)

    def generate_new_ca_certificate(self, security_param = 2048) -> Certificate:
        alg_id = Algorithms.RSA
        public_key, private_key = Rsa.keygen(security_param)
        serial_number = Random().getrandbits(32)
        tmp_cert = Certificate(alg_id, public_key, private_key, serial_number, b'')
        ca_signature = Rsa().sign(CertificateCoder().encode_without_signature(alg_id,
                        serial_number, public_key, private_key), tmp_cert)

        return Certificate(alg_id, public_key, private_key, serial_number, ca_signature)