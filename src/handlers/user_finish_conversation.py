from states import UserStates
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.find_user import find_user

from .message_templates import FINISH_CONVERSATION_MESSAGE


def user_finish_conversation(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)

    try:
        if user.state != UserStates.FINISH_CONVERSATION_STATE:
            print("StateError")
        else:
            share_problem_buttons = [InlineKeyboardButton(
                                        text="Поделиться проблемой", 
                                        callback_data="create_appeal_button")]
            kb = InlineKeyboardMarkup([[*share_problem_buttons]])

            context.bot.send_message(
                chat_id=telegram_user.id,
                text=FINISH_CONVERSATION_MESSAGE,
                reply_markup=kb
            )

            user.state = UserStates.SELECT_PROBLEM_STATE
            user.save()
    except AttributeError:
        print("UserError")
