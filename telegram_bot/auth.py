
import sqlite3
import bcrypt

DATABASE = 'users.db'

def create_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      email TEXT UNIQUE,
                      password TEXT)''')
    conn.commit()
    conn.close()

def register_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
    conn.commit()
    conn.close()

def authenticate_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()

    # Исправление здесь: убираем encode() и используем decode()
    if row and bcrypt.checkpw(password.encode('utf-8'), row[0]):  # row[0] - это bytes
        return True
    return False

# Инициализация базы данных
create_table()
