from telegram.ext import CallbackContext
from telegram import Update
from states import UserStates
from utils.find_user import find_user


def done_problem_selecting_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    user.state = UserStates.LANGUAGE_SELECTION_STATE
    user.save()
