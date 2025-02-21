import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def derive_key(password: str, salt: bytes, iterations: int = 100000) -> bytes:
    # derive a 256-bit key from a given password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt(plaintext: str, key: bytes) -> str:
    # Encrypt the plain text using AES-GCM
    # Return a Base64 encoded string containing nonce, tag and ciphertext
    nonce = os.urandom(12)  # 12-byte nonce for GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    encrypted_data = nonce + encryptor.tag + ciphertext
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt(token: str, key: bytes) -> str:
    # Decrypts the Base64 encoded token using AES-GCM
    data = base64.b64decode(token)
    nonce = data[:12]
    tag = data[12:28]   # 16-byte tag
    ciphertext = data[28:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode('utf-8')
