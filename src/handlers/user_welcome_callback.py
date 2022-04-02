from telegram.ext import CallbackContext
from utils.find_or_create_user import find_or_create_user
from .message_templates import WELCOME_MESSAGE
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from states import UserStates

def user_welcome_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_or_create_user(telegram_user)
    auth_button = InlineKeyboardButton(
        text="Авторизоваться (ссылка)", callback_data="auth_button"
    )
    kb = InlineKeyboardMarkup([[auth_button]])

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=WELCOME_MESSAGE,
        reply_markup=kb
    )

    user.state = UserStates.AWAITING_AUTHORIZATION_STATE
    user.save()

