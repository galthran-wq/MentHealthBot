from models import Appeal, User, connection_types


def get_new_appeals() -> list[(str, int)]:
    db_strings = Appeal.select().where((Appeal.therapist is None) & (Appeal.active) & (not Appeal.connection_type is None))
    if db_strings:
        new_appeals = []
        for appeal in db_strings:
            user = User.get_by_id(appeal.patient_id)
            try:
                conn = connection_types.CONNECTION_TYPES[appeal.connection_type]
            except KeyError:
                conn = "способ не указан"
            new_appeals.append((f"{user.first_name} {user.last_name}, {conn}", appeal.id))
        return new_appeals
    else:
        return []
        