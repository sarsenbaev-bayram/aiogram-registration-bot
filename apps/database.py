"""
Database - SQLite bilan ishlash (optimallashtirilgan)
"""
import sqlite3
import os
from datetime import datetime

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users.db')

def get_connection():
    """Connection olish - check_same_thread=False qo'shildi"""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    """Bazani yaratish"""
    with get_connection() as conn:
        # Foydalanuvchilar jadvali
        conn.execute('''
            CREATE TABLE IF NOT EXISTS registered_users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT,
                phone TEXT
            )
        ''')
        
        # Kursga yozilganlar jadvali
        conn.execute('''
            CREATE TABLE IF NOT EXISTS course_enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                full_name TEXT,
                phone TEXT,
                course_name TEXT,
                status TEXT DEFAULT 'pending',
                enrolled_at TEXT,
                approved_at TEXT,
                last_payment_reminder TEXT
            )
        ''')
        conn.commit()

def add_user(user_id, full_name, username, phone=None):
    """Foydalanuvchi qo'shish/yangilash"""
    with get_connection() as conn:
        conn.execute('''
            INSERT OR REPLACE INTO registered_users (user_id, full_name, username, phone) 
            VALUES (?, ?, ?, ?)
        ''', (user_id, full_name, username, phone))
        conn.commit()

def is_registered(user_id):
    """Foydalanuvchi ro'yxatdan o'tganmi"""
    with get_connection() as conn:
        cursor = conn.execute(
            'SELECT 1 FROM registered_users WHERE user_id = ? AND phone IS NOT NULL', 
            (user_id,)
        )
        return cursor.fetchone() is not None

def get_all_users():
    """Barcha foydalanuvchilarni olish"""
    with get_connection() as conn:
        cursor = conn.execute('SELECT user_id, full_name, username, phone FROM registered_users')
        return cursor.fetchall()

# ============ KURS ENROLLMENT ============
def enroll_to_course(user_id, full_name, phone, course_name):
    """Kursga yozilish"""
    with get_connection() as conn:
        conn.execute('''
            INSERT INTO course_enrollments (user_id, full_name, phone, course_name, status, enrolled_at)
            VALUES (?, ?, ?, ?, 'pending', ?)
        ''', (user_id, full_name, phone, course_name, datetime.now().strftime('%Y-%m-%d %H:%M')))
        conn.commit()

def get_pending_enrollments():
    """Kutayotgan arizalar"""
    with get_connection() as conn:
        cursor = conn.execute('''
            SELECT id, user_id, full_name, phone, course_name, enrolled_at 
            FROM course_enrollments WHERE status = 'pending'
        ''')
        return cursor.fetchall()

def get_approved_students():
    """Tasdiqlangan o'quvchilar"""
    with get_connection() as conn:
        cursor = conn.execute('''
            SELECT id, user_id, full_name, phone, course_name, approved_at 
            FROM course_enrollments WHERE status = 'approved'
        ''')
        return cursor.fetchall()

def approve_enrollment(enrollment_id):
    """Arizani tasdiqlash"""
    with get_connection() as conn:
        conn.execute('''
            UPDATE course_enrollments 
            SET status = 'approved', approved_at = ?
            WHERE id = ?
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M'), enrollment_id))
        conn.commit()

def reject_enrollment(enrollment_id):
    """Arizani rad etish"""
    with get_connection() as conn:
        conn.execute('DELETE FROM course_enrollments WHERE id = ?', (enrollment_id,))
        conn.commit()

def get_enrollment_by_id(enrollment_id):
    """Ariza olish"""
    with get_connection() as conn:
        cursor = conn.execute('''
            SELECT id, user_id, full_name, phone, course_name, status
            FROM course_enrollments WHERE id = ?
        ''', (enrollment_id,))
        return cursor.fetchone()

def update_payment_reminder(enrollment_id):
    """To'lov eslatmasi yuborildi"""
    with get_connection() as conn:
        conn.execute('''
            UPDATE course_enrollments 
            SET last_payment_reminder = ?
            WHERE id = ?
        ''', (datetime.now().strftime('%Y-%m-%d'), enrollment_id))
        conn.commit()


def get_user_courses(user_id):
    """Foydalanuvchining kurslari"""
    with get_connection() as conn:
        cursor = conn.execute('''
            SELECT id, course_name, status, enrolled_at, approved_at
            FROM course_enrollments WHERE user_id = ?
        ''', (user_id,))
        return cursor.fetchall()


def get_all_enrollments():
    """Barcha yozilishlar (admin uchun)"""
    with get_connection() as conn:
        cursor = conn.execute('''
            SELECT user_id, full_name, phone, course_name, status, enrolled_at, approved_at
            FROM course_enrollments
            ORDER BY enrolled_at DESC
        ''')
        return cursor.fetchall()


def get_course_statistics():
    """Kurslar bo'yicha statistika"""
    with get_connection() as conn:
        cursor = conn.execute('''
            SELECT course_name, COUNT(*) as count, status
            FROM course_enrollments
            GROUP BY course_name, status
        ''')
        return cursor.fetchall()


# Bazani ishga tushirish
init_db()



