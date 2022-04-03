from telegram import User as TelegramUser
from .user import User
from .datetime_utils import now
from .base_model import BaseModel
from playhouse.postgres_ext import (
    ForeignKeyField, CharField, DateTimeTZField, ArrayField, BooleanField
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
    active = BooleanField(default=True)

    @staticmethod
    def new_appeal(telegram_user: TelegramUser) -> 'Appeal':
        return Appeal(
            patient=telegram_user.id,
            problems=[]
        )

    class Meta:
        table_name = "appeal"
