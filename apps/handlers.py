"""
Bot handlerlari - Clean Architecture
Barcha commandlar tugmalarga o'girilgan
"""
from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from functools import wraps
import logging
import os
from dotenv import load_dotenv

from apps.database import (
    is_registered, add_user, get_all_users,
    enroll_to_course, get_pending_enrollments, get_approved_students,
    approve_enrollment, reject_enrollment, get_enrollment_by_id,
    get_user_courses, get_all_enrollments, get_course_statistics
)
from apps.keyboard import (
    main_menu, courses_menu, course_actions, contact_keyboard,
    back_to_main, admin_menu, creator_info
)

load_dotenv()

ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

router = Router()


# ============ HOLATLAR ============
class EnrollmentForm(StatesGroup):
    """Kursga yozilish formasi"""
    name = State()
    surname = State()
    contact = State()


class AdminStates(StatesGroup):
    broadcast = State()
    payment_reminder = State()


# ============ KURSLAR MA'LUMOTLARI ============
COURSES = {
    "🇺🇸 Ingliz Tili": {"name": "Ingliz tili", "teacher": "Ziyada", "price": 50, "duration": "3 oy", "schedule": "1/3/5, 14:00-18:00", "level": "Beginner"},
    "🇷🇺 Rus Tili": {"name": "Rus tili", "teacher": "Dilnoza", "price": 50, "duration": "3 oy", "schedule": "2/4/6, 14:00-18:00"},
    "🇹🇷 Turk Tili": {"name": "Turk tili", "teacher": "Aynura", "price": 50, "duration": "3 oy", "schedule": "1/3/5, 14:00-18:00"},
    "🇩🇪 Nemis Tili": {"name": "Nemis tili", "teacher": "Gu'lzira", "price": 50, "duration": "3 oy", "schedule": "2/4/6, 14:00-18:00"},
    "🔢 Matematika": {"name": "Matematika", "teacher": "Saida", "price": 15, "duration": "2 oy", "schedule": "1/4, 16:00-18:00"},
    "🧬 Biologiya": {"name": "Biologiya", "teacher": "Ziliyxa", "price": 15, "duration": "2 oy", "schedule": "2/5, 16:00-18:00"},
    "⚖️ Huquq": {"name": "Huquq", "teacher": "Jetes", "price": 15, "duration": "2 oy", "schedule": "3/6, 16:00-18:00"},
    "📚 Tarix": {"name": "Tarix", "teacher": "Jetes", "price": 10, "duration": "1 oy", "schedule": "2/5, 16:00-18:00"},
}


# ============ ADMIN DECORATOR ============
def admin_only(func):
    @wraps(func)
    async def wrapper(message_or_callback, *args, **kwargs):
        user_id = message_or_callback.from_user.id
        if user_id != ADMIN_ID:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("⛔ Bu funksiya faqat admin uchun!")
            elif isinstance(message_or_callback, CallbackQuery):
                await message_or_callback.answer("⛔ Bu funksiya faqat admin uchun!", show_alert=True)
            return
        return await func(message_or_callback, *args, **kwargs)
    return wrapper


# ==================== START / ASOSIY ==================== 
@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    """Botni ishga tushirish"""
    await state.clear()
    user_id = message.from_user.id
    tg_name = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
    
    # Bazaga saqlash
    add_user(user_id, tg_name, username)
    
    # Har doim main_menu ko'rsatiladi
    await message.answer(
        f"👋 Xush kelibsiz, {message.from_user.first_name}!\n\n"
        "Quyidagi menyudan kerakli bo'limni tanlang:",
        reply_markup=main_menu
    )


# ==================== BOSH MENYU ==================== 
@router.message(F.text == '🏠 Bosh menyu')
async def go_main_menu(message: Message, state: FSMContext):
    """Bosh menyuga qaytish"""
    await state.clear()
    await message.answer(
        "🏠 Bosh menyu\n\nQuyidagi bo'limlardan birini tanlang:",
        reply_markup=main_menu
    )


