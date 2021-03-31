import keyencryptor

class PasswordController(keyencryptor.PasswordController):

    def get(self):
        return "PASSWORD"

    def get_new_password(self):
        return "PASSWORD"