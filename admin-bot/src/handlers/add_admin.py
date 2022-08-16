from telegram import Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.update_user_state import update_user_state
from utils.find_user_by_telegram_user import find_user_by_telegram_user
from states import UserStates
from utils.make_user_an_admin_by_email import make_user_an_admin_by_email
from utils.create_admin_by_email import create_admin_by_email
from .message_templates import ADD_ADMIN_MESSAGE, ADD_ADMIN_SUCCESS_MESSAGE, ADD_ADMIN_ERROR_MESSAGE


def add_admin_start(update: Update, context: CallbackContext):
    telegram_user = update.effective_user

    user = find_user_by_telegram_user(telegram_user)
    check_state(user.state, [UserStates.AUTHORIZED_ADMIN_STATE])
    update_user_state(user, UserStates.ADD_ADMIN_STATE)

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=ADD_ADMIN_MESSAGE,
    )


def add_admin(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user_by_telegram_user(telegram_user)
    admin_email = update.message.text

    if not make_user_an_admin_by_email(admin_email):
        create_admin_by_email(admin_email)

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=ADD_ADMIN_SUCCESS_MESSAGE,
    )
    update_user_state(user, UserStates.AUTHORIZED_ADMIN_STATE)
