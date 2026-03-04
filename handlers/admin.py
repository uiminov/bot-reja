import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID
import utils.db as db

router = Router()

class AdminStates(StatesGroup):
    waiting_for_content = State()

# Команда /broadcast — доступна только тебе и группе из ADMIN_ID
@router.message(Command("broadcast"), F.from_user.id.in_(ADMIN_ID))
async def start_broadcast(message: Message, state: FSMContext):
    await message.answer("Отправь сообщение (текст/фото), которое нужно разослать всем:")
    await state.set_state(AdminStates.waiting_for_content)

@router.message(AdminStates.waiting_for_content, F.from_user.id.in_(ADMIN_ID))
async def perform_broadcast(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    users = await db.get_all_users()
    
    success = 0
    blocked = 0
    
    msg = await message.answer(f"⏳ Начинаю рассылку на {len(users)} чел...")

    for user_id in users:
        try:
            # Копируем сообщение целиком
            await message.copy_to(chat_id=user_id)
            success += 1
            await asyncio.sleep(0.05) # чтобы телеграм не забанил
        except Exception:
            blocked += 1

    await msg.edit_text(f"✅ Готово!\n👍 Получили: {success}\n👎 Заблокировали: {blocked}")