# ==================== KURSLAR ==================== 
@router.message(F.text == '📚 Kurslar')
async def show_courses(message: Message):
    """Kurslar ro'yxati"""
    await message.answer(
        "📚 <b>Bizning kurslar</b>\n\n"
        "Quyidagi kurslardan birini tanlang:",
        reply_markup=courses_menu,
        parse_mode=ParseMode.HTML
    )


# Barcha kurslar uchun handler
@router.message(F.text.in_(COURSES.keys()))
async def show_course_info(message: Message, state: FSMContext):
    """Kurs haqida ma'lumot"""
    course_key = message.text
    course = COURSES[course_key]
    
    # Tanlangan kursni saqlash
    await state.update_data(selected_course=course_key)
    
    level_text = f"📊 Daraja: {course.get('level', 'Barcha darajalar')}\n" if 'level' in course else ""
    
    text = (
        f"✅ <b>Ajoyib tanlov!</b>\n\n"
        f"📖 <b>{course['name']}</b>\n\n"
        f"👨‍🏫 Ustoz: {course['teacher']}\n"
        f"{level_text}"
        f"💰 Narxi: {course['price']}$\n"
        f"⏱ Davomiyligi: {course['duration']}\n"
        f"📅 Jadval: {course['schedule']}\n\n"
        f"Kursga yozilish uchun quyidagi tugmani bosing:"
    )
    
    await message.answer(text, reply_markup=course_actions, parse_mode=ParseMode.HTML)


# ==================== KURSGA YOZILISH (RO'YXATDAN O'TISH) ==================== 
@router.message(F.text == '💳 Kursga yozilish')
async def start_enrollment(message: Message, state: FSMContext):
    """Kursga yozilish - ro'yxatdan o'tish boshlanadi"""
    data = await state.get_data()
    course_key = data.get('selected_course')
    
    if not course_key or course_key not in COURSES:
        await message.answer("❌ Avval kursni tanlang!", reply_markup=courses_menu)
        return
    
    course = COURSES[course_key]
    
    await message.answer(
        f"📝 <b>{course['name']} kursiga yozilish</b>\n\n"
        f"Iltimos, ismingizni kiriting:",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML
    )
    await state.set_state(EnrollmentForm.name)


@router.message(EnrollmentForm.name)
async def enrollment_name(message: Message, state: FSMContext):
    """Ism kiritish"""
    await state.update_data(name=message.text)
    await message.answer("Familiyangizni kiriting:")
    await state.set_state(EnrollmentForm.surname)


@router.message(EnrollmentForm.surname)
async def enrollment_surname(message: Message, state: FSMContext):
    """Familiya kiritish"""
    await state.update_data(surname=message.text)
    await message.answer(
        "📱 Telefon raqamingizni ulashing:",
        reply_markup=contact_keyboard
    )
    await state.set_state(EnrollmentForm.contact)


@router.message(EnrollmentForm.contact, F.contact)
async def enrollment_contact(message: Message, state: FSMContext, bot: Bot):
    """Telefon raqam - ariza yakunlanadi"""
    phone = message.contact.phone_number
    data = await state.get_data()
    
    name = data.get('name', '')
    surname = data.get('surname', '')
    course_key = data.get('selected_course', '')
    full_name = f"{name} {surname}"
    
    course = COURSES.get(course_key, {})
    course_name = course.get('name', course_key)
    
    # Bazaga saqlash
    try:
        add_user(message.from_user.id, full_name, 
                f"@{message.from_user.username}" if message.from_user.username else "", phone)
        enroll_to_course(message.from_user.id, full_name, phone, course_name)
    except Exception as e:
        logging.error(f"Bazaga saqlashda xato: {e}")
    
    # Foydalanuvchiga xabar
    await message.answer(
        f"✅ <b>Arizangiz qabul qilindi!</b>\n\n"
        f"👤 Ism: {name}\n"
        f"👤 Familiya: {surname}\n"
        f"📱 Telefon: {phone}\n"
        f"📚 Kurs: {course_name}\n\n"
        f"⏳ Admin arizangizni ko'rib chiqadi va tez orada siz bilan bog'lanadi.\n\n"
        f"💡 <i>Eslatma: Kurs to'lovi har oy boshida amalga oshiriladi.</i>",
        reply_markup=main_menu,
        parse_mode=ParseMode.HTML
    )
    
    # Adminga xabar + tasdiqlash tugmalari
    admin_text = (
        f"🔔 <b>Yangi ariza!</b>\n\n"
        f"👤 F.I.O: {full_name}\n"
        f"📱 Telefon: {phone}\n"
        f"📚 Kurs: {course_name}\n"
        f"🆔 User ID: <code>{message.from_user.id}</code>"
    )
    
    # Inline tugmalar
    pending = get_pending_enrollments()
    if pending:
        last_enrollment = pending[-1]
        enrollment_id = last_enrollment[0]
        
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve_{enrollment_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_{enrollment_id}")
        )
        
        try:
            await bot.send_message(ADMIN_ID, admin_text, reply_markup=builder.as_markup(), parse_mode=ParseMode.HTML)
        except Exception as e:
            logging.error(f"Adminga xabar yuborishda xato: {e}")
    
    await state.clear()


