from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config import REQUIRED_CHANNELS_IDS, OSNOVA, ADMIN_ID
from keyboards import get_main_menu, get_subscription_keyboard, get_home_reply_keyboard
from utils.messages import get_welcome_message
import utils.db as db  # Импортируем нашу базу данных

router = Router(name="subscription")

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    
    # --- ЛОГИКА СТАТИСТИКИ И УВЕДОМЛЕНИЯ В ГРУППУ ---
    # Проверяем, новый ли это пользователь
    is_new = await db.add_user_if_not_exists(user_id)
    
    if is_new:
        try:
            total_users = await db.get_users_count()
            # Отправляем уведомление в твою группу
            await message.bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    f"📈 *Yangi foydalanuvchi!*\n"
                    f"👤 Ism: {message.from_user.full_name}\n"
                    f"🆔 ID: `{user_id}`\n"
                    f"📊 Jami baza: {total_users}"
                ),
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Admin guruhiga xabar yuborishda xatolik: {e}")
    # -----------------------------------------------

    # Ответ пользователю
    await message.answer_photo(
        photo=OSNOVA['image_url'],
        caption=OSNOVA['description'],
        parse_mode="MarkdownV2",
        reply_markup=get_main_menu()
    )

@router.callback_query(F.data == "check_subscription")
async def process_check_subscription(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    
    if await is_subscribed_to_all(user_id, bot):
        # Отправляем клавиатуру и приветствие
        await callback.message.answer("Menyu", reply_markup=get_home_reply_keyboard())
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
