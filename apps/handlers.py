from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import logging
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from apps.database import is_registered, add_user, init_db, get_all_users
from functools import wraps
import os
from dotenv import load_dotenv
load_dotenv()

from apps.keyboard import creator_info, kurs, back_keyboard

PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")

PAYMENTS_PROVIDER_TOKEN = PAYMENT_TOKEN
CURRENCY = "UZS" 

router = Router()

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

@router.callback_query(F.data == 'kurs_en')
async def info_english(callback: CallbackQuery):
    # .answer o'rniga .edit_text ishlatamiz (Auto-delete effekti)
    try:
        await callback.message.edit_text(
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
    except Exception:
        pass


    await callback.answer()
# 1. Rus tili
@router.callback_query(F.data == 'kurs_ru')
async def info_russian(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>🇷🇺 Rus tili</b> hozirda eng kerakli til hisoblanadi.\nFan ustozi: Dilnoza\nKurs narxi: 50$\nDavomiyligi: 3 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 3 kun (2/4/6) soat 14:00 dan 18:00 gacha.\nAgarda kursimizni sotib olmoqchi bo'lsangiz /buy buyrug'ini bosing.\n",
            reply_markup=back_keyboard,
            parse_mode=ParseMode.HTML
        )
    except Exception:
        pass
    await callback.answer()

# 2. Turk tili
@router.callback_query(F.data == 'kurs_tr')
async def info_turkish(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>🇹🇷 Turk tili</b> hozirda eng kerakli til hisoblanadi.\nFan ustozi: Aynura\nKurs narxi: 50$\nDavomiyligi: 3 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 3 kun (1/3/5) soat 14:00 dan 18:00 gacha.\nAgarda kursimizni sotib olmoqchi bo'lsangiz /buy buyrug'ini bosing.\n",
            reply_markup=back_keyboard,
            parse_mode=ParseMode.HTML
        )
    except Exception:
        pass
    await callback.answer()

# 3. Nemis tili
@router.callback_query(F.data == 'kurs_de')
async def info_german(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>🇩🇪 Nemis tili</b> hozirda eng kerakli til hisoblanadi.\nFan ustozi: Gu'lzira\nKurs narxi: 50$\nDavomiyligi: 3 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 3 kun (2/4/6) soat 14:00 dan 18:00 gacha.\nAgarda kursimizni sotib olmoqchi bo'lsangiz /buy buyrug'ini bosing.\n",
            reply_markup=back_keyboard,
            parse_mode=ParseMode.HTML
        )
    except Exception:
        pass
    await callback.answer()

# 4. Matematika
@router.callback_query(F.data == 'kurs_math')
async def info_math(callback: CallbackQuery):       
    try:
        await callback.message.edit_text(
            "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>🔢 Matematika</b> hozirda eng kerakli fan hisoblanadi.\nFan ustozi: Saida\nKurs narxi: 15$\nDavomiyligi: 2 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 2 kun (1/4) soat 16:00 dan 18:00 gacha.\nAgarda kursimizni sotib olmoqchi bo'lsangiz /buy buyrug'ini bosing.\n",
            reply_markup=back_keyboard,
            parse_mode=ParseMode.HTML
        )
    except Exception:
        pass
    await callback.answer()

# 5. Biologiya
@router.callback_query(F.data == 'kurs_bio')
async def info_biology(callback: CallbackQuery):    
    try:
        await callback.message.edit_text(
            "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>🧬 Biologiya</b> hozirda eng kerakli fan hisoblanadi.\nFan ustozi: Ziliyxa\nKurs narxi: 15$\nDavomiyligi: 2 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 2 kun (2/5) soat 16:00 dan 18:00 gacha.",
            reply_markup=back_keyboard,
            parse_mode=ParseMode.HTML
        )
    except Exception:
        pass
    await callback.answer()

# 6. Huquq
@router.callback_query(F.data == 'kurs_law')
async def info_law(callback: CallbackQuery):    
    try:
        await callback.message.edit_text(
            "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>⚖️ Huquq</b> hozirda eng kerakli fan hisoblanadi.\nFan ustozi: Jetes\nKurs narxi: 15$\nDavomiyligi: 2 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 2 kun (3/6) soat 16:00 dan 18:00 gacha.\nAgarda kursimizni sotib olmoqchi bo'lsangiz /buy buyrug'ini bosing.\n",
            reply_markup=back_keyboard,
            parse_mode=ParseMode.HTML
        )
    except Exception:
        pass
    await callback.answer()

# 7. Tarix
@router.callback_query(F.data == 'kurs_history')
async def info_history(callback: CallbackQuery):    
    try:
        await callback.message.edit_text(
            "Ajoyib! Siz to'g'ri tanlov qildingiz\n<b>📚 Tarix</b> hozirda eng kerakli fan hisoblanadi.\nFan ustozi: Jetes\nKurs narxi: 10$\nDavomiyligi: 1 oy\nBoshlanish sanasi: 1-oktabr\nHaftasiga 2 kun (2/5) soat 16:00 dan 18:00 gacha.\nAgarda kursimizni sotib olmoqchi bo'lsangiz /buy buyrug'ini bosing.\n",
            reply_markup=back_keyboard,
            parse_mode=ParseMode.HTML
        )
    except Exception:
        pass
    await callback.answer()

# --- VA ENG MUHIMI: ORQAGA QAYTISH HANDLERI ---
@router.callback_query(F.data == 'back_to_courses',)
async def back_to_menu(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            "Bu yerda kurslar haqida ma'lumot beriladi.", 
            reply_markup=kurs
        )
    except Exception:
        pass
    await callback.answer()



class Form(StatesGroup):
    name = State()
    surname = State()
    contact = State()




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



@router.callback_query(F.data == 'back_to_courses')
async def back_to_menu(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            "Bu yerda kurslar haqida ma'lumot beriladi.", 
            reply_markup=kurs
        )
    except Exception:
        pass
    await callback.answer()



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

@router.message(Form.contact, F.contact)
async def get_contact(message: Message, state: FSMContext, bot: Bot): 
    phone = message.contact.phone_number
    data = await state.get_data()
    
    full_name = f"{data.get('name')} {data.get('surname')}"
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "yo'q"

    # Bazaga yozish
    add_user(user_id, full_name, username, phone)

    # Foydalanuvchiga javob
    await message.answer("Ro'yxatdan o'tdingiz!", reply_markup=ReplyKeyboardRemove())

    # ADMIN_ID ni tekshiring, u tuple bo'lmasligi kerak (masalan ADMIN_ID = 1234567)
    try:
        await bot.send_message(chat_id=int(ADMIN_ID), text=f"🔔 Yangi o'quvchi: {full_name}")
    except Exception as e:
        print(f"Admin xatosi: {e}")

    await state.clear()

def admin_only(func):
    @wraps(func)
    async def wrapper(message_or_callback, *args, **kwargs):
        # Agar Message bo'lsa
        if isinstance(message_or_callback, Message):
            if message_or_callback.from_user.id != ADMIN_ID:
                await message_or_callback.answer("Siz bu komandani ishlata olmaysiz!")
                return
        # Agar CallbackQuery bo'lsa
        elif isinstance(message_or_callback, CallbackQuery):
            if message_or_callback.from_user.id != ADMIN_ID:
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






class AdminStates(StatesGroup):
    broadcast = State()



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