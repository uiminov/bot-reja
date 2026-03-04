from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import ADMIN_ID
import utils.db as db


router = Router(name="admin")

class AdminStates(StatesGroup):
    waiting_for_broadcast_content = State()

# Команда для запуска рассылки (только для админа)
@router.message(Command("broadcast"), F.from_user.id == ADMIN_ID)
async def cmd_broadcast(message: Message, state: FSMContext):
    await message.answer("Введите текст или отправьте фото/видео для рассылки всем пользователям:")
    await state.set_state(AdminStates.waiting_for_broadcast_content)

# Обработка сообщения для рассылки
@router.message(AdminStates.waiting_for_broadcast_content, F.from_user.id == ADMIN_ID)
async def process_broadcast(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    
    users = await db.get_all_users()
    count = 0
    blocked = 0
    
    status_msg = await message.answer(f"🚀 Рассылка начата для {len(users)} пользователей...")

    for user_id in users:
        try:
            # Метод copy_to позволяет переслать любое сообщение (текст, фото, файл)
            await message.copy_to(chat_id=user_id)
            count += 1
            # Небольшая пауза, чтобы Telegram не заблокировал за спам
            if count % 20 == 0:
                await asyncio.sleep(0.5)
        except Exception:
            blocked += 1
    
    await status_msg.edit_text(
        f"✅ Рассылка завершена!\n\n"
        f"👤 Получили: {count}\n"
        f"🚫 Заблокировали бота: {blocked}"
    )
