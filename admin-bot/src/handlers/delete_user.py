from telegram import Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.update_user_state import update_user_state
from utils.find_user_by_telegram_user import find_user_by_telegram_user
from states import UserStates
from utils.delete_user_by_telegram_username import delete_user_by_telegram_username
DELETE_USER_MESSAGE = "Пожалуйста, введите имя пользователя Telegram пользователя, которого вы хотите удалить."
DELETE_USER_SUCCESS_MESSAGE = "Пользователь успешно удален."
DELETE_USER_ERROR_MESSAGE = "Ошибка: Пользователь не найден или не может быть удален."

def delete_user_start(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user_by_telegram_user(telegram_user)
    check_state(user.state, [UserStates.AUTHORIZED_ADMIN_STATE])
    update_user_state(user, UserStates.DELETE_USER_STATE)

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=DELETE_USER_MESSAGE,
    )


def delete_user(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user_by_telegram_user(telegram_user)
    user_telegram_username = update.message.text

    if delete_user_by_telegram_username(user_telegram_username):
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=DELETE_USER_SUCCESS_MESSAGE,
        )
    else:
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=DELETE_USER_ERROR_MESSAGE,
        )
    update_user_state(user, UserStates.AUTHORIZED_ADMIN_STATE)
