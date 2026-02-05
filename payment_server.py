import hashlib
import logging
from fastapi import FastAPI, Form
from aiogram import Bot
from typing import Dict, Any

# --- КОНФИГУРАЦИЯ (Твои данные) ---
BOT_TOKEN = '8118513719:AAFPxYxAf5uqmJEM-l7ho26q-8UMBoDancA'

CLICK_CONFIG = {
    'service_id': '94950',
    'merchant_id': '55254',
    'secret_key': 'ZlxY9xXrErDmTRb',
    'merchant_user_id': '77127',
}

PLANNERS: Dict[str, Dict[str, Any]] = {
    'financial': {
        'title': 'Moliya trekeri',
        'link': 'https://docs.google.com/spreadsheets/u/0/d/1ZuH-1hAW688AVW6GYfLHCAIFjiQGEa8lK5YZHsoxD8M/copy'
    },
    'task': {
        'title': 'Vazifa trekeri',
        'link': 'https://docs.google.com/spreadsheets/d/18yD2bVvdtTies8IaBiOu1O7lvXAENs3IaIT9x957Ago/copy'
    },
    'productivity': {
        'title': 'Hosildorlik trekeri',
        'link': 'https://docs.google.com/spreadsheets/d/1NHO1rvIF0fJSAgk0_HZEuE6n82AJ-AoNQB4fniD9jNU/copy'
    }
}

BUNDLE = {
    'title': 'Aksiya: 3 po cene 2',
    'planners': ['financial', 'task', 'productivity']
}

# --- ИНИЦИАЛИЗАЦИЯ ---
app = FastAPI()
bot = Bot(token=BOT_TOKEN)
logging.basicConfig(level=logging.INFO)

def check_click_signature(params: dict, sign_string: str) -> bool:
    """Проверка безопасности MD5 хеша"""
    payload = (
        f"{params.get('click_trans_id')}{params.get('service_id')}"
        f"{CLICK_CONFIG['secret_key']}{params.get('merchant_trans_id')}"
        f"{params.get('amount')}{params.get('action')}{params.get('sign_time')}"
    )
    my_hash = hashlib.md5(payload.encode()).hexdigest()
    return my_hash == sign_string

@app.post("/click/webhook")
async def click_webhook(
    click_trans_id: str = Form(...),
    service_id: str = Form(...),
    merchant_trans_id: str = Form(...),
    amount: str = Form(...),
    action: str = Form(...),
    error: str = Form(...),
    error_note: str = Form(...),
    sign_time: str = Form(...),
    sign_string: str = Form(...)
):
    params = {
        'click_trans_id': click_trans_id, 'service_id': service_id,
        'merchant_trans_id': merchant_trans_id, 'amount': amount,
        'action': action, 'sign_time': sign_time
    }

    # 1. Проверка подписи
    if not check_click_signature(params, sign_string):
        logging.error("Sign check failed!")
        return {"error": "-1", "error_note": "SIGN CHECK FAILED"}

    # 2. Логика PREPARE (Проверка существования заказа)
    if action == "0":
        return {
            "click_trans_id": click_trans_id,
            "merchant_trans_id": merchant_trans_id,
            "error": "0",
            "error_note": "Success"
        }

    # 3. Логика COMPLETE (Подтверждение оплаты)
    if action == "1":
        if error == "0":
            try:
                # merchant_trans_id приходит в формате "user_id:item_key"
                user_id, item_key = merchant_trans_id.split(':')
                
                # Собираем данные для сообщения
                if item_key == 'bundle':
                    title = BUNDLE['title']
                    links_list = [f"• {PLANNERS[p]['title']}:\n{PLANNERS[p]['link']}" for p in BUNDLE['planners']]
                    links_text = "\n\n".join(links_list)
                else:
                    product = PLANNERS.get(item_key)
                    title = product['title'] if product else "Treker"
                    links_text = product['link'] if product else "Havola topilmadi"

                # Текст сообщения об успехе
                success_message = (
                    f"✅ <b>To'lov muvaffaqiyatli qabul qilindi!</b>\n\n"
                    f"Mahsulot: <b>{title}</b>\n\n"
                    f"Sizning havolalaringiz:\n{links_text}\n\n"
                    f"<i>Eslatma: Havolani ochib 'Copy' (Nusxa olish) tugmasini bosing.</i>"
                )

                await bot.send_message(chat_id=user_id, text=success_message, parse_mode="HTML")
                logging.info(f"Sent success message to {user_id}")

                return {
                    "click_trans_id": click_trans_id,
                    "merchant_trans_id": merchant_trans_id,
                    "error": "0",
                    "error_note": "Success"
                }
            except Exception as e:
                logging.error(f"Error sending message: {e}")
                return {"error": "-5", "error_note": "User notification failed"}
        
        return {"error": error, "error_note": error_note}

    return {"error": "-9", "error_note": "Unknown action"}