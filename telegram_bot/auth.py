
import sqlite3
import bcrypt
from database import create_connection, create_tables

db = 'database.db'

def register_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    
    # Проверка, существует ли уже пользователь с таким email
    cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
    if cursor.fetchone() is not None:
        conn.close()
        raise ValueError("Пользователь с таким email уже существует.")

    # Хеширование пароля
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Вставка нового пользователя в базу данных
    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
    conn.commit()
    conn.close()

def authenticate_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()

    # Проверка существования пользователя и воздуха пароля
    if row is not None and bcrypt.checkpw(password.encode('utf-8'), row[0]):
        conn.close()
        return True  # Успешная аутентификация

    conn.close()
    return False  # Неудачная аутентификация
