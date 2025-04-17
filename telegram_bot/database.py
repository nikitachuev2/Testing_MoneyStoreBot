
import sqlite3

DATABASE = 'database.db'

def create_connection():
    """Создает подключение к базе данных SQLite."""
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def create_tables():
    """Создает необходимые таблицы в базе данных."""
    conn = create_connection()
    if conn is None:
        return  # Завершаем выполнение, если не удалось подключиться к базе данных

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

    conn.commit()  # Сохраняем изменения
    conn.close()   # Закрываем соединение

if __name__ == '__main__':
    create_tables()  # Создание таблиц при запуске скрипта
