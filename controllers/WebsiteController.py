# WebsiteController.py
from repositories.UserRepository import UserRepository


class UserController:
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository

    def createWebsite(self, userId: int, url: str):
        return True

