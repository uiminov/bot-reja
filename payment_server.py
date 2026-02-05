import hashlib
from fastapi import FastAPI, Form, Request
from aiogram import Bot
from config import BOT_TOKEN, CLICK_CONFIG
from utils.messages import get_success_message

app = FastAPI()
bot = Bot(token=BOT_TOKEN)

def check_click_signature(params: dict, sign_string: str) -> bool:
    """Проверка безопасности: совпадает ли хеш запроса с нашим секретным ключом."""
    # Порядок склейки строго по документации CLICK
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
        return {"error": "-1", "error_note": "SIGN CHECK FAILED"}

    # 2. Логика PREPARE (Action = 0)
    if action == "0":
        # Здесь можно добавить проверку: существует ли товар в PLANNERS
        return {
            "click_trans_id": click_trans_id,
            "merchant_trans_id": merchant_trans_id,
            "error": "0",
            "error_note": "Success"
        }

    # 3. Логика COMPLETE (Action = 1)
    if action == "1":
        if error == "0":
            # Разбираем merchant_trans_id (мы его создали как "user_id:item_key")
            try:
                user_id, item_key = merchant_trans_id.split(':')
                
                # Отправляем сообщение об успехе
                text = get_success_message(item_key)
                await bot.send_message(chat_id=user_id, text=text)

                return {
                    "click_trans_id": click_trans_id,
                    "merchant_trans_id": merchant_trans_id,
                    "error": "0",
                    "error_note": "Success"
                }
            except Exception as e:
                return {"error": "-5", "error_note": f"User notification failed: {e}"}
        
        return {"error": error, "error_note": error_note}

    return {"error": "-9", "error_note": "Unknown action"}