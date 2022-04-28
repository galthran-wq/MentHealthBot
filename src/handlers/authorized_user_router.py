from models import User, Appeal
from states import UserStates
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.find_or_create_user import find_or_create_user

from handlers.message_templates import WELCOME_PATIENT_MESSAGE, WELCOME_DOCTOR_MESSAGE
from utils.update_user_state import update_user_state
from re import search


def delete_previous_message(update: Update, context: CallbackContext):
    callback = update.callback_query.data
    r = search(r"auth_succesfull_(?P<msg_id>\d+)", callback)
    msg_id = int(r.group("msg_id"))
    context.bot.delete_message(
        chat_id=update.effective_user.id,
        message_id=msg_id
    )


def delete_previous_appeals(update: Update, context: CallbackContext):
    chat_id = update.effective_user.id
    if User.select().where(User.telegram_id == chat_id).exists():
        user_id = User.select().where(User.telegram_id == chat_id).get().id
        for appeal in Appeal.select().where((Appeal.patient == user_id) & (Appeal.active)):
            appeal.active = False
            appeal.save(only=[Appeal.active])


def authorized_user_router(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_or_create_user(telegram_user)

    delete_previous_message(update, context)
    delete_previous_appeals(update, context)

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
