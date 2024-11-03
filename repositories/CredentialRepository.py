import sqlite3
from datetime import datetime
from typing import List
from models.CredentialModel import Credential

class CredentialRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cursor = connection.cursor()

    def create(self, credential: Credential) -> Credential:
        self.cursor.execute('''
            INSERT INTO credentials (website_id, username, encrypted_password)
            VALUES (?, ?, ?)
        ''', (credential.website_id, credential.username, credential.encrypted_password))

        self.conn.commit()
        credential.id = self.cursor.lastrowid
        return credential

    def get_all_by_website_id(self, website_id: int) -> List[Credential]:
        self.cursor.execute('''
            SELECT id, website_id, username, encrypted_password
            FROM credentials 
            WHERE website_id = ?
        ''', (website_id,))

        credentials = []
        for row in self.cursor.fetchall():
            credential = Credential(
                id=row[0],
                website_id=row[1],
                username=row[2],
                encrypted_password=row[3],
                notes=None,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            credentials.append(credential)

        return credentials

    def __del__(self):
        self.conn.close()