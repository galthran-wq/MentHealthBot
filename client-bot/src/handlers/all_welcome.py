from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from .message_templates import WELCOME_MESSAGE
from .authorized_user_router import authorized_user_router


def all_welcome(update: Update, context: CallbackContext):
    telegram_user = update.effective_user

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=WELCOME_MESSAGE,
    )

    authorized_user_router(update, context)