"""
Bot handlerlari - Clean Architecture
"""
from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import logging
import os
from dotenv import load_dotenv

from apps.database import is_registered, add_user, get_all_users
from apps.keyboard import (
    main_menu, courses_menu, course_actions, contact_keyboard,
    back_to_main, admin_menu, creator_info
)

load_dotenv()

ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
PAYMENTS_PROVIDER_TOKEN = os.getenv("PAYMENT_TOKEN")
USD_RATE = 12800

router = Router()


# ============ HOLATLAR ============
class RegistrationForm(StatesGroup):
    name = State()
    surname = State()
    contact = State()


class AdminStates(StatesGroup):
    broadcast = State()


# ============ KURSLAR ============
COURSES = {
    "🇺🇸 Ingliz Tili": {"name": "Ingliz tili", "teacher": "Ziyada", "price": 50, "duration": "3 oy", "schedule": "1/3/5, 14:00-18:00"},
    "🇷🇺 Rus Tili": {"name": "Rus tili", "teacher": "Dilnoza", "price": 50, "duration": "3 oy", "schedule": "2/4/6, 14:00-18:00"},
    "🇹🇷 Turk Tili": {"name": "Turk tili", "teacher": "Aynura", "price": 50, "duration": "3 oy", "schedule": "1/3/5, 14:00-18:00"},
    "🇩🇪 Nemis Tili": {"name": "Nemis tili", "teacher": "Gu'lzira", "price": 50, "duration": "3 oy", "schedule": "2/4/6, 14:00-18:00"},
    "🔢 Matematika": {"name": "Matematika", "teacher": "Saida", "price": 15, "duration": "2 oy", "schedule": "1/4, 16:00-18:00"},
    "🧬 Biologiya": {"name": "Biologiya", "teacher": "Ziliyxa", "price": 15, "duration": "2 oy", "schedule": "2/5, 16:00-18:00"},
    "⚖️ Huquq": {"name": "Huquq", "teacher": "Jetes", "price": 15, "duration": "2 oy", "schedule": "3/6, 16:00-18:00"},
    "📚 Tarix": {"name": "Tarix", "teacher": "Jetes", "price": 10, "duration": "1 oy", "schedule": "2/5, 16:00-18:00"},
}

selected_course = {}

@router.message(Command('start'))
async def register_user(message: Message, state: FSMContext):
    user_id = message.from_user.id
    tg_name = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"

    # Bazaga "sokin" saqlash (telefon hali yo'q)
    add_user(user_id, tg_name, username)

    if is_registered(user_id):
        await message.answer("Siz allaqachon ro‘yxatdan o‘tgansiz! Kurslar: /kurs")
        return
    
    await message.answer(f"Assalawma aleykum! Ismingizni kiriting:")
    await state.set_state(Form.name)



@router.message(Command('manzil'))
async def get_address(message: Message):
    await message.answer("https://maps.app.goo.gl/hEN8Jci7PUbSDLu46")


@router.message(Command('kurs'))
async def info_kurs(message: Message):
    await message.answer("Bu yerda kurslar haqida ma'lumot beriladi.", reply_markup=kurs)

# Ingliz tili
@router.message(F.text == '🇺🇸 Ingliz Tili')
async def info_english(message: Message):
    await message.answer(
        "Ajoyib! Siz tog'ri tanlov qildingiz\n"
        "🇺🇸 Ingliz tili hozirda eng kerakli til hisoblanadi.\n"
        "Fan ustozi: Ziyada\n"
        "kurs darajasi: Beginner\n"
        "Kurs narxi: 50$\n"
        "Davomiyligi: 3 oy\n"
        "Boshlanish sanasi: 23-Dekabr\n"
        "Haftasiga 3 kun bo'ladi (1/3/5) soat 14:00 dan 18:00 gacha.\n"
        "Agarda kursimizni sotib olmoqchi bo'lsangiz /buy buyrug'ini bosing.\n",
        reply_markup=back_keyboard,
        parse_mode=ParseMode.HTML
    )

