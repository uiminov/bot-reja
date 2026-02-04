from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    PreCheckoutQuery,
    Message,
)

from config import PLANNERS, BUNDLE, PROVIDER_TOKEN, CURRENCY, OSNOVA
from utils.messages import get_success_message
from keyboards import get_main_menu

router = Router(name="payments")


@router.callback_query(F.data.startswith('buy_'))
async def process_buy(callback: CallbackQuery):
    choice = callback.data.split('_')[1]

    if choice == 'bundle':
        product = BUNDLE
        prices = [LabeledPrice(label=product['title'], amount=product['price'] * 100)]
        payload = 'bundle'
        # Short description for invoice
        short_description = f"Aksiya : 2 tani narxiga 3 {product['price']:,} {CURRENCY}"
    else:
        product = PLANNERS[choice]
        prices = [LabeledPrice(label=product['title'], amount=product['price'] * 100)]
        payload = choice
        # Short description for invoice
        short_description = f"{product['title']} - {product['price']:,} {CURRENCY}"

    await callback.bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=product['title'],
        description=short_description,
        payload=payload,
        provider_token=PROVIDER_TOKEN,
        currency=CURRENCY,
        prices=prices,
        start_parameter='planex-shop',
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        is_flexible=False
    )
    await callback.answer()


@router.pre_checkout_query()
async def on_pre_checkout(pre_checkout: PreCheckoutQuery):
    await pre_checkout.bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    
    # 1. Отправляем сообщение с ссылкой(ами) — как было
    success_text = get_success_message(payload)
    await message.answer(success_text)
    
    # 2. Сразу следом отправляем главное меню (фото + текст + кнопки)
    await message.answer_photo(
        photo=OSNOVA['image_url'],
        caption=OSNOVA['description'],
        parse_mode="MarkdownV2",
        reply_markup=get_main_menu()
    )