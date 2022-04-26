from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from .message_templates import WELCOME_MESSAGE


def all_welcome(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    client_id = "fedded7a-a595-424d-84d4-e43db36e945e"
    payload = f"{telegram_user.id}0"
    auth_button = InlineKeyboardButton(
        text="Авторизоваться", callback_data="auth_button",
        url=f'''https://auth.hse.ru/adfs/oauth2/authorize/?client_id={client_id}&response_type=token&redirect_uri=https://studsovet.me/mental_bot_callback/auth&state={payload}&response_mode=form_post'''
    )
    kb = InlineKeyboardMarkup([[auth_button]])

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=WELCOME_MESSAGE,
        reply_markup=kb
    )
