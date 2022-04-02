from telegram.ext import CallbackContext
from utils.find_or_create_user import find_or_create_user
from .message_templates import PUBLIC_AWAITING_APPROVE_MESSAGE
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from states import UserStates


def public_awaiting_approve_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_or_create_user(telegram_user)

    if user.state == UserStates.PUBLIC_AWAITING_APPROVE_STATE:
        print(update.callback_query.data)  # ToDo: Save to DB

        good_button = [
            InlineKeyboardButton(text="Со мной все хорошо!", callback_data="good"),
        ]

        kb = InlineKeyboardMarkup([[*good_button]])

        context.bot.send_message(
            chat_id=telegram_user.id,
            text=PUBLIC_AWAITING_APPROVE_MESSAGE,
            reply_markup=kb
        )

        user.state = UserStates.FINISH_CONVERSATION_STATE
        user.save()
