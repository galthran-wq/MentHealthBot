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

TOKEN = config['telegram']['token']
TELEGRAM_API = "https://api.telegram.org/bot{}/".format(TOKEN)
BOT_URL = config['telegram']['url']


@app.post('/')
async def callback_auth(
    access_token: str = Form(...),
    token_type: str = Form(...),
    expires_in: int = Form(...),
    state: int = Form(...)
):
    data = jwt.decode(access_token, options={"verify_signature": False})
    chat_id = state

    if User.select().where(User.telegram_id == chat_id).exists():
        # todo сделать так, чтобы активные заявки пользователя удалялись
        pass
    else:
        user_dto = User(
            telegram_id=chat_id,
            hse_mail=data['email'],
            first_name=data['given_name'],
            last_name=data['family_name']
        )
        user_dto.save()

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
            f"sendMessage?text={text}&chat_id={chat_id}&parse_mode=HTML"
        if reply_markup:
            url += f"&reply_markup={reply_markup}"
        requests.get(url)
    except Exception as e:
        print(e)
    return RedirectResponse(url=BOT_URL)


if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=config['fastapi'].get('port', 9097),
        debug=config['fastapi'].get('debug', False)
    )
