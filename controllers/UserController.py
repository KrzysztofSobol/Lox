import hashlib
from repositories.UserRepository import UserRepository

class UserController:
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository

    def createUser(self, username: str, password: str, confirmPassword: str):
        existing_user = self.userRepository.getUserByUsername(username)
        if existing_user:
            return 3
        elif len(password) >= 5:
            if (password == confirmPassword):
                return self.userRepository.createUser(username, password)
            else:
                return 4
        else:
            return 5

    def authenticateUser(self, username: str, password: str):
        user = self.userRepository.getUserByUsername(username)
        if user is None:
            return 1
        else:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash == user.password_hash:
                return user
            return 2