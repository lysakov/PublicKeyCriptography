from interactors import *
from certificate import CertificateFactory
from controllers import PasswordController
from keyencryptor import KeyEncryptor

if __name__ == "__main__":
    password_controller = PasswordController()
    KeyEncryptor.init(password_controller)

    cert_factory = CertificateFactory.get_instance()
    cert_builder = CertBuilder(cert_factory)
    encryptor = Encryptor(cert_factory)
    interactor = Interactor(cert_builder, encryptor)
    rsa_security_param = 2048
    rabin_security_param = 2048
    n = None

    while n != "q":
        print(50*"*")
        print("1. Generate new self-signed program's key pair.")
        print("2. Register new user.")
        print("3. Encrypt message.")
        print("4. Decrypt message.")
        print("   Print q to exit.")
        print(50*"*")
        n = input()

        if n == "1":
            print("Warning: After creating new key pair all previous generated keys will be invalid.")
            print("Continue? (y/n)")
            ans = input()
            if ans != "y":
                continue
            print("You will be asked to enter key pair's password to create new one if it exists.")
            interactor.generate_ca(rsa_security_param)
            print("New programm's key pair was generated.")

        elif n == "2":
            print("Enter key pair name:")
            name = input()
            print("You will be asked to create new key pair's password and enter program's key pair's password,",
                "in order to sign it.")
            interactor.generate_cert(name, rabin_security_param)
            print(f"New key pair may be found in cert_store/{name}")

        elif n == "3":
            print("Enter file to encrypt path:")
            file_path = input()
            print("Enter key pair name:")
            cert_name = input()
            cert_name = "cert_store/" + cert_name
            output_path = f"output/{file_path.split('/')[-1]}.enc"
            interactor.encrypt(file_path, cert_name, output_path)
            print(f"Encrypted file written in {output_path}")

        elif n == "4":
            print("Enter file to decrypt path:")
            file_path = input()
            print("Enter key pair name:")
            cert_name = input()
            cert_name = "cert_store/" + cert_name
            output_path = f"output/{file_path.split('/')[-1]}.dec"
            interactor.decrypt(file_path, cert_name, output_path)
            print(f"Encrypted file written in {output_path}")
