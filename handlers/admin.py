import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID
import utils.db as db

# Обязательно эта строка!
router = Router()

class AdminStates(StatesGroup):
    waiting_for_content = State()

@router.message(Command("broadcast")) # УБРАЛИ ПРОВЕРКУ ID
async def start_broadcast(message: Message, state: FSMContext):
    # Эта строка покажет в логах КТО ПИШЕТ
    print(f"!!! КТО-ТО ПИШЕТ: {message.from_user.id}")
    
    await message.answer("Введите сообщение для рассылки:")
    await state.set_state(AdminStates.waiting_for_content)

@router.message(AdminStates.waiting_for_content, F.from_user.id.in_(ADMIN_ID))
async def perform_broadcast(message: Message, state: FSMContext):
    await state.clear()
    users = await db.get_all_users()
    
    count = 0
    await message.answer(f"🚀 Начинаю рассылку на {len(users)} пользователей...")

    for user_id in users:
        try:
            await message.copy_to(chat_id=user_id)
            count += 1
            await asyncio.sleep(0.05) # парим, чтобы не забанили
        except Exception:
            pass

    await message.answer(f"✅ Готово! Получили: {count}")
