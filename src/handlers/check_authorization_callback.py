from asyncio.log import logger
from telegram import Update
from telegram.ext import CallbackContext
from handlers.authorized_user_callback import authorized_user_callback
from handlers.user_welcome_callback import user_welcome_callback
from states import UserStates
from utils import find_user


def check_authorization_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    if user is not None:
        user.state = (
            UserStates.DOCTOR_MENU_STATE if user.therapist
            else UserStates.SELECT_PROBLEM_STATE
        )
        print(f"User with mail={user.hse_mail} is authorized")
    else:
        user_welcome_callback(update, context)
