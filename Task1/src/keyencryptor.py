import sys

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util import number

from utils import *

class PasswordController(object):

    def get(self):
        pass

    def get_new_password(self):
        pass

class KeyEncryptor(object):

    _PADDING = bytes.fromhex("0000")
    _key_encryptor = None
    _iv = ("0" * AES.block_size).encode("utf-16")

    def __init__(self, password_interactor : PasswordController):
        self._password_interactor = password_interactor

    @staticmethod
    def init(password_interactor: PasswordController):
        KeyEncryptor._key_encryptor = KeyEncryptor(password_interactor)

    @staticmethod
    def get_instance():
        return KeyEncryptor._key_encryptor

    def encrypt(self, key : bytes):
        password_hash = compute_hash(string_to_bytes(self._password_interactor.get_new_password()))
        cipher = AES.new(password_hash, AES.MODE_EAX, KeyEncryptor._iv)
        enc_key = cipher.encrypt(KeyEncryptor._PADDING + key)

        return enc_key

    def decrypt(self, blob : bytes):
        password_hash = compute_hash(string_to_bytes(self._password_interactor.get()))
        cipher = AES.new(password_hash, AES.MODE_EAX, KeyEncryptor._iv)
        dec_blob = cipher.decrypt(blob)
        if bytes_to_int(dec_blob[:2]) != bytes_to_int(KeyEncryptor._PADDING):
            raise ValueError("Invalid password")

        return dec_blob[2:]