from models import User


def user_by_telegram_username(incoming_username: str):
    return User.select().where(User.telegram_username == incoming_username)
