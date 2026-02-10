from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from config import PROVIDER_TOKEN, CURRENCY, PLANNERS, BUNDLE

router = Router(name="payments")

@router.callback_query(F.data.startswith('buy_'))
async def process_buy(callback: CallbackQuery):
    choice = callback.data.split('_')[1]
    
    # 1. Извлекаем данные из конфига в зависимости от выбора
    if choice == 'bundle':
        product_data = BUNDLE
    else:
        product_data = PLANNERS.get(choice)

    if not product_data:
        return await callback.answer("Mahsulot topilmadi.")

    title = product_data['title']
    # Очищаем Markdown-экранирование для описания в инвойсе (инвойс не всегда хорошо ест \)
    description = product_data['description'].replace('\\.', '.').replace('\\!', '!')
    # Убираем лишние спецсимволы, чтобы описание в инвойсе было чистым
    clean_description = description.split('▪️')[0].strip() # Берем текст до цены
    
    price = product_data['price']
    image_url = product_data.get('image_url')

    # 2. Формируем цену (умножаем на 100 для тийинов)
    prices = [LabeledPrice(label=title, amount=int(price * 100))]

    # 3. Отправляем инвойс
    await callback.message.answer_invoice(
        title=title,
        description=f"Planerga kirish huquqini sotib olish: {title}",
        payload=choice,
        provider_token=PROVIDER_TOKEN,
        currency=CURRENCY,
        prices=prices,
        photo_url=image_url,    # Изображение товара
        photo_size=512,         # Размер
        photo_width=512,
        photo_height=280,
        start_parameter="planner_payment",
        need_name=False,        # Нам не нужны лишние данные клиента
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        is_flexible=False
    )
    await callback.answer()

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    # Подтверждаем, что товар готов к продаже
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    from utils.messages import get_success_message
    
    # Отправляем сообщение со ссылками на скачивание
    text = get_success_message(payload)
    await message.answer(text, parse_mode="Markdown")

