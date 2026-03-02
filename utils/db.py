import sqlite3
from datetime import datetime

DB_PATH = "bot_stats.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.cursor().execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, date TEXT)')
    conn.commit()
    conn.close()

async def add_user_if_not_exists(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users VALUES (?, ?)", (user_id, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

async def get_users_count():
    conn = sqlite3.connect(DB_PATH)
    count = conn.cursor().execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    return count
