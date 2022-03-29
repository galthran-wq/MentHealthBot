from .user import User
from .appeal import Appeal
from .message import Message
from .base_model import db_client
import peeweedbevolve

db_client.evolve()