from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config import PLANNERS, BUNDLE, CURRENCY
from utils.messages import get_success_message
from keyboards import get_main_menu

# Click данные (лучше перенести в .env)
CLICK_SERVICE_ID = 94950
CLICK_MERCHANT_ID = 55254
CLICK_SECRET_KEY = "ZlxY9xXrErDmTRb"
CLICK_MERCHANT_USER_ID = 77127
CLICK_RETURN_URL = "https://t.me/твой_бот_username"  # замени на свой

router = Router(name="payments")


@router.callback_query(F.data.startswith('buy_'))
async def process_buy(callback: CallbackQuery):
    choice = callback.data.split('_')[1]

    if choice == 'bundle':
        product = BUNDLE
        amount = product['price']
        payload = 'bundle'
    else:
        product = PLANNERS[choice]
        amount = product['price']
        payload = choice

    # Формируем подпись
    sign_string = f"{amount * 100}{CLICK_SERVICE_ID}{CLICK_MERCHANT_ID}{CLICK_SECRET_KEY}"
    import hashlib
    signature = hashlib.md5(sign_string.encode('utf-8')).hexdigest()

    # Ссылка на оплату Click
    payment_url = (
        f"https://my.click.uz/services/pay?"
        f"service_id={CLICK_SERVICE_ID}&"
        f"merchant_id={CLICK_MERCHANT_ID}&"
        f"amount={amount * 100}&"  # в тиынах
        f"transaction_param={payload}&"
        f"merchant_user_id={CLICK_MERCHANT_USER_ID}&"
        f"sign={signature}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("💳 Оплатить через Click", url=payment_url)],
        [InlineKeyboardButton("⬅️ Ortga", callback_data="back_to_menu")]
    ])

    await callback.message.edit_text(
        f"Оплатите {amount:,} {CURRENCY} за {product['title']}\n\nПерейдите по кнопке ниже:",
        reply_markup=keyboard
    )
    await callback.answer()
