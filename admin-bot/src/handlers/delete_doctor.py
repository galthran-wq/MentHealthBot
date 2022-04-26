from telegram import Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.update_user_state import update_user_state
from utils.find_user_by_telegram_user import find_user_by_telegram_user
from states import UserStates
from utils.user_by_telegram_username import user_by_telegram_username
from .message_templates import DELETE_DOCTOR_MESSAGE, DELETE_DOCTOR_SUCCESS_MESSAGE, DELETE_DOCTOR_ERROR_MESSAGE
from utils.delete_doctor_by_email import delete_doctor_by_email


def delete_doctor_start(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user_by_telegram_user(telegram_user)
    check_state(user.state, [UserStates.AUTHORIZED_ADMIN_STATE])
    update_user_state(user, UserStates.DELETE_DOCTOR_STATE)

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=DELETE_DOCTOR_MESSAGE,
    )


def delete_doctor(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user_by_telegram_user(telegram_user)
    doctor_username = update.message.text[1:]

    if delete_doctor_by_email(doctor_username) is True:
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=DELETE_DOCTOR_SUCCESS_MESSAGE,
        )
    else:
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=DELETE_DOCTOR_ERROR_MESSAGE,
        )
    update_user_state(user, UserStates.AUTHORIZED_ADMIN_STATE)