# 1. Rus tili
@router.message(F.text == '🇷🇺 Rus Tili')
async def info_russian(message: Message):
    await message.answer(
        "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>🇷🇺 Rus tili</b> hozirda eng kerakli til hisoblanadi.\nFan ustozi: Dilnoza\nKurs narxi: 50$\nDavomiyligi: 3 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 3 kun (2/4/6) soat 14:00 dan 18:00 gacha.\nAgarda kursimizni sotib olmoqchi bo'lsangiz /buy buyrug'ini bosing.\n",
        reply_markup=back_keyboard,
        parse_mode=ParseMode.HTML
    )

# 2. Turk tili
@router.message(F.text == '🇹🇷 Turk Tili')
async def info_turkish(message: Message):
    await message.answer(
        "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>🇹🇷 Turk tili</b> hozirda eng kerakli til hisoblanadi.\nFan ustozi: Aynura\nKurs narxi: 50$\nDavomiyligi: 3 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 3 kun (1/3/5) soat 14:00 dan 18:00 gacha.\nAgarda kursimizni sotib olmoqchi bo'lsangiz /buy buyrug'ini bosing.\n",
        reply_markup=back_keyboard,
        parse_mode=ParseMode.HTML
    )

# 3. Nemis tili
@router.message(F.text == '🇩🇪 Nemis Tili')
async def info_german(message: Message):
    await message.answer(
        "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>🇩🇪 Nemis tili</b> hozirda eng kerakli til hisoblanadi.\nFan ustozi: Gu'lzira\nKurs narxi: 50$\nDavomiyligi: 3 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 3 kun (2/4/6) soat 14:00 dan 18:00 gacha.\nAgarda kursimizni sotib olmoqchi bo'lsangiz /buy buyrug'ini bosing.\n",
        reply_markup=back_keyboard,
        parse_mode=ParseMode.HTML
    )

# 4. Matematika
@router.message(F.text == '🔢 Matematika')
async def info_math(message: Message):
    await message.answer(
        "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>🔢 Matematika</b> hozirda eng kerakli fan hisoblanadi.\nFan ustozi: Saida\nKurs narxi: 15$\nDavomiyligi: 2 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 2 kun (1/4) soat 16:00 dan 18:00 gacha.\nAgarda kursimizni sotib olmoqchi bo'lsangiz /buy buyrug'ini bosing.\n",
        reply_markup=back_keyboard,
        parse_mode=ParseMode.HTML
    )

# 5. Biologiya
@router.message(F.text == '🧬 Biologiya')
async def info_biology(message: Message):
    await message.answer(
        "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>🧬 Biologiya</b> hozirda eng kerakli fan hisoblanadi.\nFan ustozi: Ziliyxa\nKurs narxi: 15$\nDavomiyligi: 2 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 2 kun (2/5) soat 16:00 dan 18:00 gacha.",
        reply_markup=back_keyboard,
        parse_mode=ParseMode.HTML
    )

# 6. Huquq
@router.message(F.text == '⚖️ Huquq')
async def info_law(message: Message):
    await message.answer(
        "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>⚖️ Huquq</b> hozirda eng kerakli fan hisoblanadi.\nFan ustozi: Jetes\nKurs narxi: 15$\nDavomiyligi: 2 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 2 kun (3/6) soat 16:00 dan 18:00 gacha.\nAgarda kursimizni sotib olmoqchi bo'lsangiz /buy buyrug'ini bosing.\n",
        reply_markup=back_keyboard,
        parse_mode=ParseMode.HTML
    )

