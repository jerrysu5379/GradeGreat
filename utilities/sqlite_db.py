import sqlite3
from hashlib import sha256
from .database import Database

class SQLiteDB(Database):
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_user_table(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (username TEXT PRIMARY KEY, password TEXT)''')
        conn.commit()
        conn.close()

    def register_user(self, username, password):
        conn = self.connect()
        c = conn.cursor()
        hashed_password = sha256(password.encode()).hexdigest()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            return False
        conn.close()
        return True

    def authenticate_user(self, username, password):
        conn = self.connect()
        c = conn.cursor()
        hashed_password = sha256(password.encode()).hexdigest()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        result = c.fetchone()
        conn.close()
        return result