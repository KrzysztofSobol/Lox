# UserRepository.py
import sqlite3
from datetime import datetime
from models.UserModel import User

class UserRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cursor = connection.cursor()

    def createUser(self, user_data: dict) -> User:
        """
        Expects a dictionary with keys:
          - username
          - password_hash
          - salt
          - wrapped_encryption_key
        """
        current_time = datetime.now()
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password_hash, salt, wrapped_encryption_key, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_data['username'],
                user_data['password_hash'],
                user_data['salt'],
                user_data['wrapped_encryption_key'],
                current_time,
                current_time
            ))
            self.conn.commit()
            user_id = self.cursor.lastrowid
            return User(
                id=user_id,
                username=user_data['username'],
                password_hash=user_data['password_hash'],
                salt=user_data['salt'],
                wrapped_encryption_key=user_data['wrapped_encryption_key'],
                created_at=current_time,
                updated_at=current_time
            )
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")

    def getUserByUsername(self, username: str) -> User | None:
        self.cursor.execute('''
            SELECT id, username, password_hash, salt, wrapped_encryption_key, created_at, updated_at
            FROM users WHERE username = ?
        ''', (username,))
        user_data = self.cursor.fetchone()
        if user_data:
            return User(
                id=user_data[0],
                username=user_data[1],
                password_hash=user_data[2],
                salt=user_data[3],
                wrapped_encryption_key=user_data[4],
                created_at=user_data[5],
                updated_at=user_data[6]
            )
        return None
