from peewee import Node
from models import User


def find_all_doctor() -> Node:
    return User.select().where(User.therapist == True)
