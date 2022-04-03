from subprocess import call
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from utils.find_appeal import find_appeal
from .message_templates.select_problem_message import SELECT_PROBLEM_MESSAGE
from states import UserStates
from utils.find_user import find_user
from utils.create_appeal import create_appeal


class Problem():
    def __init__(self, name, button):
        self.name = name
        self.button = button
        self.short = button.split("_")[0]


class Problems():
    TIRED = Problem("Выгорание и переутомление", "tired_problem_button")
    DEPRESSIVE = Problem("Депрессивные состояния", "depressive_problem_button")
    SELF = Problem("Личные отношения", "self_problem_button")
    KIN = Problem("Проблемы с родственниками", "kin_problem_button")
    SURROUND = Problem("Конфликты с окружающими", "surround_problem_button")
    NUTRITION = Problem("Расстройства пищевого поведения",
                        "nutrition_problem_button")
    ADAPTATION = Problem("Проблемы адаптации", "adaptation_problem_button")
    LGBT = Problem("Проблемы LGBT+ community", "LGBT_problem_button")
    ANXIETY = Problem("Тревожность", "anxiety_problem_button")

    def list(self):
        return [self.TIRED,
                self.DEPRESSIVE,
                self.SELF,
                self.KIN,
                self.SURROUND,
                self.NUTRITION,
                self.ADAPTATION,
                self.LGBT,
                self.ANXIETY]


def select_problem_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    create_appeal(user)

    buttons = [InlineKeyboardButton(text="⬛ "+m.name, callback_data=m.button)
               for m in Problems().list()]
    # buttons.append(InlineKeyboardButton(
    #     text="Добавить свою", callback_data="add_custom_problem"))
    kb = InlineKeyboardMarkup([[btn] for btn in buttons])

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=SELECT_PROBLEM_MESSAGE,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb
    )


def change_problem_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    appeal = find_appeal(user)
    callback = update.callback_query.data
    problem = callback.split("_")[0]
    if problem in appeal.problems:
        appeal.problems.remove(problem)
    else:
        appeal.problems.append(problem)
    appeal.save()
    buttons = [InlineKeyboardButton(
                text=("☑️ " if m.short in appeal.problems else "⬛ ")+m.name,
                callback_data=m.button
               ) for m in Problems().list()]
    # buttons.append(InlineKeyboardButton(
    #     text="Добавить свою", callback_data="add_custom_problem"))
    if len(appeal.problems) != 0:
        buttons.append(InlineKeyboardButton(
            text="На следующий шаг", callback_data="done_selecting_problems_button"))

    kb = InlineKeyboardMarkup([[btn] for btn in buttons])
    update.callback_query.edit_message_reply_markup(kb)


def done_problem_selecting_callback(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    user.state = UserStates.LANGIAGE_SELECTION_STATE
    user.save()
