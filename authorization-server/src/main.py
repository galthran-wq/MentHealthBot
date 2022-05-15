from __future__ import annotations

import uvicorn
from fastapi import FastAPI, Form
from starlette.responses import RedirectResponse
from config import config
import jwt
from models import User
from utils import send_message, get_jwks

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
    try:
        jwks = await get_jwks()
        kid = jwt.get_unverified_header(access_token)['kid']
        data = jwt.decode(access_token,
                            key=jwks[kid],
                            algorithms=['RS256'],
                            audience='microsoft:identityserver:'+config['oauth']['appid'])
        if data['email'].split('@')[-1] not in ('edu.hse.ru', 'hse.ru'):
                text = 'Ваша почта должна быть в домене @edu.hse.ru или @hse.ru'
                markup = None
                print(f"{state}: bad email {data['email']}")
                raise ValueError
        chat_id = state // 10
        bot = state % 10
        if bot == 1:
            TG_TOKEN = ADMIN_TOKEN
            BOT_URL = config['telegram']['admin_url']
        elif bot == 0:
            TG_TOKEN = CLIENT_TOKEN
            BOT_URL = config['telegram']['client_url']
        else:
            print("Bot id error.")
            return

        if User.select().where(User.telegram_id == chat_id).exists():
            user = User.get(User.telegram_id == chat_id)
            user.state = "Authorization"
            user.save(only=[User.state])
        elif User.select().where((User.hse_mail == data['email']) & (User.telegram_id < 0)).exists():
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

        reply_markup = {
            "inline_keyboard": [
                [{"text": "Войти в бота", "callback_data": "auth_succesfull"}]
            ]
        }


        raw = await send_message(text=text, chat_id=chat_id, token=TG_TOKEN, reply_markup=reply_markup)
        msg_id = raw.json()['result']['message_id']
        reply_markup ={
            "inline_keyboard": [
                [{"text": "Войти в бота", "callback_data": f"auth_succesfull_{msg_id}"}]
            ]
        }
        await send_message(text=text, chat_id=chat_id, token=TG_TOKEN, reply_markup=reply_markup)
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
