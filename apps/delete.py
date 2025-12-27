import sqlite3

DB_PATH = r"C:\Users\Bayram\OneDrive\Documents\aiogram\asyncio\day-2\users.db"

def clear_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Barcha qatorlarni o'chirish
    cursor.execute("DELETE FROM registered_users")
    
    conn.commit()
    conn.close()
    print("Barcha foydalanuvchilar o'chirildi.")

# Ishga tushirish
clear_all_users()
