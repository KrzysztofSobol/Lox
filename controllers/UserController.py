# UserController.py
from repositories.UserRepository import UserRepository


class UserController:
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository

    def create_user(self, username: str, password: str):
        if len(password) >= 8:
            existing_user = self.userRepository.get_user_by_username(username)
            if existing_user:
                return False
            else:
                return self.userRepository.create_user(username, password)