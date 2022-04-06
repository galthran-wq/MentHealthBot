from re import search
from models.user import User
from states import UserStates
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.find_appeal_by_user_id import find_appeal_by_user_id
from utils.find_user import find_user
from utils.update_user_state import update_user_state

from .message_templates import SELECT_CONNECTION_MESSAGE


def update_appeal(user: User, callback: Update.CALLBACK_QUERY):
    appeal = find_appeal_by_user_id(user)
    lang = search(r"set_(?P<lang>\w+)_lang_button", callback.data)
    lang = lang.group("lang")
    appeal.update(language=lang).execute()


def make_keyboard() -> InlineKeyboardMarkup:
    connection_type_button = [
        InlineKeyboardButton(
            text="Личное (очное) общение",
            callback_data="personal_connection_type_button"),
        InlineKeyboardButton(
            text="Онлайн-общение (Zoom/Skype)",
            callback_data="online_connection_type_button"),
        InlineKeyboardButton(
            text="Переписка",
            callback_data="chat_connection_type_button")
    ]
    kb = InlineKeyboardMarkup([[*connection_type_button]])
    return kb


def user_select_connection(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    check_state(user.state, [UserStates.LANGUAGE_SELECTION_STATE])
    update_user_state(user, UserStates.SELECT_CONNECTION_STATE)
    update_appeal(user, update.callback_query)

    kb = make_keyboard()

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=SELECT_CONNECTION_MESSAGE,
        reply_markup=kb
    )
