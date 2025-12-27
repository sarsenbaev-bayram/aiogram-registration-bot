from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# main = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text = 'Amaliyotlar'), KeyboardButton(text = 'Dars jadvali')],
#     [KeyboardButton(text = 'Maruzalar'), KeyboardButton(text = 'Mustaqil ishlar')]
# ],

#                             resize_keyboard=True,
#                             input_field_placeholder="Quyidagilardan birini tanlang..."
# )


kurs = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text='🇺🇸 Ingliz Tili', callback_data='kurs_en')],
    [InlineKeyboardButton(text='🇷🇺 Rus Tili', callback_data='kurs_ru')],
    [InlineKeyboardButton(text='🇹🇷 Turk Tili', callback_data='kurs_tr')],
    [InlineKeyboardButton(text='🇩🇪 Nemis Tili', callback_data='kurs_de')],
    [InlineKeyboardButton(text='🔢 Matematika', callback_data='kurs_math')],
    [InlineKeyboardButton(text='🧬 Biologiya', callback_data='kurs_bio')],
    [InlineKeyboardButton(text='⚖️ Huquq', callback_data='kurs_law')],
    [InlineKeyboardButton(text='📚 Tarix', callback_data='kurs_history')]
])
   
creator_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Telegram', url='https://t.me/sarsenbaevv_b')],
    [InlineKeyboardButton(text = 'Instagram', url='https://www.instagram.com/_sarsenbaev.b')],
    [InlineKeyboardButton(text = 'GitHub', url='https://github.com/Fulacios')],
])



back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Orqaga qaytish", callback_data="back_to_courses")]
])

