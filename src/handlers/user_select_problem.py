from models.problems import Problems
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      Update)
from telegram.ext import CallbackContext
from states import UserStates
from utils.check_state import check_state
from utils.create_appeal import create_appeal
from utils.find_user import find_user
from utils.update_user_state import update_user_state

from .message_templates.select_problem_message import SELECT_PROBLEM_MESSAGE


def get_default_problem_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for problem in Problems:
        buttons.append(InlineKeyboardButton(
            text="⬛ "+problem.value.name,
            callback_data=problem.value.button
        ))
    kb = InlineKeyboardMarkup([[btn] for btn in buttons])
    return kb


def user_select_problem(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    check_state(user.state, [UserStates.SELECT_PROBLEM_STATE, 
                             UserStates.FINISH_CONVERSATION_STATE])
    update_user_state(user, UserStates.SELECT_PROBLEM_STATE)
    
    create_appeal(user)

    kb = get_default_problem_keyboard()

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=SELECT_PROBLEM_MESSAGE,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb
    )
