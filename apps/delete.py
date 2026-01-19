import sqlite3

DB_PATH = r"C:\Users\Bayram\OneDrive\Documents\aiogram\asyncio\day-2\users.db"

def show_menu():
    print("\n" + "="*50)
    print("📋 DATABASE BOSHQARUV PANELI")
    print("="*50)
    print("1. 👥 Barcha foydalanuvchilarni o'chirish")
    print("2. 📚 Barcha kurs yozilishlarini o'chirish")
    print("3. 🗑️ Hammasini o'chirish (users + enrollments)")
    print("4. 📊 Statistikani ko'rish")
    print("5. 📋 Kurs yozilishlarini ko'rish")
    print("6. ❌ Chiqish")
    print("="*50)

def clear_all_users():
    """Barcha foydalanuvchilarni o'chirish"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registered_users")
    conn.commit()
    count = cursor.rowcount
    conn.close()
    print(f"✅ {count} ta foydalanuvchi o'chirildi.")

def clear_all_enrollments():
    """Barcha kurs yozilishlarini o'chirish"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM course_enrollments")
    conn.commit()
    count = cursor.rowcount
    conn.close()
    print(f"✅ {count} ta kurs yozilishi o'chirildi.")

def clear_all():
    """Hammasini o'chirish"""
    clear_all_users()
    clear_all_enrollments()
    print("✅ Barcha ma'lumotlar o'chirildi!")

def show_stats():
    """Statistikani ko'rish"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Foydalanuvchilar
    cursor.execute("SELECT COUNT(*) FROM registered_users")
    users_count = cursor.fetchone()[0]
    
    # Kurs yozilishlari
    cursor.execute("SELECT COUNT(*) FROM course_enrollments")
    enrollments_count = cursor.fetchone()[0]
    
    # Kutayotgan
    cursor.execute("SELECT COUNT(*) FROM course_enrollments WHERE status = 'pending'")
    pending_count = cursor.fetchone()[0]
    
    # Tasdiqlangan
    cursor.execute("SELECT COUNT(*) FROM course_enrollments WHERE status = 'approved'")
    approved_count = cursor.fetchone()[0]
    
    conn.close()
    
    print("\n📊 STATISTIKA:")
    print(f"  👥 Foydalanuvchilar: {users_count}")
    print(f"  📚 Kurs yozilishlari: {enrollments_count}")
    print(f"     ⏳ Kutayotgan: {pending_count}")
    print(f"     ✅ Tasdiqlangan: {approved_count}")

def show_enrollments():
    """Kurs yozilishlarini ko'rish"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, user_id, full_name, phone, course_name, status, enrolled_at 
        FROM course_enrollments
        ORDER BY enrolled_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("\n❌ Hozircha kurs yozilishlari yo'q.")
        return
    
    print(f"\n📋 KURS YOZILISHLARI ({len(rows)} ta):")
    print("-"*70)
    for row in rows:
        id, user_id, full_name, phone, course, status, enrolled_at = row
        status_emoji = "✅" if status == "approved" else "⏳" if status == "pending" else "❌"
        print(f"  #{id} | {full_name} | {phone} | {course} | {status_emoji} {status}")
    print("-"*70)

def main():
    while True:
        show_menu()
        choice = input("\n👉 Tanlang (1-6): ").strip()
        
        if choice == "1":
            confirm = input("⚠️ Barcha foydalanuvchilarni o'chirishni tasdiqlaysizmi? (ha/yo'q): ")
            if confirm.lower() in ['ha', 'yes', 'y']:
                clear_all_users()
        elif choice == "2":
            confirm = input("⚠️ Barcha kurs yozilishlarini o'chirishni tasdiqlaysizmi? (ha/yo'q): ")
            if confirm.lower() in ['ha', 'yes', 'y']:
                clear_all_enrollments()
        elif choice == "3":
            confirm = input("⚠️ HAMMA MA'LUMOTLARNI o'chirishni tasdiqlaysizmi? (ha/yo'q): ")
            if confirm.lower() in ['ha', 'yes', 'y']:
                clear_all()
        elif choice == "4":
            show_stats()
        elif choice == "5":
            show_enrollments()
        elif choice == "6":
            print("👋 Dastur tugatildi!")
            break
        else:
            print("❌ Noto'g'ri tanlov. Qaytadan urinib ko'ring.")

# Ishga tushirish
if __name__ == "__main__":
    main()
