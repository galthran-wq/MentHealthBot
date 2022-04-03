from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from .message_templates.select_problem_message import SELECT_PROBLEM_MESSAGE
from utils.find_user import find_user
from utils.create_appeal import create_appeal
from models.problems import Problems


def get_default_problem_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for problem in Problems:
        buttons.append(InlineKeyboardButton(
                text="⬛ "+problem.value.name,
                callback_data=problem.value.button
               ))
    kb = InlineKeyboardMarkup([[btn] for btn in buttons])
    return kb


def select_problem_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    create_appeal(user)

    kb = get_default_problem_keyboard()

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=SELECT_PROBLEM_MESSAGE,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb
    )
