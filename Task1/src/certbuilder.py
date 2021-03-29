from certificate import Certificate

class CertificateBuilder(object):

    def __init__(self, ca_cert, signature, decryptor):
        self._ca_cert = ca_cert
        self._signature = signature
        self._decryptor = decryptor

    def build(self, subject_name):
        pass