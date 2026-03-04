import os
import sqlite3  # ОБЯЗАТЕЛЬНО ДОБАВИЛ
from datetime import datetime

# 1. Находим путь к папке utils и поднимаемся на уровень выше в корень проекта
# Это гарантирует, что база всегда будет в одном и том же файле в корне бота
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "bot_stats.db")

# Теперь эта строка покажет РЕАЛЬНЫЙ путь к файлу при запуске
print(f"--- БАЗА ДАННЫХ ИСПОЛЬЗУЕТСЯ ТУТ: {DB_PATH} ---")

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

async def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users
