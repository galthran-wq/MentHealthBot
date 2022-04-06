from re import search
from states import UserStates
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.find_appeal_by_user_id import find_appeal_by_user_id
from utils.find_user import find_user
from utils.update_user_state import update_user_state

from .message_templates import PUBLIC_AWAITING_APPROVE_MESSAGE


def user_public_awaiting_approve(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    if user.state == UserStates.SELECT_CONNECTION_STATE:
        update_user_state(user, UserStates.PUBLIC_AWAITING_APPROVE_STATE)
        appeal = find_appeal_by_user_id(user)
        try:
            conn = search(r"(?P<type>\w+)_connection_type_button", update.callback_query.data)
            conn = conn.group("type")
            appeal.update(connection_type=conn).execute()
        except AttributeError:
            print("AppealError")

        good_button = [
            InlineKeyboardButton(text="Со мной все хорошо!", callback_data="cancel_appeal_button"),
        ]

        kb = InlineKeyboardMarkup([[*good_button]])

        context.bot.send_message(
            chat_id=telegram_user.id,
            text=PUBLIC_AWAITING_APPROVE_MESSAGE,
            reply_markup=kb
        )
    else:
        print("StateError")
