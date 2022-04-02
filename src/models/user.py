from .base_model import BaseModel
from .datetime_utils import now
from telegram import User as TelegramUser
from playhouse.postgres_ext import (
    BigAutoField, BigIntegerField, CharField, BooleanField, DateTimeTZField
)

class User(BaseModel):
    id = BigAutoField()

    telegram_id = BigIntegerField(index=True, unique=True, null=False)
    telegram_username = CharField(null=True, max_length=100)

    admin = BooleanField(default=False, null=False)
    therapist = BooleanField(default=False, null=False)

    last_name = CharField(null=True, max_length=100)
    first_name = CharField(null=True, max_length=100)

    hse_mail = CharField(null=True, max_length=100)
    blocked_bot = BooleanField(default=False)

    joined_on = DateTimeTZField(default=now)
    last_seen_at = DateTimeTZField(default=now)

    state = CharField(default="started", max_length=100)

    @staticmethod
    def from_telegram_user(telegram_user: TelegramUser) -> 'User':
        return User(
            telegram_id=telegram_user.id,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            telegram_username=telegram_user.username
        )

    class Meta:
        table_name = "bot_user"
