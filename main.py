import sys
import os
import asyncio
import logging

process = psutil.Process(os.getpid())
print(process.memory_info().rss / 1024 / 1024, "MB")


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers.subscription import router as subscription_router
from handlers.payments import router as payments_router
from handlers.navigation import router as navigation_router

async def main():
    logging.basicConfig(level=logging.WARNING)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(subscription_router)  # ПЕРВАЯ — проверка подписки
    dp.include_router(payments_router)
    dp.include_router(navigation_router)

    print("Бот запущен. Напиши /start")

    await dp.start_polling(
        bot,
        drop_pending_updates=True,
        polling_timeout=10
    )

if __name__ == "__main__":

    asyncio.run(main())
