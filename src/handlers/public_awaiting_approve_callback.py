from telegram.ext import CallbackContext
from utils.find_user import find_user
from utils.find_appeal_by_user_id import find_appeal_by_user_id
from .message_templates import PUBLIC_AWAITING_APPROVE_MESSAGE
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from states import UserStates


def public_awaiting_approve_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    try:
        if user.state != UserStates.PUBLIC_AWAITING_APPROVE_STATE:
            print("StateError")
        else:
            appeal = find_appeal_by_user_id(user)
            try:
                appeal.connection_type = update.callback_query.data.split("_")[0]
                appeal.save()
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

            user.state = UserStates.FINISH_CONVERSATION_STATE
            user.save()
    except AttributeError:
        print("UserError")
