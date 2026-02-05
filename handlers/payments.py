from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import CLICK_CONFIG,BUNDLE, PLANNERS

router = Router(name="payments")

@router.callback_query(F.data.startswith('buy_'))
async def process_buy(callback: CallbackQuery):
    choice = callback.data.split('_')[1]
    user_id = callback.from_user.id
    
    # Определяем данные товара из твоего конфига
    if choice == 'bundle':
        item = BUNDLE
    else:
        item = PLANNERS.get(choice)

    if not item:
        return await callback.answer("Xatolik: Mahsulot topilmadi")

    amount = item['price']
    title = item['title']
    
    # Создаем ID для CLICK
    merchant_trans_id = f"{user_id}:{choice}"
    
    # Ссылка на оплату
    url = (
        f"https://my.click.uz/services/pay"
        f"?service_id={CLICK_CONFIG['service_id']}"
        f"&merchant_id={CLICK_CONFIG['merchant_id']}"
        f"&amount={amount}&transaction_param={merchant_trans_id}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 CLICK orqali to'lash", url=url)],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="get_welcome_message")]
    ])

    await callback.message.answer(
        f"Siz tanladingiz: <b>{title}</b>\n"
        f"To'lov summasi: <b>{amount:,} UZS</b>".replace(',', '.'), 
        reply_markup=kb,
        parse_mode="HTML"
    )
    await callback.answer()