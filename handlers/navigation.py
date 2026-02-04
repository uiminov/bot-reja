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
        text = BUNDLE['description']
        image_url = BUNDLE.get('image_url')
        keyboard = get_bundle_keyboard()
    else:
        text = PLANNERS[key]['description']
        image_url = PLANNERS[key].get('image_url')
        keyboard = get_product_keyboard(key)

    # Prefer rendering as photo + caption (as requested). Fallback to plain text if no image_url.
    if image_url:
        media = InputMediaPhoto(media=image_url, caption=text, parse_mode="MarkdownV2")
        try:
            await callback.message.edit_media(media=media, reply_markup=keyboard)
        except Exception:
            # If current message is not editable into media (e.g., text message), send a new photo.
            await callback.message.answer_photo(
                photo=image_url,
                caption=text,
                parse_mode="MarkdownV2",
                reply_markup=keyboard
            )
            try:
                await callback.message.delete()
            except Exception:
                pass
    else:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="MarkdownV2")
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
