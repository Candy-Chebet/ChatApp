from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def generate_secret_key(user_password, salt, iterations=100000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt,
        iterations=iterations,
    )
    secret_key = base64.urlsafe_b64encode(kdf.derive(user_password))
    return secret_key

def encrypt_message(secret_key, plaintext):
    cipher_suite = Fernet(secret_key)
    encrypted_text = cipher_suite.encrypt(plaintext.encode())
    return encrypted_text

def decrypt_message(secret_key, ciphertext):
    cipher_suite = Fernet(secret_key)
    decrypted_text = cipher_suite.decrypt(ciphertext).decode()
    return decrypted_text

# Usage example for key derivation and encryption
def encrypt_message_with_password(user_password, plaintext, salt):
    secret_key = generate_secret_key(user_password, salt)
    encrypted_message = encrypt_message(secret_key, plaintext)
    return encrypted_message

# Usage example for decryption
def decrypt_message_with_password(user_password, ciphertext, salt):
    secret_key = generate_secret_key(user_password, salt)
    decrypted_message = decrypt_message(secret_key, ciphertext)
    return decrypted_message
