from telegram import Message
from models import Appeal, User


def create_appeal(message: Message, user: User) -> Appeal:
    appeal = Appeal.from_message_and_user(message, user)
    appeal.save()
    return appeal
