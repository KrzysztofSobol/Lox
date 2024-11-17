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
            INSERT INTO credentials (website_id, username, password, saved_link)
            VALUES (?, ?, ?, ?)
        ''', (credential.website_id, credential.username, credential.password, credential.saved_link))

        self.conn.commit()
        credential.id = self.cursor.lastrowid
        return credential

    def get_by_id(self, credential_id: int) -> Credential:
        self.cursor.execute('''
            SELECT id, website_id, username, password, saved_link
            FROM credentials
            WHERE id = ?
        ''', (credential_id,))

        row = self.cursor.fetchone()
        if row:
            return Credential(
                id=row[0],
                website_id=row[1],
                username=row[2],
                password=row[3],
                saved_link=row[4],
                notes=None,
                created_at=datetime.now(),  # Replace with actual timestamps if available in DB
                updated_at=datetime.now()  # Replace with actual timestamps if available in DB
            )
        return None

    def get_all_by_website_id(self, website_id: int) -> List[Credential]:
        self.cursor.execute('''
            SELECT id, website_id, username, password, saved_link
            FROM credentials 
            WHERE website_id = ?
        ''', (website_id,))

        credentials = []
        for row in self.cursor.fetchall():
            credential = Credential(
                id=row[0],
                website_id=row[1],
                username=row[2],
                password=row[3],
                saved_link=row[4],
                notes=None,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            credentials.append(credential)

        return credentials

    def edit(self, credential_id: int, updates: dict) -> Credential:
        if not updates:
            return self.get_by_id(credential_id)

        set_clauses = []
        values = []

        for field, value in updates.items():
            set_clauses.append(f"{field} = ?")
            values.append(value)
        values.append(credential_id)

        query = f"""
            UPDATE credentials 
            SET {', '.join(set_clauses)}
            WHERE id = ?
        """
        self.cursor.execute(query, values)
        self.conn.commit()

        return self.get_by_id(credential_id)

    def delete(self, credential_id: int) -> bool:
        try:
            self.cursor.execute('''
                DELETE FROM credentials 
                WHERE id = ?
            ''', (credential_id,))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def __del__(self):
        self.conn.close()