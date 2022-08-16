from peewee import Node
from models import Appeal


def appeal_by_message_id_and_user_id_query(message_id: int, user_id: int) -> Node:
    return Appeal.select().where((Appeal.patient == user_id) & (Appeal.message_id == message_id) & (Appeal.active))
