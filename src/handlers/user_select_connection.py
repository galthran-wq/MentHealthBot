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

from .message_templates import SELECT_CONNECTION_MESSAGE


def update_appeal(update: Update, user: User):
    r = search(r"(?P<message_id>[0-9]+.)_set_(?P<lang>\w+)_lang_button", update.callback_query.data)
    lang = r.group("lang")
    message_id = r.group("message_id")
    appeal = find_appeal_by_message_id_and_user(message_id, user)
    appeal.language = lang
    appeal.save(only=[Appeal.language])


def make_keyboard(message_id) -> InlineKeyboardMarkup:
    connection_type_button = [
        InlineKeyboardButton(
            text="Очная встреча",
            callback_data=f"{message_id}_personal_connection_type_button"),
        InlineKeyboardButton(
            text="Zoom/Skype",
            callback_data=f"{message_id}_online_connection_type_button"),
        InlineKeyboardButton(
            text="Чат",
            callback_data=f"{message_id}_chat_connection_type_button")
    ]
    kb = InlineKeyboardMarkup([[*connection_type_button]])
    return kb


def user_select_connection(update: Update, context: CallbackContext):
    update.callback_query.answer()
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    check_state(user.state, [UserStates.LANGUAGE_SELECTION_STATE])
    update_appeal(update, user)

    message_id = update.callback_query.data.split('_')[0]
    kb = make_keyboard(message_id)

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=SELECT_CONNECTION_MESSAGE,
        reply_markup=kb
    )

    update_user_state(user, UserStates.SELECT_CONNECTION_STATE)
