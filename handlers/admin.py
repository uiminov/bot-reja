import asyncio
import os
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Импортируем ADMIN_ID (который у вас является списком) и функции БД
from config import ADMIN_ID
import utils.db as db

router = Router(name="admin")

class AdminStates(StatesGroup):
    waiting_for_broadcast_content = State()

# 1. Команда для начала рассылки
@router.message(Command("broadcast"), F.from_user.id.in_(ADMIN_ID))
async def cmd_broadcast(message: Message, state: FSMContext):
    await message.answer("Введите текст или отправьте фото для рассылки всем пользователям:")
    await state.set_state(AdminStates.waiting_for_broadcast_content)

# 2. Обработка контента рассылки
@router.message(AdminStates.waiting_for_broadcast_content, F.from_user.id.in_(ADMIN_ID))
async def process_broadcast(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    
    users = await db.get_all_users()
    count = 0
    blocked = 0
    
    status_msg = await message.answer(f"🚀 Рассылка запущена для {len(users)} пользователей...")

    for user_id in users:
        try:
            # Копируем ваше сообщение пользователю
            await message.copy_to(chat_id=user_id)
            count += 1
            # Небольшая пауза, чтобы не поймать лимиты Telegram
            if count % 25 == 0:
                await asyncio.sleep(0.5)
        except Exception:
            blocked += 1
    
    await status_msg.edit_text(
        f"✅ Рассылка завершена!\n\n"
        f"👤 Получили: {count}\n"
        f"🚫 Заблокировали бота: {blocked}"
    )

# 3. Команда для получения файла базы данных
@router.message(Command("get_db"), F.from_user.id.in_(ADMIN_ID))
async def send_db_file(message: Message):
    if os.path.exists("bot_stats.db"):
        await message.answer_document(
            FSInputFile("bot_stats.db"), 
            caption="📂 Актуальная база данных"
        )
    else:
        await message.answer("❌ Файл базы данных не найден.")

# 4. Команда для просмотра списка ID текстом
@router.message(Command("users_list"), F.from_user.id.in_(ADMIN_ID))
async def send_users_list(message: Message):
    users = await db.get_all_users()
    if not users:
        return await message.answer("База пользователей пуста.")
    
    text = "👥 **Список пользователей:**\n\n" + "\n".join([f"`{u}`" for u in users])
    
    if len(text) > 4096:
        # Если список слишком большой для одного сообщения, сохраняем в файл
        with open("users.txt", "w") as f:
            f.write("\n".join(map(str, users)))
        await message.answer_document(FSInputFile("users.txt"), caption="Список ID пользователей")
    else:
        await message.answer(text, parse_mode="Markdown")
