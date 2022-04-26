import peeweedbevolve
from .user import User
from .appeal import Appeal
from .message import Message
from .base_model import db_client

db_client.evolve([User, Appeal, Message])
