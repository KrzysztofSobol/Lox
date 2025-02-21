import os
import base64
import hashlib
from repositories.UserRepository import UserRepository
from utils.CryptoUtils import derive_key, encrypt, decrypt

class UserController:
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository

    def createUser(self, username: str, password: str, confirmPassword: str):
        existing_user = self.userRepository.getUserByUsername(username)
        if existing_user:
            return 3  # User already exists
        elif len(password) < 5:
            return 5  # Password too short
        elif password != confirmPassword:
            return 4  # Passwords do not match

        salt = os.urandom(16)
        derived_key = derive_key(password, salt)
        encryption_key = os.urandom(32)
        wrapped_encryption_key = encrypt(base64.b64encode(encryption_key).decode('utf-8'), derived_key)
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        user_data = {
            'username': username,
            'password_hash': password_hash,
            'salt': base64.b64encode(salt).decode('utf-8'),
            'wrapped_encryption_key': wrapped_encryption_key
        }
        return self.userRepository.createUser(user_data)

    def authenticateUser(self, username: str, password: str):
        user = self.userRepository.getUserByUsername(username)
        if user is None:
            return 1  # User not found

        provided_hash = hashlib.sha256(password.encode()).hexdigest()
        if provided_hash != user.password_hash:
            return 2  # Incorrect password

        salt = base64.b64decode(user.salt)
        derived_key = derive_key(password, salt)
        try:
            decrypted_key_b64 = decrypt(user.wrapped_encryption_key, derived_key)
            encryption_key = base64.b64decode(decrypted_key_b64)
        except Exception:
            return 2  # Failed to decrypt

        user.encryption_key = encryption_key

        # set the encryption key
        from utils.DependencyInjector import Injector
        credential_controller = Injector.getCredentialController()
        credential_controller.set_encryption_key(encryption_key)

        return user
