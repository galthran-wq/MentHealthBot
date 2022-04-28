from telegram import Update
from telegram.ext import CallbackContext
from utils.find_all_admin import find_all_admin
from utils.find_user_by_telegram_user import find_user_by_telegram_user
from utils.check_state import check_state
from states import UserStates
from .message_templates import ADMIN_LIST_EMPTY_MESSAGE


def admin_list(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user_by_telegram_user(telegram_user)
    check_state(user.state, [UserStates.AUTHORIZED_ADMIN_STATE])
    admins = find_all_admin()
    admin_list_text = 'Список администраторов:\n'
    for admin in admins:
        admin_list_text += '{}\n'.format(admin.hse_mail)
    if len(admins) > 0:
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=admin_list_text
        )
    else:
        context.bot.send_message(
            chat_id=telegram_user.id,
            text=ADMIN_LIST_EMPTY_MESSAGE
        )
