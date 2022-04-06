from models.user import User
from states import UserStates
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.find_or_create_user import find_or_create_user

from handlers.message_templates import WELCOME_PATIENT_MESSAGE, WELCOME_DOCTOR_MESSAGE
from utils.update_user_state import update_user_state


def authorized_user_router(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_or_create_user(telegram_user)

    if user.therapist:
        callback_query = "doctor_menu_button"
        message = WELCOME_DOCTOR_MESSAGE.format(
            user.first_name, user.last_name
        )
        update_user_state(user, UserStates.DOCTOR_MENU_STATE)
    else:
        callback_query = "create_appeal_button"
        message = WELCOME_PATIENT_MESSAGE.format(
            user.first_name, user.last_name, user.hse_mail
        )
        update_user_state(user, UserStates.SELECT_PROBLEM_STATE)
    next_button = InlineKeyboardButton(
        text="Далее",
        callback_data=callback_query
    )
    keyboard = InlineKeyboardMarkup([[next_button]])

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=message,
        reply_markup=keyboard
    )
