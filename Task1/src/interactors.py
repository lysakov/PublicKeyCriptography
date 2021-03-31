import base64
from cipher import Rabin
from signature import Rsa

from pathlib import Path

class CertBuilder(object):

    _CA_PATH = "cert_store/ca"

    def __init__(self, cert_factory):
        self._cert_factory = cert_factory

    def create_ca_cert(self, security_param):
        ca_file = Path(CertBuilder._CA_PATH)

        if ca_file.is_file():
            with open(CertBuilder._CA_PATH, "rb") as ca:
                ca_cert = self._cert_factory.generate_certificate(base64.b32decode(ca.read()))
                rsa = Rsa()
                rsa.sign(b'0x12', ca_cert, ca_cert)

        with open(CertBuilder._CA_PATH, "wb") as ca:
            ca_cert = self._cert_factory.generate_new_ca_certificate(security_param)
            ca.write(base64.b32encode(ca_cert.to_bytes()))

    def create_cert(self, name, security_param):
        with open(f"cert_store/{name}", "wb") as ca, open(CertBuilder._CA_PATH, "rb") as ca_input:
            ca_cert = self._cert_factory.generate_certificate(base64.b32decode(ca_input.read()))
            cert = self._cert_factory.generate_new_certificate(ca_cert, security_param)
            ca.write(base64.b32encode(cert.to_bytes()))

class Encryptor(object):

    _CA_PATH = "cert_store/ca"

    def __init__(self, cert_factory):
        self._cert_factory = cert_factory
        self._cipher = Rabin()

    def encrypt(self, file_path : str, cert_path: str, output_path : str):
        ca = None
        with open(CertBuilder._CA_PATH, "rb") as ca:
            ca = self._cert_factory.generate_certificate(base64.b32decode(ca.read()))
            
        with open(file_path, "rb") as data_inp, open(output_path, "wb") as outp, open(cert_path, "rb") as cert_inp:
            plaintext = data_inp.read()
            cert = self._cert_factory.generate_certificate(base64.b32decode(cert_inp.read()))
            outp.write(base64.b32encode(self._cipher.encrypt(plaintext, cert)))

    def decrypt(self, file_path : str, cert_path: str, output_path : str):
        ca = None
        with open(CertBuilder._CA_PATH, "rb") as ca:
            ca = self._cert_factory.generate_certificate(base64.b32decode(ca.read()))
            
        with open(file_path, "rb") as data_inp, open(output_path, "wb") as outp, open(cert_path, "rb") as cert_inp:
            ciphertext = base64.b32decode(data_inp.read())
            cert = self._cert_factory.generate_certificate(base64.b32decode(cert_inp.read()))
            cert.validate(ca)
            outp.write(self._cipher.decrypt(ciphertext, cert))

class Interactor(object):

    def __init__(self, cert_bulder : CertBuilder, encryptor: Encryptor):
        self._cert_builder = cert_bulder
        self._encryptor = encryptor

    def generate_ca(self, security_param):
        self._cert_builder.create_ca_cert(security_param)

    def generate_cert(self, name, security_param):
        self._cert_builder.create_cert(name, security_param)

    def encrypt(self, file_path, cert_path, output_path):
        self._encryptor.encrypt(file_path, cert_path, output_path)

    def decrypt(self, file_path, cert_path, output_path):
        self._encryptor.decrypt(file_path, cert_path, output_path)