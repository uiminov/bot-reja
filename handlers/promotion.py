import asyncio
from aiogram import Router, Bot, F
from aiogram.types import LabeledPrice, Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from config import PROVIDER_TOKEN, CURRENCY, ADMIN_ID
from utils.db import get_all_users
from promotion_templates import PROMOTIONS

router = Router(name="promotion")


async def send_promotion_with_invoice(
    bot: Bot,
    user_id: int,
    text: str,
    title: str,
    description: str,
    amount: int,
    payload: str,
    image_url: str = None,
    parse_mode: str = "Markdown"
):
    """
    Отправляет текст акции отдельным сообщением, затем инвойс
    """
    
    # 1. Отправляем текстовое сообщение с акцией (с отступами и форматированием)
    await bot.send_message(
        chat_id=user_id,
        text=text,
        parse_mode=parse_mode
    )
    
    # 2. Формируем цену
    prices = [LabeledPrice(label=title, amount=int(amount * 100))]
    
    # 3. Отправляем инвойс отдельно
    # Проверяем что description не пустое
    invoice_description = description if description and description.strip() else title
    
    await bot.send_invoice(
        chat_id=user_id,
        title=title,
        description=invoice_description,
        payload=payload,
        provider_token=PROVIDER_TOKEN,
        currency=CURRENCY,
        prices=prices,
        photo_url=image_url,
        photo_size=512,
        photo_width=512,
        photo_height=280,
        start_parameter="promotion_payment",
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        is_flexible=False
    )


