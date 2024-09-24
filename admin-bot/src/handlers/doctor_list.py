from telegram import Update
from telegram.ext import CallbackContext
from utils.find_all_doctor import find_all_doctor
from utils.find_user_by_telegram_user import find_user_by_telegram_user
from utils.check_state import check_state
from states import UserStates
from .message_templates import DOCTOR_LIST_EMPTY_MESSAGE


def doctor_list(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user_by_telegram_user(telegram_user)
    check_state(user.state, [UserStates.AUTHORIZED_ADMIN_STATE])

    doctors = find_all_doctor()
    doctor_list_text = 'Список волонтеров:\n'
    for doctor in doctors:
        doctor_list_text += '{}\n'.format(doctor.telegram_username)
    if len(doctors) > 0:
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=doctor_list_text
        )
    else:
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=DOCTOR_LIST_EMPTY_MESSAGE
        )
