from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.types import InputMediaPhoto

from config import PLANNERS, BUNDLE
from utils.messages import get_welcome_message
from keyboards import get_product_keyboard, get_bundle_keyboard, get_main_menu

router = Router(name="navigation")



@router.callback_query(F.data.startswith('show_'))
async def show_product(callback: CallbackQuery):
    key = callback.data.split('_')[1]

    if key == 'bundle':
        product_data = BUNDLE
        keyboard = get_bundle_keyboard()
    else:
        product_data = PLANNERS.get(key)
        keyboard = get_product_keyboard(key)

    if not product_data:
        return await callback.answer("Mahsulot topilmadi")

    text = product_data['description']
    image_url = product_data.get('image_url')

    try:
        # Пытаемся обновить сообщение с новым фото
        media = InputMediaPhoto(media=image_url, caption=text, parse_mode="MarkdownV2")
        await callback.message.edit_media(media=media, reply_markup=keyboard)
    except Exception as e:
        print(f"Rasm yuklashda xato ({key}): {e}")
        # Если фото не грузится (wrong type of content), просто отправляем текст
        try:
            await callback.message.answer(text=text, parse_mode="MarkdownV2", reply_markup=keyboard)
            await callback.message.delete()
        except Exception as e2:
            # Если даже текст не шлется, значит ошибка в Markdown символах
            print(f"Markdown xatosi: {e2}")
            await callback.message.answer(text="Tavsifda formatlash xatosi bor.")
    
    await callback.answer()


from aiogram.types import InputMediaPhoto
from config import OSNOVA  # ← добавь импорт, если его нет

@router.callback_query(F.data == "get_welcome_message")
async def back_to_welcome(callback: CallbackQuery):
    media = InputMediaPhoto(
        media=OSNOVA['image_url'],
        caption=OSNOVA['description'],
        parse_mode="MarkdownV2"
    )

    try:
        await callback.message.edit_media(
            media=media,
            reply_markup=get_main_menu()
        )
    except Exception as e:
        print(f"edit_media failed: {e}")  # ← для отладки в консоли
        # Если edit_media не сработал (например, сообщение было текстом, а не фото) — отправляем новое фото
        await callback.message.answer_photo(
            photo=OSNOVA['image_url'],
            caption=OSNOVA['description'],
            parse_mode="MarkdownV2",
            reply_markup=get_main_menu()
        )
        try:
            await callback.message.delete()  # чистим старое, чтобы не мусорить
        except Exception:
            pass

    await callback.answer()


@router.message(F.text)
async def on_home_reply(message: Message):
    """
    Handles the reply-keyboard button "🏠 Bosh saxifaga" which sends plain text.
    This restores the welcome screen + main menu when the user taps that button.
    """
    text_value = (message.text or "").strip().lower()
    if text_value in ("🏠 bosh saxifaga", "bosh saxifaga", "вернуться в начало", "вернуться в начало."):
        await message.answer(
            get_welcome_message(),
            reply_markup=get_main_menu()
        )
