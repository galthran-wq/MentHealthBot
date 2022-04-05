from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from utils.find_appeal_by_user_id import find_appeal_by_user_id
from utils.find_user import find_user
from models.problems import Problems, Problem


def get_problem_keyboard(user_problems: list) -> InlineKeyboardMarkup:
    buttons = []
    for problem in Problems:
        buttons.append(InlineKeyboardButton(
            text=("☑️ " if problem.value.short in user_problems else "⬛ ") +
            problem.value.name,
            callback_data=problem.value.button
        ))
    if user_problems:
        buttons.append(InlineKeyboardButton(
            text="На следующий шаг", callback_data="done_selecting_problems_button"))
    kb = InlineKeyboardMarkup([[btn] for btn in buttons])
    return kb


def change_problem_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    appeal = find_appeal_by_user_id(user)
    callback = update.callback_query.data
    problem = callback.split("_")[0]
    if problem in appeal.problems:
        appeal.problems.remove(problem)
    else:
        appeal.problems.append(problem)
    appeal.save()

    kb = get_problem_keyboard(appeal.problems)

    update.callback_query.edit_message_reply_markup(kb)
