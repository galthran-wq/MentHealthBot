from telegram.ext import MessageFilter
from models.models import User


class StateFilter(MessageFilter):
    def __init__(self, state: str):
        self.state = state

    def filter(self, message):
        if (user := User.select().where(User.telegram_id == message.from_user.id)).exists():
            user = user.get()
            return user.state == self.state
        else:
            return False