# 7. Tarix
@router.message(F.text == '📚 Tarix')
async def info_history(message: Message):
    await message.answer(
        "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>📚 Tarix</b> hozirda eng kerakli fan hisoblanadi.\nFan ustozi: Jetes\nKurs narxi: 10$\nDavomiyligi: 1 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 2 kun (2/5) soat 16:00 dan 18:00 gacha.\nAgarda kursimizni sotib olmoqchi bo'lsangiz /buy buyrug'ini bosing.\n",
        reply_markup=back_keyboard,
        parse_mode=ParseMode.HTML
    )

# --- ORQAGA QAYTISH ---
@router.message(F.text == '⬅️ Orqaga qaytish')
async def back_to_menu(message: Message):
    await message.answer(
        "Bu yerda kurslar haqida ma'lumot beriladi.", 
        reply_markup=kurs
    )

# Bosh menyu
@router.message(F.text == '🏠 Bosh menyu')
async def main_menu(message: Message):
    from aiogram.types import ReplyKeyboardRemove
    await message.answer(
        "Bosh menyuga qaytdingiz. Kurslarni ko'rish uchun /kurs buyrug'ini bosing.",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Form.name)
async def register_2(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.surname)
    await message.answer("Familiyangizni kiriting:")

@router.message(Form.surname)
async def register_3(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)

    kb = [[KeyboardButton(text="📱 Raqamni ulashish", request_contact=True)]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "Telefon raqamingizni ulashing:",
        reply_markup=keyboard
    )

    await state.set_state(Form.contact)  
    
@router.message(Form.contact, F.contact)
async def get_contact(message: Message, state: FSMContext, bot: Bot): 
    # 1. Kontakt va State'dagi ma'lumotlarni yig'amiz
    phone = message.contact.phone_number
    user_data = await state.get_data()
    
    name = user_data.get('name', 'Noma\'lum')
    surname = user_data.get('surname', 'Noma\'lum')
    
    # Ism va familiyani bazaga bitta "full_name" ustuniga birlashtiramiz
    full_name_for_db = f"{name} {surname}"
    
    # Telegram username
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"

    # 2. Bazaga saqlash (ID, F.I.O, Username, Telefon)
    try:
        add_user(
            user_id=message.from_user.id, 
            full_name=full_name_for_db, 
            username=username, 
            phone=phone
        )
    except Exception as e:
        logging.error(f"Bazaga saqlashda xatolik: {e}")

    # 3. Foydalanuvchiga ko'rsatiladigan xulosa
    summary_text = (
        "✔️ Ro‘yxatdan o‘tdingiz!\n\n"
        f"👤 Ism: {name}\n"
        f"👤 Familiya: {surname}\n"
        f"📱 Telefon: {phone}\n"
        f"Bizning kurslarimiz: /kurs"
    )

    await message.answer(summary_text, reply_markup=ReplyKeyboardRemove())

    # 4. Adminga to'liq ma'lumot yuborish
    admin_text = (
        f"🔔 Yangi o'quvchi ro'yxatdan o'tdi:\n\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"👤 Ism: {name}\n"
        f"👤 Familiya: {surname}\n"
        f"🌐 Username: {username}\n"
        f"📱 Telefon: {phone}"
    )
    
    try:
        await bot.send_message(chat_id=ADMIN_ID, text=admin_text)
    except Exception as e:
        logging.error(f"Adminga yuborishda xatolik: {e}")

    # 5. Holatni tozalash
    await state.clear()


@router.message(Command('myid'))
async def get_id(message: Message):
    await message.answer(f"Your ID: {message.from_user.id}")   


@router.message(Command('info'))
async def get_info(message: Message):
    await message.answer_animation('CAACAgIAAxkBAAICKWkkxy_IrM-YgJh5r5VW7q-602qyAAJuRwACpqBgScPVnFF2q7w5NgQ')
    await message.answer('You select info command',
                         reply_markup=creator_info)


@router.message(Command('Kurslar'))
async def select_fan(message: Message):
    await message.answer('You Select {message.text}',
                         reply_markup=kurs)
        
@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("It's a help command.")


