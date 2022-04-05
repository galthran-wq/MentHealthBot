
from telegram import User
from models import User as BotUser
from .find_user_by_telegram_id_query import user_by_telegram_id_query


def find_or_create_user(telegram_user: User) -> BotUser:
    if user_by_telegram_id_query(telegram_user.id).exists():
        user = user_by_telegram_id_query(telegram_user.id).get()
    else:
        user = BotUser.from_telegram_user(telegram_user)
        user.save()
    return user
