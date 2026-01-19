"""
Bot klaviaturalari - Reply va Inline keyboard'lar
"""
from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# ============ BOSH MENYU ============
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📚 Kurslar'), KeyboardButton(text='📖 Mening kurslarim')],
        [KeyboardButton(text='📍 Manzil'), KeyboardButton(text='👤 Profil')],
        [KeyboardButton(text='📞 Aloqa'), KeyboardButton(text='ℹ️ Yordam')]
    ],
    resize_keyboard=True,
    input_field_placeholder="Menyudan tanlang..."
)


# ============ KURSLAR MENYUSI ============
courses_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🇺🇸 Ingliz Tili'), KeyboardButton(text='🇷🇺 Rus Tili')],
        [KeyboardButton(text='🇹🇷 Turk Tili'), KeyboardButton(text='🇩🇪 Nemis Tili')],
        [KeyboardButton(text='🔢 Matematika'), KeyboardButton(text='🧬 Biologiya')],
        [KeyboardButton(text='⚖️ Huquq'), KeyboardButton(text='📚 Tarix')],
        [KeyboardButton(text='🏠 Bosh menyu')]
    ],
    resize_keyboard=True,
    input_field_placeholder="Kursni tanlang..."
)


# ============ KURS TANLANGANDAN KEYIN ============
course_actions = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='💳 Kursga yozilish')],
        [KeyboardButton(text='⬅️ Orqaga'), KeyboardButton(text='🏠 Bosh menyu')]
    ],
    resize_keyboard=True
)


# ============ TELEFON ULASHISH ============
contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📱 Raqamni ulashish', request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


# ============ ORQAGA QAYTISH ============
back_to_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🏠 Bosh menyu')]
    ],
    resize_keyboard=True
)


# ============ ADMIN PANEL ============
admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='👥 Foydalanuvchilar'), KeyboardButton(text='📢 Xabar yuborish')],
        [KeyboardButton(text='📋 Yangi arizalar'), KeyboardButton(text='✅ Tasdiqlangan')],
        [KeyboardButton(text='💰 To\'lov eslatmasi'), KeyboardButton(text='📊 Statistika')],
        [KeyboardButton(text='🏠 Bosh menyu')]
    ],
    resize_keyboard=True
)


# ============ INLINE KEYBOARD'LAR ============

# Creator info - URL lar uchun
creator_info = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='📱 Telegram', url='https://t.me/sarsenbaevv_b')],
        [InlineKeyboardButton(text='📷 Instagram', url='https://www.instagram.com/_sarsenbaev.b')],
        [InlineKeyboardButton(text='💻 GitHub', url='https://github.com/Fulacios')],
    ]
)
# Tasdiqlash
confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='✅ Ha', callback_data='confirm_yes'),
            InlineKeyboardButton(text='❌ Yo\'q', callback_data='confirm_no')
        ]
    ]
)


# Eski nomlar uchun alias (orqaga moslik)
kurs = courses_menu
back_keyboard = course_actions



