import asyncio
import logging
from aiogram import Bot, Dispatcher
from utils.db import init_db
from config import BOT_TOKEN
from handlers.subscription import router as subscription_router
from handlers.payments import router as payments_router
from handlers.navigation import router as navigation_router
from handlers.admin import router as admin_router
from handlers.promotion import router as promotion_router

async def main():
    init_db()
    
    # ИЗМЕНЕНО: ставим WARNING, чтобы не видеть INFO сообщения красным
    logging.basicConfig(level=logging.WARNING)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(promotion_router)
    dp.include_router(admin_router) 
    dp.include_router(subscription_router)
    dp.include_router(payments_router)
    dp.include_router(navigation_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())