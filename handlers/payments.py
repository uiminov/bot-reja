from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    PreCheckoutQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    URLInputFile,
)

import hashlib
import time
import uuid
import aiohttp

from config import (
    PLANNERS, BUNDLE, CURRENCY,
    CLICK_SERVICE_ID, CLICK_MERCHANT_ID, CLICK_SECRET_KEY, CLICK_MERCHANT_USER_ID,
    CLICK_RETURN_URL, CLICK_BASE_URL
)
from utils.messages import get_success_message
from keyboards import get_main_menu

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

    # Генерируем уникальный invoice_id
    invoice_id = str(uuid.uuid4())

    # Параметры для Click
    params = {
        'service_id': CLICK_SERVICE_ID,
        'merchant_id': CLICK_MERCHANT_ID,
        'amount': amount * 100,  # в тиынах (сум * 100)
        'transaction_param': payload,  # передаём payload как параметр
        'merchant_user_id': CLICK_MERCHANT_USER_ID,
        'return_url': CLICK_RETURN_URL,
    }

    # Подпись (signature) по документации Click
    sign_string = f"{params['amount']}{params['service_id']}{params['merchant_id']}{CLICK_SECRET_KEY}"
    signature = hashlib.md5(sign_string.encode('utf-8')).hexdigest()

    params['sign'] = signature

    # Формируем ссылку на оплату
    payment_url = f"https://my.click.uz/services/pay?service_id={CLICK_SERVICE_ID}&merchant_id={CLICK_MERCHANT_ID}&amount={amount * 100}&transaction_param={payload}&merchant_user_id={CLICK_MERCHANT_USER_ID}&sign={signature}"

    # Отправляем кнопку с ссылкой на оплату
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("💳 Оплатить через Click", url=payment_url)],
        [InlineKeyboardButton("⬅️ Ortga", callback_data="back_to_menu")]
    ])

    await callback.message.edit_text(
        f"Перейдите по кнопке ниже для оплаты {amount:,} {CURRENCY} за {product['title']}",
        reply_markup=keyboard
    )
    await callback.answer()


@router.message(F.successful_payment)
async def on_successful_payment(message: Message):
    # Эта функция не нужна для Click, так как оплата проходит по внешней ссылке.
    # Но если хочешь оставить на будущее — удали или закомментируй.
    pass


# Для обработки возврата после оплаты (если используешь return_url)
# Настрой webhook на сервере, если нужно обрабатывать статус оплаты
