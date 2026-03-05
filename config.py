from typing import Dict, Any


BOT_TOKEN = '8118513719:AAHOtzF2EeW6uySSH0xIgiwfgax0skSrFuc'
PROVIDER_TOKEN = '333605228:LIVE:55254_6E6BFB0FBFB5D592A8E9CE3F19DE47B44451F844'
ADMIN_ID = [-5299954879, 892260845]

# Твои данные из вопроса
CLICK_CONFIG = {
    'service_id': '94950',
    'merchant_id': '55254',
    'secret_key': 'ZlxY9xXrErDmTRb',
    'merchant_user_id': '77127',
}

CURRENCY = 'UZS'

PLANNERS: Dict[str, Dict[str, Any]] = {
    'financial': {
        'title': 'Moliya trekeri',
        # Direct image URL recommended (i.imgur.com/....jpg/png) for Telegram
        'image_url': 'https://i.postimg.cc/DZtKQ4w4/Moliya.png',
        'description': (
            "*✦🗂️ Moliya trekeri✦*\n\n"
            "> Moliyalaringizni nazorat qiling va maqsadlaringizga erishing \\! "
            "Daromadlar, xarajatlar va investitsiyalarni bitta joyda hisobga oling\\.\n\n"
            "▪️*Narxi:* 69\\.000 UZS\n\n"
             "_Bir marta toʻlaysiz — cheklovlarsiz foydalanasiz_"
        ),
        'price': 69000,
        'link': 'https://docs.google.com/spreadsheets/u/0/d/1ZuH-1hAW688AVW6GYfLHCAIFjiQGEa8lK5YZHsoxD8M/copy'
    },
    'task': {
        'title': 'Vazifa trekeri',
        'image_url': 'https://i.postimg.cc/7ZpMkxhX/Vazifalar-planeri.png',
        'description': (
            "*✦☑️ Vazifa trekeri✦*\n\n"
            "> Vazifalaringiz va yutuqlaringizni vizualashtiring \\! "
            "Loyihalar va kundalik ishlarni boshqarish uchun ideal vosita\\.\n\n"
            "▪️*Narxi:* 69\\.000 UZS\n\n"
             "_Bir marta toʻlaysiz — cheklovlarsiz foydalanasiz_"
        ),
        'price': 69000,
        'link': 'https://docs.google.com/spreadsheets/d/18yD2bVvdtTies8IaBiOu1O7lvXAENs3IaIT9x957Ago/copy'
    },
    'productivity': {
        'title': 'Hosildorlik trekeri',
        'image_url': 'https://i.postimg.cc/jdpVGMG5/Planer-produktivnosti.png',
        'description': (
            "*✦📊 Hosildorlik trekeri✦*\n\n"
            "> Samaradorligingizni yuqori darajaga ko‘taring \\! "
            "Kun rejasini tuzing, odatlarni kuzatib boring va mahsuldorlikni tahlil qiling\\.\n\n"
            "▪️*Narxi:* 69\\.000 UZS\n\n"
             "_Bir marta toʻlaysiz — cheklovlarsiz foydalanasiz_"
        ),
        'price': 69000,
        'link': 'https://docs.google.com/spreadsheets/d/1NHO1rvIF0fJSAgk0_HZEuE6n82AJ-AoNQB4fniD9jNU/copy'
    }
}

BUNDLE = {
    'title': '2 ta puliga 3 ta oling',
    'image_url': 'https://i.postimg.cc/q7JswHcx/3st1.png',
    'description': (
        "*✦🔥 2 ta puliga 3 ta oling ✦*\n\n"
            "> Hozirdan foydalaning — bu imkoniyatni qo‘ldan boy bermang \\! "
            "Aksiya muddati cheklangan \\.\n\n"
            "▪️*Narxi:* 99\\.000 UZS\n\n"
             "_Bir marta toʻlaysiz — cheklovlarsiz foydalanasiz_"
    ),
    'price': 129000,
    'planners': ['financial', 'task', 'productivity']
}

OSNOVA = {
    'image_url': 'https://i.postimg.cc/1zjdL40t/Bez-imeni-3.png',
    'description': (
        "*Assalomu alaykum*\\!\n\n"
        "*✦ REJALAR ✦*\n\n"
        "> O‘z rivojlanishingizni vizual qiling va hayotingiz samaradorligini oshiring\\! "
        "Google Sheets uchun premium trekerlari bilan\\.\n\n"
        "*▪️ Trekerni tanlang : *"
    )
}
# Для проверки подписки (chat_id каналов)
REQUIRED_CHANNELS_IDS = [
    "-1001728474725",
    "-1002297752370"
]

# Для кнопок подписки (твои приватные invite-ссылки)
REQUIRED_CHANNELS_INVITE = [
    "https://t.me/+UFhJnCwuHRo2ODc6",
    "https://t.me/+oGhb7Mf2Ms03MmRi"
]
