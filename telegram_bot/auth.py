import sqlite3
import bcrypt
from database import create_connection, create_tables

db= 'database.db'

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

