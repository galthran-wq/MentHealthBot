from telegram.ext import CallbackContext
from utils.find_or_create_user import find_or_create_user
from utils.find_appeal import find_appeal
from .message_templates import SELECT_CONNECTION_MESSAGE
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from states import UserStates


def select_connection_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_or_create_user(telegram_user)

    if user.state == UserStates.SELECT_CONNECTION_STATE:
        appeal = find_appeal(user)
        appeal.language = update.callback_query.data

        connection_type_button = [
            InlineKeyboardButton(text="Личное (очное) общение", callback_data="personal"),
            InlineKeyboardButton(text="Онлайн-общение (Zoom/Skype)", callback_data="online"),
            InlineKeyboardButton(text="Переписка", callback_data="chat")
        ]

        kb = InlineKeyboardMarkup([[button] for button in connection_type_button])

        context.bot.send_message(
            chat_id=telegram_user.id,
            text=SELECT_CONNECTION_MESSAGE,
            reply_markup=kb
        )

        user.state = UserStates.PUBLIC_AWAITING_APPROVE_STATE
        user.save()
