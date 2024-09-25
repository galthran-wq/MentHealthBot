from telegram import Message
from telegram.ext import MessageFilter
from models import User
from states import UserStates


class StateFilter(MessageFilter):
    def __init__(self, state: UserStates):
        self.state = state

    def filter(self, message: Message) -> bool:
        if (user := User.select().where(User.telegram_username == message.from_user.username)).exists():
            user = user.get()
            return user.state == self.state
        else:
            return False
