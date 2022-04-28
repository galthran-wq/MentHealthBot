from models import User

def create_admin_by_email(email: str):
    new_user = User(
        telegram_id = -1,
        admin=True,
        hse_mail=email
    )
    new_user.save()