# ==================== ADMIN - ARIZA TASDIQLASH ==================== 
@router.callback_query(F.data.startswith("approve_"))
@admin_only
async def approve_student(callback: CallbackQuery, bot: Bot):
    """Arizani tasdiqlash"""
    enrollment_id = int(callback.data.split("_")[1])
    enrollment = get_enrollment_by_id(enrollment_id)
    
    if not enrollment:
        await callback.answer("Ariza topilmadi!", show_alert=True)
        return
    
    user_id = enrollment[1]
    full_name = enrollment[2]
    course_name = enrollment[4]
    
    approve_enrollment(enrollment_id)
    
    # O'quvchiga xabar
    try:
        await bot.send_message(
            user_id,
            f"🎉 <b>Tabriklaymiz!</b>\n\n"
            f"Sizning <b>{course_name}</b> kursiga arizangiz tasdiqlandi!\n\n"
            f"📍 Darslar tez orada boshlanadi.\n"
            f"💰 To'lov har oy boshida amalga oshiriladi.\n\n"
            f"Savollar bo'lsa, biz bilan bog'laning!",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logging.error(f"O'quvchiga xabar yuborishda xato: {e}")
    
    await callback.message.edit_text(
        callback.message.text + f"\n\n✅ <b>TASDIQLANDI</b>",
        parse_mode=ParseMode.HTML
    )
    await callback.answer("O'quvchi tasdiqlandi!", show_alert=True)


@router.callback_query(F.data.startswith("reject_"))
@admin_only
async def reject_student(callback: CallbackQuery, bot: Bot):
    """Arizani rad etish"""
    enrollment_id = int(callback.data.split("_")[1])
    enrollment = get_enrollment_by_id(enrollment_id)
    
    if not enrollment:
        await callback.answer("Ariza topilmadi!", show_alert=True)
        return
    
    user_id = enrollment[1]
    course_name = enrollment[4]
    
    reject_enrollment(enrollment_id)
    
    # O'quvchiga xabar
    try:
        await bot.send_message(
            user_id,
            f"❌ <b>Afsus!</b>\n\n"
            f"Sizning <b>{course_name}</b> kursiga arizangiz rad etildi.\n\n"
            f"Savollar bo'lsa, biz bilan bog'laning.",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logging.error(f"O'quvchiga xabar yuborishda xato: {e}")
    
    await callback.message.edit_text(
        callback.message.text + f"\n\n❌ <b>RAD ETILDI</b>",
        parse_mode=ParseMode.HTML
    )
    await callback.answer("Ariza rad etildi!", show_alert=True)


# ==================== MANZIL ==================== 
@router.message(F.text == '📍 Manzil')
async def show_address(message: Message):
    """Manzilni ko'rsatish"""
    await message.answer(
        "📍 <b>Bizning manzil</b>\n\n"
        "🏢 O'quv markazi\n"
        "📌 Lokatsiya: https://maps.app.goo.gl/hEN8Jci7PUbSDLu46\n\n"
        "Sizni kutamiz! 🤗",
        reply_markup=main_menu,
        parse_mode=ParseMode.HTML
    )


# ==================== PROFIL ==================== 
@router.message(F.text == '👤 Profil')
async def show_profile(message: Message):
    """Foydalanuvchi profili"""
    user = message.from_user
    username = f"@{user.username}" if user.username else "Mavjud emas"
    
    await message.answer(
        f"👤 <b>Sizning profilingiz</b>\n\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"👤 Ism: {user.first_name}\n"
        f"👤 Familiya: {user.last_name or 'Mavjud emas'}\n"
        f"🌐 Username: {username}\n",
        reply_markup=main_menu,
        parse_mode=ParseMode.HTML
    )


# ==================== MENING KURSLARIM ==================== 
@router.message(F.text == '📖 Mening kurslarim')
async def my_courses(message: Message):
    """Foydalanuvchining kurslari"""
    user_id = message.from_user.id
    courses = get_user_courses(user_id)
    
    if not courses:
        await message.answer(
            "📖 <b>Mening kurslarim</b>\n\n"
            "❌ Siz hali hech qanday kursga yozilmagansiz.\n\n"
            "📚 Kurslarni ko'rish uchun <b>📚 Kurslar</b> tugmasini bosing.",
            reply_markup=main_menu,
            parse_mode=ParseMode.HTML
        )
        return
    
    text = "📖 <b>Mening kurslarim</b>\n\n"
    
    for course in courses:
        enrollment_id, course_name, status, enrolled_at, approved_at = course
        
        # Status emoji
        if status == 'pending':
            status_text = "⏳ Kutilmoqda"
        elif status == 'approved':
            status_text = "✅ Tasdiqlangan"
        else:
            status_text = "❌ Rad etilgan"
        
        text += (
            f"📚 <b>{course_name}</b>\n"
            f"   📅 Yozilgan: {enrolled_at[:10] if enrolled_at else '-'}\n"
            f"   📌 Holat: {status_text}\n"
        )
        
        if approved_at:
            text += f"   ✅ Tasdiqlangan: {approved_at[:10]}\n"
        
        text += "\n"
    
    await message.answer(text, reply_markup=main_menu, parse_mode=ParseMode.HTML)


# ==================== ALOQA ==================== 
@router.message(F.text == '📞 Aloqa')
async def show_contact(message: Message):
    """Aloqa ma'lumotlari"""
    await message.answer(
        "📞 <b>Biz bilan bog'laning</b>\n\n"
        "Quyidagi ijtimoiy tarmoqlar orqali biz bilan bog'lanishingiz mumkin:",
        reply_markup=creator_info,
        parse_mode=ParseMode.HTML
    )


# ==================== YORDAM ==================== 
@router.message(F.text == 'ℹ️ Yordam')
async def show_help(message: Message):
    """Yordam"""
    await message.answer(
        "ℹ️ <b>Yordam</b>\n\n"
        "🔹 <b>📚 Kurslar</b> - Mavjud kurslarni ko'rish\n"
        "🔹 <b>📍 Manzil</b> - https://maps.app.goo.gl/uuor6svgj2v5CTFY8\n"
        "🔹 <b>👤 Profil</b> - @sarsenbaevv_b\n"
        "🔹 <b>📞 Aloqa</b> - +998902626244\n\n"
        "Savollar bo'lsa, 📞 Aloqa orqali murojaat qiling!",
        reply_markup=main_menu,
        parse_mode=ParseMode.HTML
    )


# ==================== ORQAGA ==================== 
@router.message(F.text == '⬅️ Orqaga')
async def go_back(message: Message):
    """Orqaga - kurslar ro'yxatiga"""
    await message.answer(
        "📚 Kurslardan birini tanlang:",
        reply_markup=courses_menu
    )


# ==================== ADMIN PANEL ==================== 
@router.message(Command('admin'))
@admin_only
async def cmd_admin(message: Message):
    """Admin panel"""
    await message.answer(
        "👨‍💼 <b>Admin Panel</b>\n\n"
        "Quyidagi funksiyalardan foydalaning:",
        reply_markup=admin_menu,
        parse_mode=ParseMode.HTML
    )


@router.message(F.text == '👥 Foydalanuvchilar')
@admin_only
async def show_users(message: Message):
    """Foydalanuvchilar ro'yxati"""
    users = get_all_users()
    
    if not users:
        await message.answer("Hozircha foydalanuvchilar yo'q.", reply_markup=admin_menu)
        return
    
    text = f"👥 <b>Foydalanuvchilar ({len(users)} ta)</b>\n\n"
    no_phone = "Tel yoq"
    for i, user in enumerate(users[:20], 1):  # Birinchi 20 tasi
        text += f"{i}. {user[1]} | {user[2]} | {user[3] or no_phone}\n"
    
    if len(users) > 20:
        text += f"\n... va yana {len(users) - 20} ta"
    
    await message.answer(text, reply_markup=admin_menu, parse_mode=ParseMode.HTML)


@router.message(F.text == '📢 Xabar yuborish')
@admin_only
async def start_broadcast(message: Message, state: FSMContext):
    """Broadcast boshlash"""
    await message.answer(
        "📢 Xabarni yozing.\n\nBarcha foydalanuvchilarga yuboriladi:",
        reply_markup=back_to_main
    )
    await state.set_state(AdminStates.broadcast)


@router.message(AdminStates.broadcast)
@admin_only
async def do_broadcast(message: Message, state: FSMContext, bot: Bot):
    """Xabarni yuborish"""
    users = get_all_users()
    text = message.text
    
    sent, failed = 0, 0
    for user in users:
        try:
            await bot.send_message(user[0], text)
            sent += 1
        except Exception:
            failed += 1
    
    await message.answer(
        f"✅ Xabar yuborildi!\n\n"
        f"📤 Yuborildi: {sent}\n"
        f"❌ Xato: {failed}",
        reply_markup=admin_menu
    )
    await state.clear()


@router.message(F.text == '📊 Statistika')
@admin_only
async def show_stats(message: Message):
    """Statistika"""
    users = get_all_users()
    registered = len([u for u in users if u[3]])  # Telefoni bor
    pending = get_pending_enrollments()
    approved = get_approved_students()
    course_stats = get_course_statistics()
    
    text = (
        f"📊 <b>Statistika</b>\n\n"
        f"👥 Jami foydalanuvchilar: {len(users)}\n"
        f"✅ Ro'yxatdan o'tgan: {registered}\n"
        f"⏳ Ro'yxatdan o'tmagan: {len(users) - registered}\n\n"
        f"📋 Kutayotgan arizalar: {len(pending)}\n"
        f"✅ Tasdiqlangan o'quvchilar: {len(approved)}\n\n"
    )
    
    # Kurslar bo'yicha statistika
    if course_stats:
        text += "📚 <b>Kurslar bo'yicha:</b>\n"
        course_data = {}
        for course_name, count, status in course_stats:
            if course_name not in course_data:
                course_data[course_name] = {'pending': 0, 'approved': 0}
            course_data[course_name][status] = count
        
        for course_name, data in course_data.items():
            pending_count = data.get('pending', 0)
            approved_count = data.get('approved', 0)
            total = pending_count + approved_count
            text += f"  • {course_name}: {total} ta (✅{approved_count} / ⏳{pending_count})\n"
    
    await message.answer(text, reply_markup=admin_menu, parse_mode=ParseMode.HTML)


@router.message(F.text == '📋 Yangi arizalar')
@admin_only
async def show_pending_enrollments(message: Message):
    """Kutayotgan arizalarni ko'rsatish"""
    pending = get_pending_enrollments()
    
    if not pending:
        await message.answer(
            "📋 Hozircha yangi arizalar yo'q.",
            reply_markup=admin_menu
        )
        return
    
    text = f"📋 <b>Kutayotgan arizalar ({len(pending)} ta)</b>\n\n"
    
    for enrollment in pending[:10]:  # Birinchi 10 tasi
        enrollment_id, user_id, full_name, phone, course, status, enrolled_at, _, _ = enrollment
        text += (
            f"🆔 #{enrollment_id}\n"
            f"👤 {full_name}\n"
            f"📱 {phone}\n"
            f"📚 {course}\n"
            f"📅 {enrolled_at[:10] if enrolled_at else '-'}\n\n"
        )
        
        # Inline tugmalar har bir ariza uchun
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve_{enrollment_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_{enrollment_id}")
        )
        
        await message.answer(
            f"📋 <b>Ariza #{enrollment_id}</b>\n\n"
            f"👤 F.I.O: {full_name}\n"
            f"📱 Telefon: {phone}\n"
            f"📚 Kurs: {course}\n"
            f"📅 Sana: {enrolled_at[:10] if enrolled_at else '-'}",
            reply_markup=builder.as_markup(),
            parse_mode=ParseMode.HTML
        )
    
    if len(pending) > 10:
        await message.answer(
            f"... va yana {len(pending) - 10} ta ariza bor.",
            reply_markup=admin_menu
        )


@router.message(F.text == '✅ Tasdiqlangan')
@admin_only
async def show_approved_students(message: Message):
    """Tasdiqlangan o'quvchilar ro'yxati"""
    approved = get_approved_students()
    
    if not approved:
        await message.answer(
            "✅ Hozircha tasdiqlangan o'quvchilar yo'q.",
            reply_markup=admin_menu
        )
        return
    
    text = f"✅ <b>Tasdiqlangan o'quvchilar ({len(approved)} ta)</b>\n\n"
    
    for i, student in enumerate(approved[:15], 1):
        enrollment_id, user_id, full_name, phone, course, status, enrolled_at, approved_at, _ = student
        text += f"{i}. {full_name} | {course} | {phone}\n"
    
    if len(approved) > 15:
        text += f"\n... va yana {len(approved) - 15} ta"
    
    await message.answer(text, reply_markup=admin_menu, parse_mode=ParseMode.HTML)


@router.message(F.text == '💰 To\'lov eslatmasi')
@admin_only
async def start_payment_reminder(message: Message, state: FSMContext):
    """To'lov eslatmasini boshlash"""
    approved = get_approved_students()
    
    if not approved:
        await message.answer(
            "❌ Hozircha tasdiqlangan o'quvchilar yo'q.",
            reply_markup=admin_menu
        )
        return
    
    await message.answer(
        f"💰 <b>To'lov eslatmasi</b>\n\n"
        f"Tasdiqlangan o'quvchilar: {len(approved)} ta\n\n"
        f"Eslatma xabarini yozing (barchaga yuboriladi):\n\n"
        f"<i>Masalan: Hurmatli o'quvchi! Oylik to'lov vaqti keldi...</i>",
        reply_markup=back_to_main,
        parse_mode=ParseMode.HTML
    )
    await state.set_state(AdminStates.payment_reminder)


@router.message(AdminStates.payment_reminder)
@admin_only
async def send_payment_reminder(message: Message, state: FSMContext, bot: Bot):
    """To'lov eslatmasini yuborish"""
    approved = get_approved_students()
    reminder_text = message.text
    
    sent, failed = 0, 0
    
    for student in approved:
        user_id = student[1]
        full_name = student[2]
        course = student[4]
        
        try:
            await bot.send_message(
                user_id,
                f"💰 <b>To'lov eslatmasi</b>\n\n"
                f"Hurmatli {full_name}!\n\n"
                f"📚 Kurs: {course}\n\n"
                f"{reminder_text}\n\n"
                f"Savollar bo'lsa, biz bilan bog'laning!",
                parse_mode=ParseMode.HTML
            )
            sent += 1
        except Exception as e:
            logging.error(f"Eslatma yuborishda xato {user_id}: {e}")
            failed += 1
    
    await message.answer(
        f"✅ <b>To'lov eslatmasi yuborildi!</b>\n\n"
        f"📤 Yuborildi: {sent}\n"
        f"❌ Xato: {failed}",
        reply_markup=admin_menu,
        parse_mode=ParseMode.HTML
    )
    await state.clear()


# ==================== MEDIA HANDLERLAR ==================== 
@router.message(F.photo)
async def handle_photo(message: Message):
    await message.answer(f"🖼 Rasm ID: <code>{message.photo[-1].file_id}</code>", parse_mode=ParseMode.HTML)


@router.message(F.sticker)
async def handle_sticker(message: Message):
    await message.answer(f"🎭 Sticker ID: <code>{message.sticker.file_id}</code>", parse_mode=ParseMode.HTML)


@router.message(F.document)
async def handle_document(message: Message):
    await message.answer(f"📄 Fayl ID: <code>{message.document.file_id}</code>", parse_mode=ParseMode.HTML)
