from states import UserStates
from telegram import Update
from telegram.ext import CallbackContext
from utils import find_user

from handlers.all_welcome import all_welcome


def check_authorization(update: Update, context: CallbackContext):
    update.callback_query.answer()
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    if user is not None:
        user.state = (
            UserStates.DOCTOR_MENU_STATE if user.therapist
            else UserStates.SELECT_PROBLEM_STATE
        )
        print(f"User with mail={user.hse_mail} is authorized")
    else:
        all_welcome(update, context)
