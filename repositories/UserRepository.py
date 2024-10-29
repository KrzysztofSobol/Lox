# UserRepository.py
import sqlite3
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet
from models.UserModel import User


class UserRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cursor = connection.cursor()

    def createUser(self, username: str, password: str) -> User:
        encryption_key = Fernet.generate_key()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        current_time = datetime.now()

        try:
            self.cursor.execute('''
                INSERT INTO users (username, password_hash, encryption_key)
                VALUES (?, ?, ?)
            ''', (username, password_hash, encryption_key.decode()))

            self.conn.commit()
            user_id = self.cursor.lastrowid

            return User(
                id=user_id,
                username=username,
                password_hash=password_hash,
                encryption_key=encryption_key,
                created_at=current_time,
                updated_at=current_time
            )
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")

    def getUserByUsername(self, username: str) -> User | None:
        self.cursor.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        )
        user_data = self.cursor.fetchone()

        if user_data:
            return User(
                id=user_data[0],
                username=user_data[1],
                password_hash=user_data[2],
                encryption_key=user_data[3].encode(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        return None