from peewee import Node
from models import User
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

def user_by_telegram_id_query(incoming_id: int) -> Node:
    return User.select().where(User.telegram_id == incoming_id)

def user_welcome_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user

    if user_by_telegram_id_query(telegram_user.id).exists():
        user = user_by_telegram_id_query(telegram_user.id).get()
    else:
        user = User.from_telegram_user(telegram_user)
        user.save()

    auth_button = InlineKeyboardButton(
        text="Авторизоваться (обман)",
        callback_data="fake_auth"
    )
    help_button = InlineKeyboardButton(
        text="Помогите...",
        callback_data="help_me"
    )

    kb = InlineKeyboardMarkup([[auth_button], [help_button]])

    msg = context.bot.send_message(
        chat_id=telegram_user.id,
        text="Приветствую тебя в боте помощи психологам! Бла-бла-бла",
        reply_markup=kb
    )
