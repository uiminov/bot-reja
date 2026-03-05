import os
from datetime import datetime

# Получаем DATABASE_URL из переменных окружения (Railway)
DATABASE_URL = os.environ.get('DATABASE_URL')

# Если DATABASE_URL не задан, используем SQLite для локальной разработки
if DATABASE_URL:
    USE_POSTGRES = True
    import asyncpg
    print("--- ИСПОЛЬЗУЕТСЯ POSTGRESQL ---")
else:
    USE_POSTGRES = False
    import sqlite3
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "bot_stats.db")
    print(f"--- ИСПОЛЬЗУЕТСЯ SQLITE: {DB_PATH} ---")


async def get_db_connection():
    """Получает соединение с базой данных"""
    if USE_POSTGRES:
        return await asyncpg.connect(DATABASE_URL)
    else:
        return sqlite3.connect(DB_PATH)


def init_db():
    """Инициализация базы данных"""
    if USE_POSTGRES:
        # Для PostgreSQL таблица создаётся при первом подключении
        print("PostgreSQL: таблицы создадутся автоматически при первом запросе")
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.cursor().execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, date TEXT)')
        conn.commit()
        conn.close()


async def _init_postgres_table():
    """Создаёт таблицу в PostgreSQL если её нет"""
    if USE_POSTGRES:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                date TEXT
            )
        ''')
        await conn.close()


async def add_user_if_not_exists(user_id):
    if USE_POSTGRES:
        await _init_postgres_table()
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            # Проверяем существует ли пользователь
            row = await conn.fetchrow("SELECT user_id FROM users WHERE user_id = $1", user_id)
            if row is None:
                await conn.execute(
                    "INSERT INTO users (user_id, date) VALUES ($1, $2)",
                    user_id, datetime.now().isoformat()
                )
                return True
            return False
        finally:
            await conn.close()
    else:
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
    if USE_POSTGRES:
        await _init_postgres_table()
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            row = await conn.fetchrow("SELECT COUNT(*) FROM users")
            return row[0] + 223
        finally:
            await conn.close()
    else:
        conn = sqlite3.connect(DB_PATH)
        count = conn.cursor().execute("SELECT COUNT(*) FROM users").fetchone()[0]
        conn.close()
        return count + 223


async def get_all_users():
    if USE_POSTGRES:
        await _init_postgres_table()
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            rows = await conn.fetch("SELECT user_id FROM users")
            return [row['user_id'] for row in rows]
        finally:
            await conn.close()
    else:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        users = [row[0] for row in cursor.fetchall()]
        conn.close()
        return users