@router.message(Command("sendpromo"))
async def promo_menu(message: Message):
    """Главное меню выбора акции"""
    
    # Проверяем админ ли
    if message.from_user.id not in ADMIN_ID:
        return await message.answer("❌ Только администратор может отправлять акции")
    
    # Создаем кнопки с готовыми акциями
    buttons = []
    for promo_id, promo_data in PROMOTIONS.items():
        buttons.append([
            InlineKeyboardButton(
                text=promo_data['title'],
                callback_data=f"send_promo_{promo_id}"
            )
        ])
    
    # Добавляем кнопку для создания своей акции
    buttons.append([
        InlineKeyboardButton(text="💬 Отправить сообщение", callback_data="send_broadcast")
    ])
    
    # Добавляем кнопку для свободного сообщения
    buttons.append([
        InlineKeyboardButton(text="✏️ Свободное сообщение", callback_data="send_free_message")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await message.answer(
        "*📢 Выбери акцию для отправки:*\n\n"
        "Нажми на одну из готовых или создай свою",
        parse_mode="Markdown",
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith("send_promo_"))
async def send_ready_promo(callback: CallbackQuery, bot: Bot):
    """Отправка готовой акции"""
    
    promo_id = callback.data.split("_", 2)[2]
    
    if promo_id not in PROMOTIONS:
        return await callback.answer("❌ Акция не найдена", show_alert=True)
    
    promo = PROMOTIONS[promo_id]
    
    # Показываем превью перед отправкой
    preview_text = f"*Превью:*\n\n{promo['text']}"
    
    buttons = [
        [
            InlineKeyboardButton(text="✅ Отправить", callback_data=f"confirm_promo_{promo_id}"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_promo")
        ]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(
        preview_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_promo_"))
async def confirm_and_send(callback: CallbackQuery, bot: Bot):
    """Подтверждение и отправка акции"""
    
    promo_id = callback.data.split("_", 2)[2]
    promo = PROMOTIONS[promo_id]
    
    try:
        # Получаем всех пользователей
        users = await get_all_users()
        
        if not users:
            return await callback.answer("❌ Нет пользователей для отправки", show_alert=True)
        
        # Отправляем акцию каждому пользователю
        success_count = 0
        failed_count = 0
        
        await callback.message.edit_text(
            "⏳ *Отправка акции...*",
            parse_mode="Markdown"
        )
        
        for user_id in users:
            try:
                await send_promotion_with_invoice(
                    bot=bot,
                    user_id=user_id,
                    text=promo['text'],
                    title=promo['title'],
                    description=promo['description'],
                    amount=promo['price'],
                    payload=promo_id,
                    image_url=promo.get('image_url'),
                    parse_mode="Markdown"
                )
                success_count += 1
            except Exception as e:
                print(f"Ошибка при отправке пользователю {user_id}: {e}")
                failed_count += 1
        
        # Отправляем отчет
        report = (
            f"✅ *Рассылка завершена*\n\n"
            f"✔️ Отправлено: {success_count}\n"
            f"❌ Ошибок: {failed_count}\n"
            f"📊 Всего: {success_count + failed_count}"
        )
        
        await callback.message.edit_text(report, parse_mode="Markdown")
        
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}", show_alert=True)


@router.callback_query(F.data == "cancel_promo")
async def cancel_promo(callback: CallbackQuery):
    """Отмена отправки"""
    await callback.message.delete()
    await callback.answer("❌ Отменено", show_alert=False)


@router.callback_query(F.data == "send_broadcast")
async def broadcast_start(callback: CallbackQuery):
    """Инструкция по отправке сообщения всем"""
    
    await callback.message.delete()
    await callback.answer()
    
    await callback.message.answer(
        "💬 *Отправка сообщения всем пользователям*\n\n"
        "Используй команду:\n"
        "`/sendall Твой текст`\n\n"
        "Пример:\n"
        "`/sendall Привет! Это новая акция`",
        parse_mode="Markdown"
    )


@router.callback_query(F.data == "send_free_message")
async def free_message_start(callback: CallbackQuery):
    """Инструкция по отправке свободного сообщения"""
    
    await callback.message.delete()
    await callback.answer()
    
    await callback.message.answer(
        "✏️ *Свободное сообщение*\n\n"
        "Используй команду:\n"
        "`/sendfree Твой текст`\n\n"
        "Пример:\n"
        "`/sendfree Привет всем!`",
        parse_mode="Markdown"
    )


@router.message(Command("sendall"))
async def sendall_command(message: Message):
    """Простой обходной путь: /sendall текст — рассылка без FSM (только для админов)"""
    if message.from_user.id not in ADMIN_ID:
        return await message.answer("❌ Только администратор может использовать эту команду")

    # Парсим текст после команды
    text = message.text.replace("/sendall", "").strip()
    if not text:
        return await message.answer("❌ Укажи текст после команды, например:\n/sendall Тест рассылки")

    users = await get_all_users()
    if not users:
        return await message.answer("❌ Нет пользователей в базе")

    sent = 0
    status = await message.answer(f"⏳ Начинаю рассылку на {len(users)} пользователей...")
    for uid in users:
        try:
            await message.bot.send_message(chat_id=uid, text=text, parse_mode="Markdown")
            sent += 1
        except Exception as e:
            # Если Markdown не сработал, отправляем как обычный текст
            try:
                await message.bot.send_message(chat_id=uid, text=text)
                sent += 1
            except Exception as e2:
                print(f"[SENDALL] Ошибка при отправке {uid}: {e2}")
        await asyncio.sleep(0.05)

    await status.edit_text(f"✅ Готово! Доставлено: {sent}/{len(users)}")


@router.message(Command("sendfree"))
async def sendfree_command(message: Message):
    """Отправка свободного сообщения всем пользователям (только для админов)"""
    if message.from_user.id not in ADMIN_ID:
        return await message.answer("❌ Только администратор может использовать эту команду")

    # Парсим текст после команды
    text = message.text.replace("/sendfree", "").strip()
    if not text:
        return await message.answer("❌ Укажи текст после команды, например:\n/sendfree Привет всем!")

    users = await get_all_users()
    if not users:
        return await message.answer("❌ Нет пользователей в базе")

    sent = 0
    status = await message.answer(f"⏳ Начинаю рассылку на {len(users)} пользователей...")
    for uid in users:
        try:
            await message.bot.send_message(chat_id=uid, text=text, parse_mode="Markdown")
            sent += 1
        except Exception as e:
            # Если Markdown не сработал, отправляем как обычный текст
            try:
                await message.bot.send_message(chat_id=uid, text=text)
                sent += 1
            except Exception as e2:
                print(f"[SENDFREE] Ошибка при отправке {uid}: {e2}")
        await asyncio.sleep(0.05)

    await status.edit_text(f"✅ Готово! Доставлено: {sent}/{len(users)}")

