from telegram import User
from .user_by_telegram_id_query import user_by_telegram_id_query


def check_admin(telegram_user: User):
    if user_by_telegram_id_query(telegram_user.id).exists():
        return user_by_telegram_id_query(telegram_user.id).get().admin
    return False
