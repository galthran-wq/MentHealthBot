from models import User
from random import randint
from peewee import IntegrityError

def create_admin_by_email(email: str):
    new_user = User(
        telegram_id = -1,
        admin=True,
        hse_mail=email
    )
    new_user.save()


def create_admin_by_telegram_username(telegram_username: str):
    for i in [randint(-10000, -1) for _ in range(3)]:
        try:
            new_user = User(
                telegram_id = i,
                admin=True,
                telegram_username=telegram_username
            )
            new_user.save()
        except IntegrityError:
            pass
        else:
            break