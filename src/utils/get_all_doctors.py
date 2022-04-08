from models import User


def get_all_doctors() -> list[User.telegram_id]:
    db_strings = User.select().where(User.therapist == True)
    if db_strings:
        therapists = [therapist.telegram_id for therapist in db_strings]
        return therapists
    else:
        return []
