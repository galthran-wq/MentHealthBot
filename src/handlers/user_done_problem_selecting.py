from states import UserStates
from telegram import Update
from telegram.ext import CallbackContext
from utils.find_user import find_user


def user_done_problem_selecting(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    user.state = UserStates.LANGUAGE_SELECTION_STATE
    user.save()
