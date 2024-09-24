from .user import User
from .datetime_utils import now
from .base_model import BaseModel
from playhouse.postgres_ext import (
    ForeignKeyField, CharField, DateTimeTZField
)

class Message(BaseModel):
    user = ForeignKeyField(
        backref="messages", column_name="user_id",
        field="id", model=User, null=True
    )
    text = CharField(null=False, max_length=255)
    direction = CharField(null=False)
    json_string = CharField(null=True, max_length=100000)
    message_id = CharField(index=True, null=True, max_length=100)
    sent_at = DateTimeTZField(index=True, default=now)

    class Meta:
        table_name = "message"
