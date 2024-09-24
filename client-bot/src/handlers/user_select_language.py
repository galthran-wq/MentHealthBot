from models.appeal import Appeal
from states import UserStates
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.find_user import find_user
from utils.update_user_state import update_user_state

from .message_templates import USER_SELECTION_LANGUAGE_MESSAGE


def make_keyboard(message_id) -> InlineKeyboardMarkup:
    language_buttons = [InlineKeyboardButton(
        text="Русский",
        callback_data=f"{message_id}_set_russian_lang_button"),
        InlineKeyboardButton(
        text="English",
        callback_data=f"{message_id}_set_english_lang_button")]
    kb = InlineKeyboardMarkup([[*language_buttons]])
    return kb


def user_select_language(update: Update, context: CallbackContext):
    update.callback_query.answer()
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    check_state(user.state, [UserStates.SELECT_PROBLEM_STATE])

    message_id = update.callback_query.data.split('_')[0]
    kb = make_keyboard(message_id)

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=USER_SELECTION_LANGUAGE_MESSAGE,
        reply_markup=kb
    )

    update_user_state(user, UserStates.LANGUAGE_SELECTION_STATE)
