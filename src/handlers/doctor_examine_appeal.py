import logging
from re import search
from models.connection_types import connections
from models.exceptions import StateError
from models.problems import Problems
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext
from states import UserStates
from utils.find_appeal_by_id import find_appeal_by_id
from utils.find_user import find_user
from utils.find_user_by_id import find_user_by_id
from utils.update_user_state import update_user_state
from .message_templates.doctor_examine_appeal_message import MESSAGE


def make_problems_list(appeal_problems):
    problems = []
    for problem in Problems:
        if problem.value.short in appeal_problems:
            problems.append(f"- {problem.value.name}")
    problems = "\n".join(problems)


def make_keyboard(appeal):
    buttons = [InlineKeyboardButton(
        text=f"Принять вызов",
        callback_data=f"take_appeal_{appeal.id}_button"
    ),
        InlineKeyboardButton(
        text=f"Назад",
        callback_data="new_appeals_menu_button"
    )]
    kb = InlineKeyboardMarkup([[btn] for btn in buttons])
    return kb


def doctor_examine_appeal(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    if user.state != UserStates.SELECT_APPEAL_STATE:
        logging.info(f"User state is {user.state}")
        raise StateError("User state is incorrect.")
    update_user_state(user, UserStates.EXAMINE_APPEAL_STATE)
    appeal_id = search(r"(?P<id>\d+)", update.callback_query.data)
    appeal_id = appeal_id.group("id")
    appeal = find_appeal_by_id(appeal_id)
    patient = find_user_by_id(appeal.patient_id)

    kb = make_keyboard(appeal)
    name = " ".join([patient.first_name, patient.last_name])
    problems = make_problems_list(appeal.problems)
    conn_type = connections[appeal.connection_type]

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=MESSAGE.format(name, problems, conn_type),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb
    )
