from models import User

def create_admin_by_email(email: str):
    new_user = User(
        telegram_id = -1,
        admin=True,
        hse_mail=email
    )
    new_user.save()


def create_admin_by_telegram_username(telegram_username: str):
    new_user = User(
        telegram_id = -1,
        admin=True,
        telegram_username=telegram_username
    )
    new_user.save()