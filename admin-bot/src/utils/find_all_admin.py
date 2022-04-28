from peewee import Node
from models import User


def find_all_admin() -> Node:
    return User.select().where(User.admin == True)
