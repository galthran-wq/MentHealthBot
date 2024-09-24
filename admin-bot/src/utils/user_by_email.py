from models import User


def user_by_email(incoming_email: str):
    return User.select().where(User.hse_mail == incoming_email)

def user_by_telegram_username(telegram_username: str):
    return User.select().where(User.telegram_username == telegram_username)
