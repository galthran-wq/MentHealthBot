from models import Appeal, User, connection_types


def get_new_appeals() -> list[Appeal]:
    data = Appeal.select().where(Appeal.therapist==None)
    if data:
        new_appeals = []
        for appeal in data:
            user = User.get_by_id(appeal.patient_id)
            conn = connection_types.connections[appeal.connection_type]
            new_appeals.append((f"{user.first_name} {user.last_name}, {conn}", appeal.id))
        return new_appeals
    else:
        return []
    