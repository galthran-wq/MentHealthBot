import logging
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

    logging.info(f"User \"{telegram_user.username}\" is trying to add a doctor")
    if user is not None:
        logging.info(f"Found User(id={user.id}, username={user.telegram_username}, admin={user.admin})")
    else:
        logging.info(f"User is not found for \"{telegram_user.username}\"!")

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
    logging.info(f"User \"{telegram_user.username}\" is trying to add a doctor {doctor_telegram_username}")
    if user is not None:
        logging.info(f"Found User(id={user.id}, username={user.telegram_username}, admin={user.admin})")
    else:
        logging.info(f"User is not found for \"{telegram_user.username}\"!")

    if not make_user_an_doctor_by_telegram_username(doctor_telegram_username):
        logging.info(f"Didn't find a user for \"{doctor_telegram_username}\". Creating a random one with doctor privileges")
        create_doctor_by_telegram_username(doctor_telegram_username)
    context.bot.send_message(
        chat_id=telegram_user.id,
        text=ADD_DOCTOR_SUCCESS_MESSAGE,
    )
    update_user_state(user, UserStates.AUTHORIZED_ADMIN_STATE)
