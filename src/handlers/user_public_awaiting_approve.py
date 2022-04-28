from re import search
from models.appeal import Appeal
from models.user import User
from states import UserStates
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.find_appeal_by_message_id_and_user import find_appeal_by_message_id_and_user
from utils.find_user import find_user
from utils.update_user_state import update_user_state

from .message_templates import PUBLIC_AWAITING_APPROVE_MESSAGE


def update_appeal(update: Update, user: User):
    r = search(r"(?P<message_id>[0-9]+.)_(?P<type>\w+)_connection_type_button", update.callback_query.data)
    conn = r.group("type")
    message_id = r.group("message_id")
    appeal = find_appeal_by_message_id_and_user(message_id, user)
    appeal.connection_type = conn
    appeal.save(only=[Appeal.connection_type])


def make_keyboard(message_id) -> InlineKeyboardMarkup:
    good_button = [
        InlineKeyboardButton(text="Со мной все хорошо!", callback_data=f"{message_id}_cancel_appeal_button"),
    ]
    kb = InlineKeyboardMarkup([[*good_button]])
    return kb


def user_public_awaiting_approve(update: Update, context: CallbackContext):
    update.callback_query.answer()
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    check_state(user.state, [UserStates.SELECT_CONNECTION_STATE])
    update_appeal(update, user)

    message_id = update.callback_query.data.split('_')[0]
    kb = make_keyboard(message_id)

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=PUBLIC_AWAITING_APPROVE_MESSAGE,
        reply_markup=kb
    )

    update_user_state(user, UserStates.PUBLIC_AWAITING_APPROVE_STATE)
