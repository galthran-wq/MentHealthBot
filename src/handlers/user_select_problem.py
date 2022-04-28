from models import Appeal, User
from models.problems import Problems
from states import UserStates
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      Update)
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.create_appeal import create_appeal
from utils.find_user import find_user
from utils.update_user_state import update_user_state

from .message_templates import DELETED_PREVIOUS_APPEALS_MESSAGE
from .message_templates.select_problem_message import SELECT_PROBLEM_MESSAGE


def delete_previous_appeals(update: Update, context: CallbackContext) -> bool:
    chat_id = update.effective_user.id
    user_has_old_appeals = False
    if User.select().where(User.telegram_id == chat_id).exists():
        user_id = User.select().where(User.telegram_id == chat_id).get().id
        for appeal in Appeal.select().where((Appeal.patient == user_id) & (Appeal.active)):
            user_has_old_appeals = True
            appeal.active = False
            appeal.save(only=[Appeal.active])
    if user_has_old_appeals:
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text=DELETED_PREVIOUS_APPEALS_MESSAGE
        )


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
    update.callback_query.answer()
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    check_state(user.state, ["Authorization",
                             UserStates.FINISH_CONVERSATION_STATE])

    delete_previous_appeals(update, context)

    kb = get_default_problem_keyboard()

    msg = context.bot.send_message(
        chat_id=telegram_user.id,
        text=SELECT_PROBLEM_MESSAGE,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb
    )

    create_appeal(msg, user)

    update_user_state(user, UserStates.SELECT_PROBLEM_STATE)
