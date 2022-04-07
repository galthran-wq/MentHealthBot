from models import User
from models import Appeal


def find_appeals_by_doctor_id(therapist: User) -> list[str]:
    db_rows = Appeal.select().where(Appeal.therapist == therapist.id)
    if db_rows:
        appeals = []
        for appeal in db_rows:
            user = User.get_by_id(appeal.patient_id)
            appeals.append(f"{user.first_name} {user.last_name}")
        return appeals
    else:
        return []
