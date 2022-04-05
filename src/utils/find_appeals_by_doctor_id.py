from models import User
from models import Appeal


def find_appeals_by_doctor_id(therapist: User) -> list[Appeal]:
    data = Appeal.select().where(Appeal.therapist == therapist.id)
    if data:
        appeals = []
        for appeal in data:
            user = User.get_by_id(appeal.patient_id)
            appeals.append(f"{user.first_name} {user.last_name}")
        return appeals
    else:
        return []