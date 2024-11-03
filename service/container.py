from typing import Dict, Any
from database.database import init_db
from repositories.UserRepository import UserRepository
from repositories.WebsiteRepository import WebsiteRepository
from repositories.CredentialRepository import CredentialRepository
from controllers.UserController import UserController
from controllers.WebsiteController import WebsiteController
from controllers.CredentialController import CredentialController


class ContainerError(Exception):
    """Custom exception for container-related errors"""
    pass


class Container:
    _instances: Dict[str, Any] = {}
    _initialized = False

    @classmethod
    def initialize(cls):
        """Initialize the container if not already initialized"""
        if not cls._initialized:
            try:
                cls._instances['db_connection'] = init_db()
                cls._initialized = True
            except Exception as e:
                raise ContainerError(f"Failed to initialize container: {str(e)}")

    @classmethod
    def _get_instance(cls, key: str, creator_func):
        """Generic method to get or create an instance"""
        if not cls._initialized:
            cls.initialize()

        if key not in cls._instances:
            try:
                cls._instances[key] = creator_func()
            except Exception as e:
                raise ContainerError(f"Failed to create {key}: {str(e)}")
        return cls._instances[key]

    @classmethod
    def get_db_connection(cls):
        return cls._get_instance('db_connection', lambda: init_db())

    @classmethod
    def get_user_repository(cls):
        return cls._get_instance('user_repository',
                                 lambda: UserRepository(cls.get_db_connection()))

    @classmethod
    def get_website_repository(cls):
        return cls._get_instance('website_repository',
                                 lambda: WebsiteRepository(cls.get_db_connection()))

    @classmethod
    def get_credential_repository(cls):
        return cls._get_instance('credential_repository',
                                 lambda: CredentialRepository(cls.get_db_connection()))

    @classmethod
    def get_user_controller(cls):
        return cls._get_instance('user_controller',
                                 lambda: UserController(cls.get_user_repository()))

    @classmethod
    def get_website_controller(cls):
        return cls._get_instance('website_controller',
                                 lambda: WebsiteController(cls.get_website_repository()))

    @classmethod
    def get_credential_controller(cls):
        return cls._get_instance('credential_controller',
                                 lambda: CredentialController(
                                     cls.get_credential_repository(),
                                     cls.get_website_controller()
                                 ))

    @classmethod
    def reset(cls):
        """Reset the container - useful for testing"""
        cls._instances = {}
        cls._initialized = False