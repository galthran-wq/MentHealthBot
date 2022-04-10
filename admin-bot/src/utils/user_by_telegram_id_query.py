from peewee import Node
from models import User


def user_by_telegram_id_query(incoming_id: int) -> Node:
    return User.select().where(User.telegram_id == incoming_id)
