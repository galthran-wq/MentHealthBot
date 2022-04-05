from models.problems import Problems
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from states import UserStates
from utils.find_appeal_by_user_id import find_appeal_by_user_id
from utils.find_user import find_user


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


def user_change_problem(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    print(user.state)
    if user.state == UserStates.SELECT_PROBLEM_STATE:
        appeal = find_appeal_by_user_id(user)
        callback = update.callback_query.data
        problem = callback.split("_")[0]
        #todo: replace save() to update() method
        if problem in appeal.problems:
            appeal.problems.remove(problem)
        else:
            appeal.problems.append(problem)
        appeal.save()

        kb = get_problem_keyboard(appeal.problems)

        update.callback_query.edit_message_reply_markup(kb)
    else:
        print("StateError")
