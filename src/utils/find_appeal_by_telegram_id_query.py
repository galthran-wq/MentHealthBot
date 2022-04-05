from peewee import Node
from models import Appeal


def appeal_by_user_id_query(incoming_id: int) -> Node:
    return Appeal.select().where((Appeal.patient == incoming_id) & (Appeal.active))
