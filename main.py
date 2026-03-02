import sys
import os
import asyncio
import logging
import psutil
from aiogram import Bot, Dispatcher

# Твои импорты
from utils.db import init_db
from config import BOT_TOKEN
from handlers.subscription import router as subscription_router
from handlers.payments import router as payments_router
from handlers.navigation import router as navigation_router

# Логирование памяти (опционально)
process = psutil.Process(os.getpid())
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")

async def main():
    # 1. ОБЯЗАТЕЛЬНО: Создаем базу данных при старте
    init_db()
    
    # 2. Настройка логирования
    logging.basicConfig(level=logging.WARNING)

    # 3. Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # 4. Регистрация роутеров
    dp.include_router(subscription_router)
    dp.include_router(payments_router)
    dp.include_router(navigation_router)

    print("Бот запущен. Напиши /start")

    # 5. Удаляем старые сообщения, которые пришли пока бот был выключен (drop_pending_updates)
    # Это также помогает избежать ошибки Conflict
    await bot.delete_webhook(drop_pending_updates=True)

    # 6. Запуск поллинга
    await dp.start_polling(
        bot,
        polling_timeout=10
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен вручную")
