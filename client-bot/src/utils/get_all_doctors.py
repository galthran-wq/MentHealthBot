from models import User


def get_all_doctors() -> list[User.telegram_id]:
    db_rows = User.select().where(User.therapist)
    if db_rows:
        therapists = [therapist.telegram_id for therapist in db_rows]
        return therapists
    else:
        return []
