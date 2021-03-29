class Certificate(object):

    def __init__(self, 
            alg_id,
            public_key, 
            private_key, 
            subject_name,
            serial_number, 
            ca_signature,
            ca_serial_number,
            private_key_decryptor):

        self._alg_id = alg_id
        self._public_key = public_key
        self._private_key = private_key
        self._subject_name = subject_name
        self._serial_number = serial_number
        self._ca_signature = ca_signature
        self._ca_serial_number = ca_serial_number
        self._private_key_decryptor = private_key_decryptor

    def get_alg_id(self):
        return self._alg_id

    def get_public_key(self):
        return self._public_key

    def get_private_key(self):
        return self._private_key

    def get_serial_number(self):
        return self._serial_number

    def get_ca_serial_number(self):
        return self._ca_serial_number

    def get_subject_name(self):
        return self._subject_name