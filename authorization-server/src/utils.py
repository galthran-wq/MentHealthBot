import httpx
import json
import jwt
import time
from async_lru import alru_cache


async def send_message(text: str, chat_id: int, token: str, reply_markup: dict = None):
    TELEGRAM_API = f'https://api.telegram.org/bot{token}/'
    url = TELEGRAM_API + f'sendMessage?text={text}&chat_id={chat_id}&parse_mode=HTML'
    if reply_markup:
        url += f'&reply_markup={json.dumps(reply_markup)}'
    async with httpx.AsyncClient() as client:
        return await client.get(url)

@alru_cache(maxsize=1)
async def _get_jwks(ttl_hash):
    async with httpx.AsyncClient() as client:
        jwks = (await client.get('https://auth.hse.ru/adfs/discovery/keys')).json()
    public_keys = {}
    for jwk in jwks['keys']:
        kid = jwk['kid']
        public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    return public_keys


async def get_jwks():
    return await _get_jwks(ttl_hash=round(time.monotonic() / 86400))
