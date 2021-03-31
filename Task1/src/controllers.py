import keyencryptor

class PasswordController(keyencryptor.PasswordController):

    def get(self):
        print("Enter password:")
        password = input()

        return password

    def get_new_password(self):
        print("Create new password:")
        password = input()

        return password