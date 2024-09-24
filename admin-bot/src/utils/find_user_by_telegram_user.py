from typing import Optional
from models import User as BotUser
from telegram import User
from .user_by_telegram_id_query import user_by_telegram_id_query, user_by_telegram_username_query


def find_user_by_telegram_user(telegram_user: User) -> Optional[BotUser]:
    if user_by_telegram_username_query(telegram_user.username).exists():
        return user_by_telegram_username_query(telegram_user.username).get()
    return None
