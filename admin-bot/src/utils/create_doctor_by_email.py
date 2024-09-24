from models import User
from random import randint
from peewee import IntegrityError

def create_doctor_by_email(email: str):
    for i in [randint(-10000, -1) for _ in range(3)]:
        try:
            new_user = User(
                telegram_id = i,
                therapist=True,
                hse_mail=email
            )
            new_user.save()
        except IntegrityError:
            pass
        else:
            break


def create_doctor_by_telegram_username(telegram_username: str):
    for i in [randint(-10000, -1) for _ in range(3)]:
        try:
            new_user = User(
                telegram_id = i,
                therapist=True,
                telegram_username=telegram_username
            )
            new_user.save()
        except IntegrityError:
            pass
        else:
            break