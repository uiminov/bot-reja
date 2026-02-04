from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Убрал старый импорт — он больше не нужен
# from config import REQUIRED_CHANNELS as REQUIRED_CHANNELS_INVITE  ← УДАЛИТЬ ЭТУ СТРОКУ!

from config import REQUIRED_CHANNELS_INVITE  # ← правильный импорт

def get_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗂️ Moliya trekeri", callback_data="show_financial")],
        [InlineKeyboardButton(text="☑️ Vazifa trekeri", callback_data="show_task")],
        [InlineKeyboardButton(text="📊 Hosildorlik trekeri", callback_data="show_productivity")],
        [InlineKeyboardButton(text="🔥 Aksiya: 2 narxi uchun 3", callback_data="show_bundle")],
    ])


def get_product_keyboard(product_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▪️ To'lov qilish", callback_data=f"buy_{product_key}")],
        [InlineKeyboardButton(text="▪️ Bosh saxifaga", callback_data="get_welcome_message")]
    ])

def get_bundle_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▪️ To'lov qilish", callback_data="buy_bundle")],
        [InlineKeyboardButton(text="▪️ Bosh saxifaga", callback_data="get_welcome_message")]
    ])

def get_subscription_keyboard() -> InlineKeyboardMarkup:
    kb = []
    
    for idx, link in enumerate(REQUIRED_CHANNELS_INVITE, 1):
        kb.append([
            InlineKeyboardButton(
                text=f"Kanalga obuna bo'lish {idx}",
                url=link
            )
        ])
    
    kb.append([
        InlineKeyboardButton(
            text="✅ Obunani tekshirmoq",
            callback_data="check_subscription"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_back_to_home_keyboard() -> InlineKeyboardMarkup:
    """Keyboard with only the 'Bosh saxifaga' button."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▪️ Bosh saxifaga", callback_data="get_welcome_message")]
    ])


def get_home_reply_keyboard() -> ReplyKeyboardMarkup:
    # Persistent reply keyboard so user always has a "back to home" button near the input.
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text="▪️ Bosh saxifaga")]]
    )
 