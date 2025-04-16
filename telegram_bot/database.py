import sqlite3

DATABASE = 'database.db'

def create_connection():
    """Создает подключение к базе данных SQLite."""
    conn = sqlite3.connect(DATABASE)
    return conn

def create_tables():
    """Создает необходимые таблицы в базе данных."""
    conn = create_connection()
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      email TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL)''')

    # Создание таблицы покупок
    cursor.execute('''CREATE TABLE IF NOT EXISTS purchases (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER NOT NULL,
                      category TEXT NOT NULL,
                      amount REAL NOT NULL,
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE)''')

    # Создание таблицы целей
    cursor.execute('''CREATE TABLE IF NOT EXISTS goals (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER NOT NULL,
                      target_amount REAL NOT NULL,
                      current_amount REAL DEFAULT 0,
                      dream_name TEXT NOT NULL,
                      FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE)''')

    # Создание таблицы взносов
    cursor.execute('''CREATE TABLE IF NOT EXISTS contributions (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER NOT NULL,
                      amount REAL NOT NULL,
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE)''')

    conn.commit()
    conn.close()

create_tables()
