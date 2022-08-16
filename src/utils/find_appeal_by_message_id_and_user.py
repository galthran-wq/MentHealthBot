from typing import Optional
from models import User
from models import Appeal
from .find_appeal_by_telegram_id_query import appeal_by_message_id_and_user_id_query


def find_appeal_by_message_id_and_user(message_id: int, user: User) -> Optional[Appeal]:
    query = appeal_by_message_id_and_user_id_query(message_id, user.id)
    if query.exists():
        return query.get()
    return None
