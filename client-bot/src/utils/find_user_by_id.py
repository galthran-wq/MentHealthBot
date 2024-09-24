from typing import Optional
from models import User
from peewee import Node
from telegram import User as TeleUser


def user_by_telegram_id_query(incoming_id: int) -> Node:
    return TeleUser.select().where(User.telegram_id == incoming_id)


def find_user_by_id(id: int) -> Optional[User]:
    return User.get_by_id(id)