@router.message(Command('movies'))
async def get_movies(message: Message):
    keyboard = ReplyKeyboardBuilder()
    for row in movie_list:
        keyboard.row(*row)
    await message.answer("Select a movie number:", reply_markup=keyboard.as_markup(resize_keyboard=True))



# bad_words = ["ahmoq", 'jinni', 'dick', 'pussy']
# @router.message()
# async def check_bad_words(message: Message):
#     text = message.text.lower() if message.text else ""

#     if any(bad_word in text for bad_word in bad_words):
#         await message.answer_sticker('CAACAgIAAxkBAAPSaSDDODlYKxG0u9DGlUyjOh4qybMAAlBKAAJl3qhL9kHyIFQbiGY2BA')
#     else:
#         await message.send_copy(chat_id=message.chat.id)

#     # try:
#     #     # Send a copy of the received message
#     #     await message.send_copy(chat_id=message.chat.id)
#     # except TypeError:
#     #     # But not all the types is supported to be copied so need to handle it
#     #     await message.answer("Nice try!")



# F filter example
@router.message(F.text == 'info')
async def info_aksiya(message: Message):
    await message.answer("Bu yerda aksiya haqida malumot beriladi.")    


@router.message(F.text == 'news')
async def xabar(message: Message):
    await message.answer("It's news info")


@router.message(F.text == 'name')
async def login(message: Message):
    await message.answer("Atin'iz kim ?")

@router.message(F.photo)
async def get_photo_id(message: Message):
    await message.answer(f"Photo ID: {message.photo[-1].file_id}")

@router.message(F.sticker)
async def get_sticker_id(message: Message):
    await message.answer(f"Sticker ID: {message.sticker.file_id}")

@router.message(F.animation)
async def get_animation_id(message: Message):
    await message.answer(f"Animaton ID: {message.animation.file_id}")

@router.message(F.document)
async def get_document_id(message: Message):
    await message.answer(f"Document ID: {message.document.file_id}")

@router.callback_query(F.data == 'amaliyotlar')
async def catalog(callback: CallbackQuery):
    await callback.message.answer("You select catalog", show_alert=True)



#Tolovlar uchun handler
@router.message(F.text == "/buy")
async def choose_price(message: Message):
    # Dollarda vergul muammosi bo'lmaydi, shuning uchun matnni soddalashtirdik
    builder = InlineKeyboardBuilder()
            
                # Callback_data ichida dollarda yozamiz (masalan 10 va 20 dollar)
    builder.add(InlineKeyboardButton(text="🇺🇸Ingliz Tili - 50$", callback_data="price_50"))
    builder.add(InlineKeyboardButton(text="🇷🇺Rus Tili - 50$", callback_data="price_50"))
    builder.add(InlineKeyboardButton(text="🇹🇷Turk Tili - 50$", callback_data="price_50"))
    builder.add(InlineKeyboardButton(text="🇩🇪Nemis Tili - 50$", callback_data="price_50"))
    builder.add(InlineKeyboardButton(text="🔢Matematika - 15$", callback_data="price_15"))
    builder.add(InlineKeyboardButton(text="🧬Biologiya - 15$", callback_data="price_15"))
    builder.add(InlineKeyboardButton(text="⚖️Huquq - 15$", callback_data="price_15"))
    builder.add(InlineKeyboardButton(text="📚Tariyx - 10$", callback_data="price_10"))

    builder.adjust(1)  # Har qatorda 2 ta tugma
    await message.answer("Iltimos, o'zingizga kerakli fanni tanlang:", 
                         reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("price_"))
