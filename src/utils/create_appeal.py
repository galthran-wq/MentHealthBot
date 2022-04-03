from telegram import User
from models import Appeal


def create_appeal(telegram_user: User) -> Appeal:
    appeal = Appeal.from_telegram_user(telegram_user)
    appeal.save()
    return appeal
