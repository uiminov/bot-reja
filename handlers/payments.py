from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from config import PROVIDER_TOKEN, CURRENCY, PLANNERS, BUNDLE

router = Router(name="payments")

@router.callback_query(F.data.startswith('buy_'))
async def process_buy(callback: CallbackQuery):
    choice = callback.data.split('_')[1]
    
    if choice == 'bundle':
        title = BUNDLE['title']
        description = "Paket: 3 ta planer"
        price = BUNDLE['price']
    else:
        title = PLANNERS[choice]['title']
        description = "Elektron planer"
        price = PLANNERS[choice]['price']

    # Telegram принимает цены в минимальных единицах валюты (тийинах)
    # 69000 UZS -> 6900000
    prices = [LabeledPrice(label=title, amount=price * 100)]

    await callback.message.answer_invoice(
        title=title,
        description=description,
        payload=choice, # ID товара, вернется в успешном платеже
        provider_token=PROVIDER_TOKEN,
        currency=CURRENCY,
        prices=prices,
        start_parameter="planner_payment"
    )
    await callback.answer()

# Обязательный ответ на предварительный запрос (проверка наличия товара)
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

# Обработка после успешной оплаты
@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    # Здесь можно вызвать вашу функцию get_success_message(payload)
    from utils.messages import get_success_message
    
    text = get_success_message(payload)
    await message.answer(text)
