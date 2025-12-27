

import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Yangi ustunlar bilan jadval yaratish
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registered_users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, full_name, username, phone=None):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Ma'lumotni saqlash yoki yangilash
    cursor.execute('''
        INSERT OR REPLACE INTO registered_users (user_id, full_name, username, phone) 
        VALUES (?, ?, ?, ?)
    ''', (user_id, full_name, username, phone))
    conn.commit()
    conn.close()

def is_registered(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Telefon raqami borligini tekshirish
    cursor.execute('SELECT 1 FROM registered_users WHERE user_id = ? AND phone IS NOT NULL', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_all_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, full_name, username, phone FROM registered_users')
    users = cursor.fetchall()
    conn.close()
    return users

# Bazani ishga tushirish
init_db()