async def send_invoice_callback(callback: CallbackQuery, bot: Bot):
    # Dollarni ajratib olamiz
    dollar_amount = int(callback.data.split("_")[1])
    
    # MUHIM: Telegramga tiyin ko'rinishida yuborish kerak (10$ * 100 = 1000 tiyin)
    total_amount = dollar_amount * 100 
    
    prices = [LabeledPrice(label="Tanlangan mahsulot", amount=total_amount)]

    try:
        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title="Siz tanlagan mahsulot",
            description=f"To'lov miqdori: {dollar_amount}$",
            payload=f"payload_{dollar_amount}",
            provider_token=PAYMENTS_PROVIDER_TOKEN,
            currency="UZS", # Bevosita "USD" deb yozish ham mumkin
            prices=[LabeledPrice(label="Mahsulot", amount=dollar_amount * 12800 * 100)],
            start_parameter="start_shopping",
        )
    except Exception as e:
        logging.error(f"Invoice yuborishda xato: {e}")
        
    await callback.answer()

@router.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    # Bu yerda bot Telegramga "Hammasi yaxshi, to'lovni qabul qilaver" deb javob beradi
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Tolov muvaffaqiyatli amalga oshgach
@router.message(F.successful_payment)
async def successful_payment_handler(message: Message):
    await message.answer("To'lov muvaffaqiyatli amalga oshirildi! Rahmat!")

def admin_only(func):
    @wraps(func)
    async def wrapper(message_or_callback, *args, **kwargs):
        admin_id = int(ADMIN_ID) if ADMIN_ID else 0
        # Agar Message bo'lsa
        if isinstance(message_or_callback, Message):
            if message_or_callback.from_user.id != admin_id:
                await message_or_callback.answer("Siz bu komandani ishlata olmaysiz!")
                return
        # Agar CallbackQuery bo'lsa
        elif isinstance(message_or_callback, CallbackQuery):
            if message_or_callback.from_user.id != admin_id:
                await message_or_callback.answer("Siz bu tugmani ishlata olmaysiz!", show_alert=True)
                return
        return await func(message_or_callback, *args, **kwargs)
    return wrapper


@router.message(Command('admin'))
@admin_only
async def admin_panel(message: Message):
    builder = InlineKeyboardBuilder()

    # Tugmalar qo'shish
    builder.add(
        InlineKeyboardButton(text="Ro'yxatdan o'tgan foydalanuvchilar", callback_data="admin_users"),
        InlineKeyboardButton(text="Broadcast xabar yuborish", callback_data="admin_broadcast")
    )

    builder.adjust(1)  # har qatorga 1 tugma

    await message.answer("Admin panelga xush kelibsiz!", reply_markup=builder.as_markup())


@router.callback_query(F.data == "admin_users")
@admin_only
async def show_users(callback: CallbackQuery):
    # Bazadan foydalanuvchilar ro'yxatini olish
    users = get_all_users()  # sening apps.database.py da yozilgan bo'lishi kerak
    text = "Ro'yxatdan o'tgan foydalanuvchilar:\n\n" + "\n".join(str(u) for u in users)
    await callback.message.edit_text(text)
    await callback.answer()


@router.callback_query(F.data == "admin_broadcast")
@admin_only
async def start_broadcast(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.broadcast)
    await callback.message.answer("Endi xabarni yuboring, u barcha foydalanuvchilarga jo'natiladi:")
    await callback.answer()



@router.message(AdminStates.broadcast)
@admin_only
async def broadcast_message(message: Message, state: FSMContext):
    users = get_all_users() # Bu funksiya tuplelar ro'yxatini qaytaradi
    text = message.text

    sent = 0
    failed = 0
    for user_row in users:
        try:
            # user_row bu (7805185795, 'Ism', 'User', 'Tel')
            # Shuning uchun user_row[0] ni olishimiz shart!
            current_user_id = user_row[0] 
            
            await message.bot.send_message(chat_id=int(current_user_id), text=text)
            sent += 1
        except Exception as e:
            print(f"Xato {user_row[0]}: {e}")
            failed += 1

    await message.answer(f"Xabar yuborildi!\n✅ Muvaffaqiyatli: {sent}\n❌ Xato: {failed}")
    await state.clear()