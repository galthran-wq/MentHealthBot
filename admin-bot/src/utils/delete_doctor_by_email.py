from .user_by_email import user_by_email


def delete_doctor_by_email(email: str) -> bool:
    if user_by_email(email).exists():
        user = user_by_email(email).get()
        user.therapist = False
        user.save()
        return True
    else:
        return False
