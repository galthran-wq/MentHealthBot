from .user_by_telegram_username import user_by_telegram_username


def delete_admin_by_telegram_username(telegram_username: str):
    user = user_by_telegram_username(telegram_username).get()
    user.admin = False
    user.save()
