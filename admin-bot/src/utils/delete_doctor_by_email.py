from .user_by_email import user_by_telegram_username, user_by_email


def delete_doctor_by_email(email: str) -> bool:
    if user_by_email(email).exists():
        user = user_by_email(email).get()
        user.therapist = False
        user.save()
        return True
    else:
        return False

def delete_doctor_by_telegram_username(telegram_username: str) -> bool:
    if user_by_telegram_username(telegram_username).exists():
        user = user_by_telegram_username(telegram_username).get()
        user.therapist = False
        user.save()
        return True
    else:
        return False
