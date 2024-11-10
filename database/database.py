import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            encryption_key TEXT NOT NULL
        )
    ''')

    # Websites table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, url)
        )
    ''')

    # Credentials table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY,
            website_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL,
            saved_link TEXT NOT NULL,
            FOREIGN KEY (website_id) REFERENCES websites (id)
        )
    ''')

    conn.commit()
    return conn