from typing import Dict, Any
from database.database import init_db
from repositories.UserRepository import UserRepository
from repositories.WebsiteRepository import WebsiteRepository
from repositories.CredentialRepository import CredentialRepository
from controllers.UserController import UserController
from controllers.WebsiteController import WebsiteController
from controllers.CredentialController import CredentialController

class Container:
    _instances: Dict[str, Any] = {}
    _initialized = False

    @classmethod
    def initialize(cls):
        if not cls._initialized:
                cls._instances['db_connection'] = init_db()
                cls._initialized = True

    @classmethod
    def getInstance(cls, key: str, creator_func):
        if not cls._initialized:
            cls.initialize()

        if key not in cls._instances:
                cls._instances[key] = creator_func()
        return cls._instances[key]

    @classmethod
    def getDbConnection(cls):
        return cls.getInstance('db_connection', lambda: init_db())

    @classmethod
    def getUserRepository(cls):
        return cls.getInstance('user_repository',
                               lambda: UserRepository(cls.getDbConnection()))

    @classmethod
    def getWebsiteRepository(cls):
        return cls.getInstance('website_repository',
                               lambda: WebsiteRepository(cls.getDbConnection()))

    @classmethod
    def getCredentialRepository(cls):
        return cls.getInstance('credential_repository',
                               lambda: CredentialRepository(cls.getDbConnection()))

    @classmethod
    def getUserController(cls):
        return cls.getInstance('user_controller',
                               lambda: UserController(cls.getUserRepository()))

    @classmethod
    def getWebsiteController(cls):
        return cls.getInstance('website_controller',
                               lambda: WebsiteController(cls.getWebsiteRepository()))

    @classmethod
    def getCredentialController(cls):
        return cls.getInstance('credential_controller',
                               lambda: CredentialController(
                                   cls.getCredentialRepository(),
                                   cls.getWebsiteController()))