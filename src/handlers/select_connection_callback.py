from telegram.ext import CallbackContext
from utils.find_user import find_user
from utils.find_appeal import find_appeal
from .message_templates import SELECT_CONNECTION_MESSAGE
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from states import UserStates


def select_connection_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    try:
        if user.state != UserStates.SELECT_CONNECTION_STATE:
            return "StateError"
        else:
            appeal = find_appeal(user)
            try:
                appeal.language = update.callback_query.data
                appeal.save()
            except AttributeError:
                print("AppealError")

            connection_type_button = [
                InlineKeyboardButton(text="Личное (очное) общение", callback_data="personal_connection_type_button"),
                InlineKeyboardButton(text="Онлайн-общение (Zoom/Skype)", callback_data="online_connection_type_button"),
                InlineKeyboardButton(text="Переписка", callback_data="chat_connection_type_button")
            ]

            kb = InlineKeyboardMarkup([[button] for button in connection_type_button])

            context.bot.send_message(
                chat_id=telegram_user.id,
                text=SELECT_CONNECTION_MESSAGE,
                reply_markup=kb
            )

            user.state = UserStates.PUBLIC_AWAITING_APPROVE_STATE
            user.save()
    except AttributeError:
        print("UserError")
