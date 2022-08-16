from models import User


def user_by_email(incoming_email: str):
    return User.select().where(User.hse_mail == incoming_email)
