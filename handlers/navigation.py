from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from config import PLANNERS, BUNDLE, OSNOVA 
from utils.messages import get_welcome_message
from keyboards import get_product_keyboard, get_bundle_keyboard, get_main_menu

router = Router(name="navigation")

@router.callback_query(F.data.startswith('show_'))
async def show_product(callback: CallbackQuery):
    key = callback.data.split('_')[1]
    product_data = BUNDLE if key == 'bundle' else PLANNERS.get(key)
    keyboard = get_bundle_keyboard() if key == 'bundle' else get_product_keyboard(key)

    if not product_data:
        return await callback.answer("Mahsulot topilmadi")

    # ВОЗВРАЩАЕМ MarkdownV2 для стилизации
    try:
        media = InputMediaPhoto(
            media=product_data['image_url'], 
            caption=product_data['description'],
            parse_mode="MarkdownV2" # Теперь это будет работать красиво
        )
        await callback.message.edit_media(media=media, reply_markup=keyboard)
    except Exception as e:
        # Если вдруг в тексте осталась неэкранированная точка, отправим как обычный текст
        await callback.message.answer(text=product_data['description'], reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "get_welcome_message")
async def back_to_welcome(callback: CallbackQuery):
    try:
        # ВОЗВРАЩАЕМ MarkdownV2 для главного меню
        media = InputMediaPhoto(
            media=OSNOVA['image_url'], 
            caption=OSNOVA['description'],
            parse_mode="MarkdownV2"
        )
        await callback.message.edit_media(media=media, reply_markup=get_main_menu())
    except Exception:
        await callback.message.answer_photo(
            photo=OSNOVA['image_url'], 
            caption=OSNOVA['description'], 
            parse_mode="MarkdownV2",
            reply_markup=get_main_menu()
        )
    await callback.answer()
