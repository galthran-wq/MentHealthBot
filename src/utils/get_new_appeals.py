from models import Appeal, User, connection_types


def get_new_appeals() -> list[(str, int)]:
    db_strings = Appeal.select().where((Appeal.therapist == None) & (Appeal.active == True) & (Appeal.connection_type != None))
    if db_strings:
        new_appeals = []
        for appeal in db_strings:
            user = User.get_by_id(appeal.patient_id)
            conn = connection_types.CONNECTION_TYPES[appeal.connection_type]
            new_appeals.append((f"{user.first_name} {user.last_name}, {conn}", appeal.id))
        return new_appeals
    return []
