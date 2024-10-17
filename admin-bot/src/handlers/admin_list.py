import logging
from telegram import Update
from telegram.ext import CallbackContext, ContextTypes
from utils.find_all_admin import find_all_admin
from utils.find_user_by_telegram_user import find_user_by_telegram_user
from utils.check_state import check_state
from states import UserStates
from .message_templates import ADMIN_LIST_EMPTY_MESSAGE

async def admin_list(update: Update, context) -> None:
    user_id = update.effective_user.id
    logging.info(f"Admin list requested by user {user_id}")
    
    telegram_user = update.effective_user
    user = find_user_by_telegram_user(telegram_user)
    logging.info(f"User {user_id} found in database")
    
    try:
        check_state(user.state, [UserStates.AUTHORIZED_ADMIN_STATE])
        logging.info(f"User {user_id} state verified as authorized admin")
    except Exception as e:
        logging.error(f"User {user_id} state verification failed: {str(e)}")
        await update.message.reply_text("You are not authorized to view the admin list.")
        return
    
    admins = find_all_admin()
    logging.info(f"Retrieved {len(admins)} admins from database")
    
    if len(admins) > 0:
        admin_list_text = 'Список администраторов:\n' + '\n'.join([admin.telegram_username for admin in admins])
        await update.message.reply_text(admin_list_text)
        logging.info(f"Admin list sent to user {user_id}")
    else:
        await update.message.reply_text(ADMIN_LIST_EMPTY_MESSAGE)
        logging.info(f"Empty admin list message sent to user {user_id}")
