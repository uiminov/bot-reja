from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config import REQUIRED_CHANNELS_IDS
from keyboards import get_main_menu, get_subscription_keyboard, get_home_reply_keyboard
from utils.messages import get_welcome_message
from config import OSNOVA

router = Router(name="subscription")


# subscription.py — минимальное изменение
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer_photo(
        photo=OSNOVA['image_url'],                     # ← фото из config
        caption=OSNOVA['description'],                 # ← текст под фото
        parse_mode="MarkdownV2",                       # ← обязательно для форматирования
        reply_markup=get_main_menu()                   # ← ваша главная клавиатура
    )
@router.callback_query(F.data == "check_subscription")
async def process_check_subscription(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    
    if await is_subscribed_to_all(user_id, bot):
        # Send a fresh message to set reply keyboard, then show inline menu.
        await callback.message.answer("Меню", reply_markup=get_home_reply_keyboard())
        await callback.message.answer(get_welcome_message(), reply_markup=get_main_menu())
        try:
            await callback.message.delete()
        except Exception:
            pass
        await callback.answer("Obuna tasdiqlandi! Xush kelibsiz! 🎉", show_alert=True)
    else:
        await callback.answer("Siz hali hamma kanallarga obuna bo'lmagansiz.", show_alert=True)


async def is_subscribed_to_all(user_id: int, bot: Bot) -> bool:
    for channel_id in REQUIRED_CHANNELS_IDS:
        try:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status in ["left", "kicked"]:
                return False
        except Exception as e:
            print(f"Tasdiqlashda xatolik {channel_id}: {e}")
            return False
    
    return True