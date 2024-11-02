import sqlite3
from datetime import datetime
from models.WebsiteModel import Website


class WebsiteRepository:
    def __init__(self):
        self.conn = sqlite3.connect('password_manager.db')
        self.cursor = self.conn.cursor()

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
                created_at=datetime.now(),  # Since these aren't in DB yet
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

    def __del__(self):
        self.conn.close()