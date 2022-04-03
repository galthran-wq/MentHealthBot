from __future__ import annotations

import uvicorn
from fastapi import FastAPI, Form
from starlette.responses import RedirectResponse
from config import config
import json
import requests
import jwt
from models import db_client, User

app = FastAPI(
    title='Digital Studsovet Mental Health Bot',
    description='Digital Studsovet Mental Health Bot Authorization Server',
    version='1.0.0',
)

items = [['Получить VPN']]
reply_markup = json.dumps(
    {
        "inline_keyboard": [
            [{"text": "Далее", "callback_data": "auth_succesfull"}]
        ]
    }
)
TOKEN = config['telegram']['token']

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
        return

    user_dto = User(
        telegram_id = chat_id,
        hse_mail=data['email'],
        first_name=data['firstname'],
        last_name=data['lastname']
    )
    user_dto.save()

    text = f"""
    Успешная авторизация!

    Вас зовут: {data['commonname']}
    Ваша почта: {data['email']}

    <b>Пожалуйста выберите на клавиатуре кнопку 'Получить VPN'</b>
    """
    try:
        TELEGRAM_API = "https://api.telegram.org/bot{}/".format(TOKEN)
        url = TELEGRAM_API
        + "sendMessage?text={}&chat_id={}&parse_mode=HTML".format(text, chat_id)
        if reply_markup:
            url += "&reply_markup={}".format(reply_markup)
        requests.get(url)
    except Exception as e:
        print(e)
    return RedirectResponse(url='https://t.me/MentalHealthHseTestBot')


if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=config['fastapi'].get('port', 9097),
        debug=config['fastapi'].get('debug', False)
    )
