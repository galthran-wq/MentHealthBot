from re import search
from models.appeal import Appeal
from models.problems import Problems, Problem
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from states import UserStates
from utils.check_state import check_state
from utils.find_appeal_by_user_id import find_appeal_by_update_and_user
from utils.find_user import find_user


def get_problem_keyboard(appeal: Appeal) -> InlineKeyboardMarkup:
    buttons = []
    user_problems = appeal.problems
    for problem in Problems:
        buttons.append(InlineKeyboardButton(
            text=("☑️ " if problem.value.short in user_problems else "⬛ ") +
            problem.value.name,
            callback_data=problem.value.button
        ))
    if user_problems:
        buttons.append(InlineKeyboardButton(
            text="На следующий шаг", callback_data=f"{appeal.message_id}_done_selecting_problems_button"))
    kb = InlineKeyboardMarkup([[btn] for btn in buttons])
    return kb


def user_change_problem(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    check_state(user.state, [UserStates.SELECT_PROBLEM_STATE])

    appeal = find_appeal_by_update_and_user(update, user)
    callback = update.callback_query.data
    problem = search(r"(?P<problem>\w+)_problem_button", callback)
    problem = problem.group("problem")
    #todo: replace save() to update() method
    if problem in appeal.problems:
        appeal.problems.remove(problem)
    else:
        appeal.problems.append(problem)
    appeal.save()

    kb = get_problem_keyboard(appeal)
    update.callback_query.edit_message_reply_markup(kb)
