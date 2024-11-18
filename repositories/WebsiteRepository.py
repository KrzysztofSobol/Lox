import sqlite3
from datetime import datetime
from models.WebsiteModel import Website

class WebsiteRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cursor = connection.cursor()

    def get_user_website_by_id(self, user_id: int, website_id: int) -> Website:
        self.cursor.execute('''
            SELECT id, user_id, name 
            FROM websites 
            WHERE user_id = ? AND id = ?
        ''', (user_id, website_id))

        row = self.cursor.fetchone()
        if row:
            return Website(
                id=row[0],
                user_id=row[1],
                name=row[2]
            )
        return None

    def get_all_by_user_id(self, user_id: int) -> list[Website]:
        self.cursor.execute('''
            SELECT id, user_id, name, url 
            FROM websites 
            WHERE user_id = ?
        ''', (user_id,))

        websites = []
        for row in self.cursor.fetchall():
            website = Website(
                id=row[0],
                user_id=row[1],
                name=row[2],
                url=row[3],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            websites.append(website)

        return websites

    def create(self, website: Website) -> Website:
        self.cursor.execute('''
            INSERT INTO websites (user_id, name, url)
            VALUES (?, ?, ?)
        ''', (website.user_id, website.name, website.url))

        self.conn.commit()
        website.id = self.cursor.lastrowid
        return website

    def delete(self, website_id: int) -> bool:
        try:
            self.cursor.execute('''
                DELETE FROM credentials 
                WHERE website_id = ?
            ''', (website_id,))

            self.cursor.execute('''
                DELETE FROM websites 
                WHERE id = ?
            ''', (website_id,))

            self.conn.commit()
            return True
        except sqlite3.Error:
            self.conn.rollback()
            return False

    def __del__(self):
        self.conn.close()