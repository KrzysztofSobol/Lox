# UserController.py
import hashlib

from repositories.UserRepository import UserRepository


class UserController:
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository

    def createUser(self, username: str, password: str, confirmPassword: str):
        existing_user = self.userRepository.getUserByUsername(username)
        if existing_user:
            return False
        elif len(password) >= 5 and (password == confirmPassword):
            return self.userRepository.createUser(username, password)
        else:
            return False

    def authenticateUser(self, username: str, password: str):
        user = self.userRepository.getUserByUsername(username)
        if user is None:
            return None
        else:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash == user.password_hash:
                return user
            return None