from telegram.ext import CallbackContext
from utils.find_or_create_user import find_or_create_user
from .message_templates import USER_SELECTION_LANGUAGE_MESSAGE
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from states import UserStates


def user_selection_language_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_or_create_user(telegram_user)

    if user.state == UserStates.LANGUAGE_SELECTION_STATE:
        telegram_user = update.effective_user
        user = find_or_create_user(telegram_user)

        # if user.state == UserStates.SELECT_CONNECTION_STATE:
        language_buttons = [InlineKeyboardButton(text="Русский", callback_data="russia"),
                            InlineKeyboardButton(text="Английский", callback_data="english")]

        kb = InlineKeyboardMarkup([[*language_buttons]])

        context.bot.send_message(
            chat_id=telegram_user.id,
            text=USER_SELECTION_LANGUAGE_MESSAGE,
            reply_markup=kb
        )

        user.state = UserStates.SELECT_CONNECTION_STATE
        user.save()
