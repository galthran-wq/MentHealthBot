from telegram import Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.update_user_state import update_user_state
from utils.find_user import find_user
from states import UserStates
from utils.check_admin import check_admin
from utils.user_by_telegram_username import user_by_telegram_username
from utils.add_admin_by_telegram_username import add_admin_by_telegram_username
from .message_templates import ADD_ADMIN_MESSAGE, ADD_ADMIN_SUCCESS_MESSAGE, ADD_ADMIN_ERROR_MESSAGE


def add_admin_start(update: Update, context: CallbackContext):
    telegram_user = update.effective_user

    user = find_user(telegram_user)
    check_state(user.state, [UserStates.AUTHORIZED_ADMIN_STATE])
    update_user_state(user, UserStates.ADD_ADMIN_STATE)

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=ADD_ADMIN_MESSAGE,
    )


def add_admin(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    admin_username = update.message.text[1:]

    if user_by_telegram_username(admin_username):
        add_admin_by_telegram_username(admin_username)
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=ADD_ADMIN_SUCCESS_MESSAGE,
        )
    else:
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=ADD_ADMIN_ERROR_MESSAGE,
        )
    update_user_state(user, UserStates.AUTHORIZED_ADMIN_STATE)
