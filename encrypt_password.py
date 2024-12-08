from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

mail = input("Enter xour email: ")
password = input("Enter your password: ")

encrypted_password = cipher_suite.encrypt(password.encode())

with open("config.py", "w") as config_file:
    config_file.write(f"TILE_USERNAME = {repr(mail)}\n")
    config_file.write(f"TILE_PASSWORD_ENCRYPTED = {repr(encrypted_password)}\n")
    config_file.write(f"ENCRYPTION_KEY = {repr(key)}\n")

print(f"Encrypted password: {encrypted_password}")
print(f"Encryption key: {key}")
