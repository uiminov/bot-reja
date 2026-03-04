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
    # 1. Инициализация базы
    init_db()
    
    # 2. Настройка логирования (INFO поможет увидеть ошибки)
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # --- ВАЖНЫЙ ПОРЯДОК РЕГИСТРАЦИИ ---
    # Мы ставим admin_router ПЕРВЫМ. 
    # Теперь бот сначала проверит, не является ли сообщение командой /broadcast.
    dp.include_router(admin_router) 
    
    # Все остальные роутеры ниже
    dp.include_router(subscription_router)
    dp.include_router(payments_router)
    dp.include_router(navigation_router)

    print("Бот запущен. Попробуй написать /broadcast в личку боту.")

    # Очистка очереди и запуск
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
