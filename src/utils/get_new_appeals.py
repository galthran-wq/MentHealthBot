from models import Appeal, User


def get_new_appeals() -> list[Appeal]:
    data = Appeal.select().where(Appeal.therapist==None)
    if data:
        new_appeals = []
        for appeal in data:
            user = User.get_by_id(appeal.patient_id)
            #todo: change appearance of connection_type to user-friendly
            new_appeals.append((f"{user.first_name} {user.last_name}, {appeal.connection_type}", appeal.id))
        return new_appeals
    else:
        return []
    