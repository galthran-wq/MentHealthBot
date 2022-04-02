from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from .message_templates.select_problem_message import SELECT_PROBLEM_MESSAGE
from states import UserStates
from utils.find_or_create_user import find_or_create_user

problems = {"tired_problem_button": ["Выгорание и переутомление", False],
            "depressive_problem_button": ["Депрессивные состояния", False],
            "self_problem_button": ["Личные отношения", False],
            "kin_problem_button": ["Проблемы с родственниками", False],
            "surround_problem_button": ["Конфликты с окружающими", False],
            "nutrition_problem_button": ["Расстройства пищевого поведения", False],
            "adaptation_problem_button": ["Проблемы адаптации", False],
            "LGBT_problem_button": ["Проблемы LGBT+ community", False],
            "anxiety_problem_button": ["Тревожность", False]}


def select_problem_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_or_create_user(telegram_user)

    buttons = [InlineKeyboardButton(text="⬛ "+m[0], callback_data=btn)
               for btn, m in zip(problems.keys(), problems.values())]
    buttons.append(InlineKeyboardButton(
        text="Добавить свою", callback_data="add_custom_problem"))
    kb = InlineKeyboardMarkup([[btn] for btn in buttons])

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=SELECT_PROBLEM_MESSAGE,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb
    )


def change_problem_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_or_create_user(telegram_user)
    callback = update.callback_query.data
    global problems
    problems[callback][1] = not problems[callback][1]
    buttons = [InlineKeyboardButton(text=("☑️ " if m[1] else "⬛ ")+m[0], callback_data=btn)
            for btn, m in zip(problems.keys(), problems.values())]
    buttons.append(InlineKeyboardButton(
        text="Добавить свою", callback_data="add_custom_problem"))
    if sum(m[1] for m in problems.values()) != 0:
        buttons.append(InlineKeyboardButton(
            text="На следующий шаг", callback_data="done_selecting_problems_button"))

    kb = InlineKeyboardMarkup([[btn] for btn in buttons])
    update.callback_query.edit_message_reply_markup(kb)


def finish_problem_selecting_callback(update: Update, context: CallbackContext):
    #todo записать проблемы в БД
    #todo перейти на следующий стейт
    pass
       