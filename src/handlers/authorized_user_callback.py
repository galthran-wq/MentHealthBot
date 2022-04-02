
from telegram.ext import CallbackContext
from telegram import Update
from handlers.message_templates.welcome_doctor_message import WELCOME_DOCTOR_MESSAGE
from handlers.message_templates.welcome_patient_message import WELCOME_PATIENT_MESSAGE
from models.user import User
from states import UserStates
from utils.find_or_create_user import find_or_create_user

def authorized_user_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_or_create_user(telegram_user)

    if user.therapist:
        message = WELCOME_DOCTOR_MESSAGE.format(
            user.first_name, user.last_name
        )
        user.state = UserStates.DOCTOR_MENU_STATE
    else:
        message = WELCOME_PATIENT_MESSAGE.format(
            user.first_name, user.last_name, user.hse_mail
        )
        user.state = User.state = UserStates.SELECT_PROBLEM_STATE
    context.bot.send_message(
        chat_id=telegram_user.id,
        text=message,
    )
