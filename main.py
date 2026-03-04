import sys
import os
import asyncio
import logging
from aiogram import Bot, Dispatcher

# Твои импорты
from utils.db import init_db
from config import BOT_TOKEN
from handlers.subscription import router as subscription_router
from handlers.payments import router as payments_router
from handlers.navigation import router as navigation_router
from handlers.admin import router as admin_router

async def main():
    # 1. Создаем базу данных
    init_db()
    
    # 2. Настройка логирования
    logging.basicConfig(level=logging.INFO)

    # 3. Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # 4. Регистрация роутеров — ПОРЯДОК ИМЕЕТ ЗНАЧЕНИЕ!
    # Ставим admin_router САМЫМ ПЕРВЫМ, чтобы его команды не перехватывались
    dp.include_router(admin_router)
    dp.include_router(subscription_router)
    dp.include_router(payments_router)
    dp.include_router(navigation_router)

    print("Бот запущен. Попробуй написать /broadcast")

    # 5. Очистка очереди обновлений и запуск
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
