from telegram import Update
from telegram.ext import CallbackContext
from handlers.authorized_user_callback import authorized_user_callback
from states import UserStates

from utils.find_or_create_user import find_or_create_user


def check_authorization_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_or_create_user(telegram_user)
    if user is None:
        authorized_user_callback(update, context)
    user.state = (
        UserStates.DOCTOR_MENU_STATE if user.therapist
        else UserStates.SELECT_PROBLEM_STATE
    )

