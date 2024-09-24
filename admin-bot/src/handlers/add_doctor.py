from telegram import Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.update_user_state import update_user_state
from utils.find_user_by_telegram_user import find_user_by_telegram_user
from states import UserStates
from utils.make_user_an_doctor_by_email import make_user_an_doctor_by_email, make_user_an_doctor_by_telegram_username
from .message_templates import ADD_DOCTOR_MESSAGE, ADD_DOCTOR_SUCCESS_MESSAGE, ADD_DOCTOR_ERROR_MESSAGE
from utils.create_doctor_by_email import create_doctor_by_telegram_username


def add_doctor_start(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user_by_telegram_user(telegram_user)
    check_state(user.state, [UserStates.AUTHORIZED_ADMIN_STATE])
    update_user_state(user, UserStates.ADD_DOCTOR_STATE)

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=ADD_DOCTOR_MESSAGE,
    )

def add_doctor(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user_by_telegram_user(telegram_user)
    doctor_telegram_username = update.message.text

    if not make_user_an_doctor_by_telegram_username(doctor_telegram_username):
        create_doctor_by_telegram_username(doctor_telegram_username)
    context.bot.send_message(
        chat_id=telegram_user.id,
        text=ADD_DOCTOR_SUCCESS_MESSAGE,
    )
    update_user_state(user, UserStates.AUTHORIZED_ADMIN_STATE)
