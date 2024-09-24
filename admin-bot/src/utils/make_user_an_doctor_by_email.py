from .user_by_email import user_by_email, user_by_telegram_username


def make_user_an_doctor_by_email(email: str) -> bool:
    if user_by_email(email).exists():
        user = user_by_email(email).get()
        user.therapist = True
        user.save()
        return True
    else:
        return False


def make_user_an_doctor_by_telegram_username(telegram_username: str) -> bool:
    if user_by_telegram_username(telegram_username).exists():
        user = user_by_telegram_username(telegram_username).get()
        user.therapist = True
        user.save()
        return True
    else:
        return False