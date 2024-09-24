from typing import Optional
from models import User as BotUser
from telegram import User
from .user_by_telegram_id_query import user_by_telegram_id_query


def find_user(telegram_user: User) -> Optional[BotUser]:
    if user_by_telegram_id_query(telegram_user.id).exists():
        return user_by_telegram_id_query(telegram_user.id).get()
    return None
