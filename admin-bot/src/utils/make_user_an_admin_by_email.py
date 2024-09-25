import logging
from .user_by_email import user_by_email, user_by_telegram_username


def make_user_an_admin_by_email(email: str) -> bool:
    if user_by_email(email).exists():
        user = user_by_email(email).get()
        user.admin = True
        user.save()
        return True
    else:
        return False

def make_user_an_admin_by_telegram_username(telegram_username: str) -> bool:
    if user_by_telegram_username(telegram_username).exists():
        user = user_by_telegram_username(telegram_username).get()
        logging.info(f"Making User(id={user.id}, username={user.telegram_username}, state={user.state}) and admin.")
        user.admin = True
        user.save()
        return True
    else:
        return False
