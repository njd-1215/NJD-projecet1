import sqlite3
from datetime import datetime


class Database:
    """SQLite 数据库存储"""

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self._init_table()

    def _init_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site TEXT,
                title TEXT,
                url TEXT UNIQUE,
                date TEXT,
                pushed INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        self.conn.commit()

    def is_exists(self, url):
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM items WHERE url = ?", (url,))
        return cursor.fetchone() is not None

    def insert_item(self, item):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO items (site, title, url, date, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            item["site"], item["title"], item["url"],
            item["date"], datetime.now().isoformat()
        ))
        self.conn.commit()

    def mark_pushed(self, url):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE items SET pushed = 1 WHERE url = ?", (url,))
        self.conn.commit()

    def close(self):
        self.conn.close()
