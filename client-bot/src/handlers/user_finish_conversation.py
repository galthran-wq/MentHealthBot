from models.appeal import Appeal
from models.user import User
from states import UserStates
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.find_appeal_by_message_id_and_user import find_appeal_by_message_id_and_user
from utils.find_user import find_user
from utils.update_user_state import update_user_state

from .message_templates import FINISH_CONVERSATION_MESSAGE


def update_appeal(update: Update, user: User):
    message_id = int(update.callback_query.data.split('_')[0])
    appeal = find_appeal_by_message_id_and_user(message_id, user)
    appeal.active = False
    appeal.save(only=[Appeal.active])


def user_finish_conversation(update: Update, context: CallbackContext):
    update.callback_query.answer()
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    check_state(user.state, [UserStates.PUBLIC_AWAITING_APPROVE_STATE,
                             UserStates.ANON_AWAITING_APPROVE_STATE])
    update_appeal(update, user)

    share_problem_buttons = [InlineKeyboardButton(
                                text="Поделиться проблемой",
                                callback_data="create_appeal_button")]
    kb = InlineKeyboardMarkup([[*share_problem_buttons]])

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=FINISH_CONVERSATION_MESSAGE,
        reply_markup=kb
    )

    update_user_state(user, UserStates.FINISH_CONVERSATION_STATE)
