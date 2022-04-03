from typing import Optional
from models import User
from models import Appeal
from .appeal_by_telegram_id_query import appeal_by_user_id_query


def find_appeal(user: User) -> Optional[Appeal]:
    if appeal_by_user_id_query(user.id).exists():
        return appeal_by_user_id_query(user.id).get()
    return None
