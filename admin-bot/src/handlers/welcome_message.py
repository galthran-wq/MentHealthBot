import logging
from telegram import Update
from telegram.ext import CallbackContext
from utils.check_admin import check_admin
from utils.find_user_by_telegram_user import find_user_by_telegram_user
from utils.update_user_state import update_user_state
from states import UserStates
from .message_templates import WELCOME_MESSAGE
from .message_templates import AUTHORIZATION_ERROR_MESSAGE


def welcome_message(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    logging.info(f"Telegram user \"{telegram_user.username}\" is logging into admin panel")
    
    user = find_user_by_telegram_user(telegram_user)
    if user is not None:
        logging.info(f"Found User(id={user.id}, username={user.telegram_username}, admin={user.admin})")
    else:
        logging.info(f"User is not found for \"{telegram_user.username}\"!")

    if check_admin(telegram_user):
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=WELCOME_MESSAGE,
        )
        update_user_state(user, UserStates.AUTHORIZED_ADMIN_STATE)
    else:
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=AUTHORIZATION_ERROR_MESSAGE,
        )
        update_user_state(user, UserStates.ERROR_AUTHORIZATION_ADMIN_STATE)
