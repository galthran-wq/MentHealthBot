from re import search
from models.appeal import Appeal
from models.user import User
from states import UserStates
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.find_appeal_by_user_id import find_appeal_by_update_and_user
from utils.find_user import find_user
from utils.update_user_state import update_user_state

from .message_templates import PUBLIC_AWAITING_APPROVE_MESSAGE


def update_appeal(update: Update, user: User):
    appeal = find_appeal_by_update_and_user(update, user)
    conn = search(r"(?P<type>\w+)_connection_type_button", update.callback_query.data)
    conn = conn.group("type")
    appeal.connection_type = conn
    appeal.save(only=[Appeal.connection_type])


def make_keyboard() -> InlineKeyboardMarkup:
    good_button = [
        InlineKeyboardButton(text="Со мной все хорошо!", callback_data="cancel_appeal_button"),
    ]
    kb = InlineKeyboardMarkup([[*good_button]])
    return kb


def user_public_awaiting_approve(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    check_state(user.state, [UserStates.SELECT_CONNECTION_STATE])
    update_appeal(update, user)

    kb = make_keyboard()

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=PUBLIC_AWAITING_APPROVE_MESSAGE,
        reply_markup=kb
    )

    update_user_state(user, UserStates.PUBLIC_AWAITING_APPROVE_STATE)
