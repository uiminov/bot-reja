import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID
import utils.db as db

router = Router()

class AdminStates(StatesGroup):
    waiting_for_content = State()

# Команда для рассылки (доступна тебе и группе)
@router.message(Command("broadcast"), F.from_user.id.in_(ADMIN_ID))
async def start_broadcast(message: Message, state: FSMContext):
    await message.answer("Введите сообщение для рассылки (текст или фото):")
    await state.set_state(AdminStates.waiting_for_content)

@router.message(AdminStates.waiting_for_content, F.from_user.id.in_(ADMIN_ID))
async def perform_broadcast(message: Message, state: FSMContext):
    await state.clear()
    users = await db.get_all_users() # Получаем список из БД
    
    count = 0
    await message.answer(f"🚀 Начинаю рассылку на {len(users)} пользователей...")

    for user_id in users:
        try:
            await message.copy_to(chat_id=user_id)
            count += 1
            await asyncio.sleep(0.05) # Пауза для защиты от бана
        except Exception:
            pass

    await message.answer(f"✅ Рассылка завершена! Получили: {count} чел.")
