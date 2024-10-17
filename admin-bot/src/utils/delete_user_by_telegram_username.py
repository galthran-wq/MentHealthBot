import logging

from utils.user_by_telegram_username import user_by_telegram_username
from models import User

def delete_user_by_telegram_username(telegram_username: str) -> bool:
    user_ref = user_by_telegram_username(telegram_username)
    if user_ref:
        try:
            q = User.delete().where(
                User.telegram_username == telegram_username 
            )
            q.execute()
        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            return False
        return True
    else:
        return False
