from telegram.ext import CallbackContext
from utils.find_user import find_user
from .message_templates import USER_SELECTION_LANGUAGE_MESSAGE
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from states import UserStates


def user_selection_language_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    print(user.state)
    try:
        if user.state == UserStates.SELECT_PROBLEM_STATE:
            user.state = UserStates.LANGUAGE_SELECTION_STATE
        print(user.state)
        if user.state == UserStates.LANGUAGE_SELECTION_STATE:
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
    except AttributeError:
        print("UserError")
