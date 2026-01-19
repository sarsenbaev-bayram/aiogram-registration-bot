"""
Bot konfiguratsiyasi - barcha sozlamalar shu yerda
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Bot sozlamalari
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
PAYMENTS_PROVIDER_TOKEN = os.getenv("PAYMENT_TOKEN")

# Valyuta
CURRENCY = "UZS"
USD_RATE = 12800  # 1 USD = 12800 UZS

# Kurslar ma'lumotlari
COURSES = {
    "🇺🇸 Ingliz Tili": {
        "name": "Ingliz tili",
        "teacher": "Ziyada",
        "level": "Beginner",
        "price": 50,
        "duration": "3 oy",
        "start_date": "23-Dekabr",
        "schedule": "Haftasiga 3 kun (1/3/5) soat 14:00 dan 18:00 gacha"
    },
    "🇷🇺 Rus Tili": {
        "name": "Rus tili",
        "teacher": "Dilnoza",
        "price": 50,
        "duration": "3 oy",
        "start_date": "1-oktabr",
        "schedule": "Haftasiga 3 kun (2/4/6) soat 14:00 dan 18:00 gacha"
    },
    "🇹🇷 Turk Tili": {
        "name": "Turk tili",
        "teacher": "Aynura",
        "price": 50,
        "duration": "3 oy",
        "start_date": "1-oktabr",
        "schedule": "Haftasiga 3 kun (1/3/5) soat 14:00 dan 18:00 gacha"
    },
    "🇩🇪 Nemis Tili": {
        "name": "Nemis tili",
        "teacher": "Gu'lzira",
        "price": 50,
        "duration": "3 oy",
        "start_date": "1-oktabr",
        "schedule": "Haftasiga 3 kun (2/4/6) soat 14:00 dan 18:00 gacha"
    },
    "🔢 Matematika": {
        "name": "Matematika",
        "teacher": "Saida",
        "price": 15,
        "duration": "2 oy",
        "start_date": "1-oktabr",
        "schedule": "Haftasiga 2 kun (1/4) soat 16:00 dan 18:00 gacha"
    },
    "🧬 Biologiya": {
        "name": "Biologiya",
        "teacher": "Ziliyxa",
        "price": 15,
        "duration": "2 oy",
        "start_date": "1-oktabr",
        "schedule": "Haftasiga 2 kun (2/5) soat 16:00 dan 18:00 gacha"
    },
    "⚖️ Huquq": {
        "name": "Huquq",
        "teacher": "Jetes",
        "price": 15,
        "duration": "2 oy",
        "start_date": "1-oktabr",
        "schedule": "Haftasiga 2 kun (3/6) soat 16:00 dan 18:00 gacha"
    },
    "📚 Tarix": {
        "name": "Tarix",
        "teacher": "Jetes",
        "price": 10,
        "duration": "1 oy",
        "start_date": "1-oktabr",
        "schedule": "Haftasiga 2 kun (2/5) soat 16:00 dan 18:00 gacha"
    }
}

# Xabarlar
MESSAGES = {
    "welcome": "🎓 <b>Xush kelibsiz!</b>\n\nBu bot orqali siz bizning o'quv markazimiz kurslariga yozilishingiz mumkin.\n\nQuyidagi tugmalardan birini tanlang:",
    "registered": "✅ Siz allaqachon ro'yxatdan o'tgansiz!\n\nQuyidagi tugmalardan foydalaning:",
    "enter_name": "👤 Assalomu alaykum!\n\nRo'yxatdan o'tish uchun ismingizni kiriting:",
    "enter_surname": "👤 Familiyangizni kiriting:",
    "share_contact": "📱 Telefon raqamingizni ulashing:",
    "registration_complete": "✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!",
    "courses_menu": "📚 <b>Bizning kurslarimiz</b>\n\nO'zingizga kerakli kursni tanlang:",
    "help": "ℹ️ <b>Yordam</b>\n\n📚 Kurslar - Mavjud kurslarni ko'rish\n📍 Manzil - O'quv markazi manzili\n👤 Profil - Sizning ma'lumotlaringiz\n📞 Aloqa - Biz bilan bog'lanish\n\nSavollaringiz bo'lsa, admin bilan bog'laning.",
    "contact": "📞 <b>Biz bilan bog'lanish</b>\n\n📱 Telefon: +998 XX XXX XX XX\n📧 Email: info@example.com\n🌐 Website: example.com",
    "address": "📍 <b>Bizning manzilimiz</b>\n\n🗺 https://maps.app.goo.gl/hEN8Jci7PUbSDLu46"
}
