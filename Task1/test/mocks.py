import keyencryptor

class PasswordController(keyencryptor.PasswordController):

    def get(self):
        return "PASSWORD"