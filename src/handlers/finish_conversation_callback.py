from telegram.ext import CallbackContext
from utils.find_or_create_user import find_or_create_user
from .message_templates import FINISH_CONVERSATION_MESSAGE
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from states import UserStates


def finish_conversation_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_or_create_user(telegram_user)

    if user.state == UserStates.FINISH_CONVERSATION_STATE:
        share_problem_buttons = [
            InlineKeyboardButton(text="Поделиться проблемой", callback_data="share_problem"),
        ]
        kb = InlineKeyboardMarkup([[*share_problem_buttons]])

        context.bot.send_message(
            chat_id=telegram_user.id,
            text=FINISH_CONVERSATION_MESSAGE,
            reply_markup=kb
        )

        user.state = UserStates.SELECT_PROBLEM_STATE
        user.save()
