from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import CLICK_CONFIG

router = Router(name="payments")

@router.callback_query(F.data.startswith('buy_'))
async def process_buy(callback: CallbackQuery):
    choice = callback.data.split('_')[1]
    user_id = callback.from_user.id
    
    # Определяем цену
    amount = 129000 if choice == 'bundle' else 69000
    
    # Формируем ID транзакции для себя: "ID_ПОЛЬЗОВАТЕЛЯ:ТОВАР"
    merchant_trans_id = f"{user_id}:{choice}"
    
    # Генерируем ссылку для перехода
    url = (
        f"https://my.click.uz/services/pay"
        f"?service_id={CLICK_CONFIG['service_id']}"
        f"&merchant_id={CLICK_CONFIG['merchant_id']}"
        f"&amount={amount}"
        f"&transaction_param={merchant_trans_id}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 CLICK orqali to'lash", url=url)],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="get_welcome_message")]
    ])

    await callback.message.answer(
        f"Siz tanladingiz: {choice.capitalize()}\nTo'lov summasi: {amount:,} UZS\n\n"
        "To'lovni amalga oshirish uchun tugmani bosing:",
        reply_markup=kb
    )
    await callback.answer()