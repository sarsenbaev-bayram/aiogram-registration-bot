"""
Bot holatlari (States) - FSM uchun
"""
from aiogram.fsm.state import StatesGroup, State


class RegistrationForm(StatesGroup):
    """Ro'yxatdan o'tish holatlari"""
    name = State()
    surname = State()
    contact = State()


class AdminStates(StatesGroup):
    """Admin panel holatlari"""
    broadcast = State()
    waiting_message = State()


class PaymentStates(StatesGroup):
    """To'lov holatlari"""
    selecting_course = State()
    confirming = State()
