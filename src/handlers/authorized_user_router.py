from re import search

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.find_user import find_user

from models import User
from handlers.message_templates import (WELCOME_DOCTOR_MESSAGE,
                                        WELCOME_PATIENT_MESSAGE)


def delete_previous_message(update: Update, context: CallbackContext):
    callback = update.callback_query.data
    r = search(r"auth_succesfull_(?P<msg_id>\d+)", callback)
    msg_id = int(r.group("msg_id"))
    context.bot.delete_message(
        chat_id=update.effective_user.id,
        message_id=msg_id
    )


def authorized_user_router(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    check_state(user.state, ["Authorization"])
    
    user.telegram_username = update.effective_user.username
    user.save(only=[User.telegram_username])

    delete_previous_message(update, context)

    if user.therapist:
        callback_query = "doctor_menu_button"
        message = WELCOME_DOCTOR_MESSAGE.format(
            user.first_name, user.last_name
        )
        next_button = InlineKeyboardButton(
            text="В главное меню",
            callback_data=callback_query
        )
    else:
        callback_query = "create_appeal_button"
        message = WELCOME_PATIENT_MESSAGE.format(
            user.first_name, user.last_name, user.hse_mail
        )
        next_button = InlineKeyboardButton(
            text="Создать новую заявку",
            callback_data=callback_query
        )

    keyboard = InlineKeyboardMarkup([[next_button]])

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=message,
        reply_markup=keyboard
    )
