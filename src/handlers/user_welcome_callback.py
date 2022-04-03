from telegram.ext import CallbackContext
from utils.find_user import find_user
from .message_templates import WELCOME_MESSAGE
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from states import UserStates

def user_welcome_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    auth_button = InlineKeyboardButton(
        text="Авторизоваться (ссылка)", callback_data="auth_button",
        url=f'''https://auth.hse.ru/adfs/oauth2/authorize/?client_id=0c80418a-a6bc-481f-9ab9-989139576fed&response_type=token&redirect_uri=https://studsovet.me/mental_bot_callback/auth&state={telegram_user.id}&response_mode=form_post'''
    )
    kb = InlineKeyboardMarkup([[auth_button]])

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=WELCOME_MESSAGE,
        reply_markup=kb
    )
