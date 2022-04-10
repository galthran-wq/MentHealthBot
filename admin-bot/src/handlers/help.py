from telegram import Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.find_user_by_telegram_user import find_user_by_telegram_user
from states import UserStates
from .message_templates import HELP_MESSAGE


def help(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user_by_telegram_user(telegram_user)
    check_state(user.state, [UserStates.AUTHORIZED_ADMIN_STATE])
    context.bot.send_message(
        chat_id=telegram_user.id,
        text=HELP_MESSAGE,
    )
