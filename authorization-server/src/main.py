from __future__ import annotations

import uvicorn
from fastapi import FastAPI, Form
from starlette.responses import RedirectResponse
from config import config
import json
import requests
import jwt
from models import User

app = FastAPI(
    title='Digital Studsovet Mental Health Bot',
    description='Digital Studsovet Mental Health Bot Authorization Server',
    version='1.0.0',
)

CLIENT_TOKEN = config['telegram']['client_token']
ADMIN_TOKEN = config['telegram']['admin_token']


@app.post('/')
async def callback_auth(
    access_token: str = Form(...),
    token_type: str = Form(...),
    expires_in: int = Form(...),
    state: int = Form(...)
):
    data = jwt.decode(access_token, options={"verify_signature": False})
    chat_id = state // 10
    bot = state % 10
    if bot == 1:
        TELEGRAM_API = f"https://api.telegram.org/bot{ADMIN_TOKEN}/"
        BOT_URL = config['telegram']['admin_url']
    elif bot == 0:
        TELEGRAM_API = f"https://api.telegram.org/bot{CLIENT_TOKEN}/"
        BOT_URL = config['telegram']['client_url']
    else:
        print("Bot id error.")
        return

    if User.select().where(User.telegram_id == chat_id).exists():
        user = User.get(User.telegram_id == chat_id)
        user.state = "Authorization"
        user.save(only=[User.state])
    elif User.select().where((User.hse_mail == data['email']) & (User.telegram_id == -1)).exists():
        user = User.get(User.hse_mail == data['email'])
        user.telegram_id = chat_id
        user.hse_mail=data['email']
        user.first_name=data['given_name']
        user.last_name=data['family_name']
        user.state="Authorization"
        user.save()
    else:
        user = User(
            telegram_id=chat_id,
            hse_mail=data['email'],
            first_name=data['given_name'],
            last_name=data['family_name'],
            state="Authorization"
        )
        user.save()
        


    text = """
    Мы нашли твой вышкинский аккаунт!
Пожалуйста, нажми кнопку <b>«Войти в бота»</b> для завершения регистрации.
"""

    reply_markup = json.dumps({
        "inline_keyboard": [
            [{"text": "Войти в бота", "callback_data": "auth_succesfull"}]
        ]
    })

    try:
        url = TELEGRAM_API + \
            f"sendMessage?text={text}&chat_id={chat_id}&parse_mode=HTML&reply_markup={reply_markup}"
        raw = requests.get(url)
        msg_id = raw.json()['result']['message_id']
        reply_markup = json.dumps({
            "inline_keyboard": [
                [{"text": "Войти в бота", "callback_data": f"auth_succesfull_{msg_id}"}]
            ]
        })
        url = TELEGRAM_API + \
            f"editMessageReplyMarkup?chat_id={chat_id}&message_id={msg_id}&reply_markup={reply_markup}"
        requests.get(url)
    except Exception as e:
        print(e)
        return
    return RedirectResponse(url=BOT_URL)


if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=config['fastapi'].get('port', 9097),
        debug=config['fastapi'].get('debug', False)
    )
