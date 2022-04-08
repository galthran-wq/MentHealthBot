from .user_by_telegram_username import user_by_telegram_username


def add_admin_by_telegram_username(telegram_username: str):
    if user_by_telegram_username(telegram_username).exists():
        user = user_by_telegram_username(telegram_username).get()
        user.admin = True
        user.save()
    return None
