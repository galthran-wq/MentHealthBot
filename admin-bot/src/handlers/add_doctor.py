from telegram import Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.update_user_state import update_user_state
from utils.find_user import find_user
from states import UserStates
from utils.user_by_telegram_username import user_by_telegram_username
from utils.add_doctor_by_telegram_username import add_doctor_by_telegram_username
from .message_templates import ADD_DOCTOR_MESSAGE, ADD_DOCTOR_SUCCESS_MESSAGE, ADD_DOCTOR_ERROR_MESSAGE


def add_doctor_start(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    check_state(user.state, [UserStates.AUTHORIZED_ADMIN_STATE])
    update_user_state(user, UserStates.ADD_DOCTOR_STATE)

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=ADD_DOCTOR_MESSAGE,
    )


def add_doctor(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    doctor_username = update.message.text[1:]

    if user_by_telegram_username(doctor_username):
        add_doctor_by_telegram_username(doctor_username)
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=ADD_DOCTOR_SUCCESS_MESSAGE,
        )
    else:
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=ADD_DOCTOR_ERROR_MESSAGE,
        )
    update_user_state(user, UserStates.AUTHORIZED_ADMIN_STATE)
