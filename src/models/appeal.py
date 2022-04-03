from .user import User
from .datetime_utils import now
from .base_model import BaseModel
from playhouse.postgres_ext import (
    ForeignKeyField, CharField, BooleanField, DateTimeTZField, ArrayField
)

class Appeal(BaseModel):
    patient = ForeignKeyField(
        backref="appeals", column_name="patient_id", model=User, null=False
    )
    therapist = ForeignKeyField(
        backref="appeals", column_name="therapist_id", model=User, null=True
    )
    created_at = DateTimeTZField(index=True, default=now)
    connection_type = CharField(null=True, max_length=100)
    language = CharField(null=True)
    problems = ArrayField(CharField)

    class Meta:
        table_name = "appeal"
