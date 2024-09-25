from telegram import User
from .user_by_telegram_id_query import user_by_telegram_id_query, user_by_telegram_username_query


def check_admin(telegram_user: User):
    if user_by_telegram_username_query(telegram_user.username).exists():
        return user_by_telegram_username_query(telegram_user.username).get().admin
    return False
