from utils.user_by_telegram_username import user_by_telegram_username

def delete_user_by_telegram_username(telegram_username: str) -> bool:
    user_ref = user_by_telegram_username(telegram_username)
    if user_ref:
        user_ref.delete()
        return True
    else:
        return False
