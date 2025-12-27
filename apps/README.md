# 🤖 Aiogram Registration Bot

Ushbu Telegram bot foydalanuvchilarni ro'yxatga olish, ma'lumotlarni SQLite bazasiga saqlash va admin panel orqali xabar tarqatish (broadcast) imkoniyatlarini taqdim etadi.

## ✨ Xususiyatlari
* **FSM (Finite State Machine)**: Foydalanuvchi ma'lumotlarini bosqichma-bosqich yig'ish.
* **Ma'lumotlar Bazasi**: SQLite va Python `sqlite3` kutubxonasi yordamida foydalanuvchilarni boshqarish.
* **Xavfsizlik**: `.env` fayli yordamida maxfiy tokenlarni yashirish.
* **Admin Panel**: Faqat adminlar uchun maxsus buyruqlar va xabar tarqatish funksiyasi.
* **Validatsiya**: Telefon raqami va kiritilgan ma'lumotlarni tekshirish.

## 🛠 Texnologiyalar
* **Python 3.x**
* **Aiogram 3.x** (Asinxron kutubxona)
* **SQLite3** (Ma'lumotlar bazasi)
* **python-dotenv** (Muhit o'zgaruvchilari uchun)

## 📂 Loyiha Strukturasi
```text
day-2/
├── apps/               # Botning asosiy mantiqiy qismlari
│   ├── handlers.py     # Xabarlarni qayta ishlovchi funksiyalar
│   ├── database.py     # Baza bilan ishlash (CRUD)
│   └── keyboard.py     # Tugmalar (Reply/Inline)
├── .env                # Maxfiy tokenlar (GitHub'ga yuklanmaydi)
├── .gitignore          # Keraksiz fayllar ro'yxati
├── requirements.txt    # Kerakli kutubxonalar
└── run.py              # Botni ishga tushirish fayli

```

## 🚀 O'rnatish va Ishga tushirish

1. **Repozitoriyani yuklab oling:**
```bash
git clone [https://github.com/sarsenbaev-bayram/bot_for_umu_xf.git](https://github.com/sarsenbaev-bayram/bot_for_umu_xf.git)
cd bot_for_umu_xf

```


2. **Virtual muhitni yarating va faollashtiring:**
```bash
python -m venv venv
# Windows uchun:
venv\Scripts\activate

```


3. **Zarur kutubxonalarni o'rnating:**
```bash
pip install -r requirements.txt

```


4. **Environment o'zgaruvchilarini sozlang:**
`.env` faylini yarating va quyidagilarni yozing:
```env
BOT_TOKEN=Sizning_Bot_Tokeningiz
ADMIN_ID=Sizning_Telegram_IDingiz

```


5. **Botni ishga tushiring:**
```bash
python run.py

```



## 📝 Muallif

* **Bayram Sarsenbaev** - [https://www.google.com/search?q=https://github.com/sarsenbaev-bayram]

```

---

