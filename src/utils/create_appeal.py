from telegram import Update
from models import Appeal, User


def create_appeal(update: Update, user: User) -> Appeal:
    appeal = Appeal.from_update_and_user(update, user)
    appeal.save()
    return appeal
