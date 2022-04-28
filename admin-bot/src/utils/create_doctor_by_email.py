from models import User

def create_doctor_by_email(email: str):
    new_user = User(
        telegram_id = -1,
        therapist=True,
        hse_mail=email
    )
    new_user.save()
